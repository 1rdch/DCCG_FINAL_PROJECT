import numpy as np
import random
import math
import os
import compas.geometry as cg
from compas.datastructures import Mesh
from compas_cgal.triangulation import refined_delaunay_mesh as rdm
from compas_cgal.meshing import trimesh_remesh
from compas_viewer.viewer import Viewer
from compas.colors import Color

# =============================================================================
# 1. 參數設定與長方形邊界 (90m x 5m)
# =============================================================================
L, W = 90.0, 5.0
WALKWAY_Z = -5.0 

# 生成長方形邊界點，並增加點密度以利後續「有機化」
boundary_pts = []
# 長邊點
for x in np.linspace(-L/2, L/2, 60): boundary_pts.append([x, W/2, 0])
# 短邊點
for y in np.linspace(W/2, -W/2, 10): boundary_pts.append([L/2, y, 0])
# 下長邊
for x in np.linspace(L/2, -L/2, 60): boundary_pts.append([x, -W/2, 0])
# 左短邊
for y in np.linspace(-W/2, W/2, 10): boundary_pts.append([-L/2, y, 0])

boundary = cg.Polygon(boundary_pts)
boundary_coords = np.array(boundary, dtype=np.float64)

# =============================================================================
# 2. 生成孔洞參數 (準備收束成 0.3-0.4m)
# =============================================================================
num_holes = 7
hole_params = []
spacing = L / (num_holes + 1)
for i in range(num_holes):
    x_pos = -L/2 + (i + 1) * spacing + random.uniform(-2.0, 2.0)
    y_pos = random.uniform(-0.5, 0.5)
    hole_params.append({
        'center': [x_pos, y_pos, 0],
        'radius': random.uniform(0.6, 0.8), # 初始開孔半徑
        'target_radius': random.uniform(0.3, 0.4) # 需求1：收束後的半徑 (直徑0.3-0.4m)
    })

holes = []
for params in hole_params:
    poly = cg.Polygon.from_sides_and_radius_xy(20, params['radius'])
    h_poly = poly.transformed(cg.Translation.from_vector(params['center']))
    holes.append(np.array(h_poly, dtype=np.float64))

# =============================================================================
# 3. 初始網格與頂點操縱 (收束邏輯)
# =============================================================================
V, F = rdm(boundary_coords, holes=holes, maxlength=0.5, is_optimized=True)
mesh = Mesh.from_vertices_and_faces(V, F)

fixed_vertices = set()
for v in mesh.vertices():
    if mesh.is_vertex_on_boundary(v):
        x, y, z = mesh.vertex_coordinates(v)
        
        # 判定是否為外框：需求2：讓外框有機化/滑順化
        if abs(x) > (L/2 - 0.2) or abs(y) > (W/2 - 0.2):
            # 讓外框產生微小的 Y 軸波動，使其不那麼死板
            new_y = y + 0.3 * math.sin(0.5 * x)
            mesh.vertex_attribute(v, 'y', new_y)
            fixed_vertices.add(v)
        else:
            # 判定為孔洞底緣：需求1：收束至直徑 0.3-0.4m
            for params in hole_params:
                dist = ((x - params['center'][0])**2 + (y - params['center'][1])**2)**0.5
                if dist < params['radius'] + 0.1:
                    cx, cy, _ = params['center']
                    # 計算收縮向量
                    vec = cg.Vector(x - cx, y - cy, 0)
                    vec.unitize()
                    # 將頂點移動到目標半徑位置
                    new_x = cx + vec.x * params['target_radius']
                    new_y = cy + vec.y * params['target_radius']
                    mesh.vertex_attributes(v, 'xyz', [new_x, new_y, WALKWAY_Z])
                    fixed_vertices.add(v)
                    break

# =============================================================================
# 4. 平滑鬆弛 + 自然疊加波海浪
# =============================================================================
for i in range(180):
    updates = {}
    for v in mesh.vertices():
        if v in fixed_vertices: continue
        nbrs = [mesh.vertex_coordinates(n) for n in mesh.vertex_neighbors(v)]
        if not nbrs: continue
        cx, cy, cz = cg.centroid_points(nbrs)
        px, py, pz = mesh.vertex_coordinates(v)
        
        # 疊加波浪
        wave1 = 1.8 * math.sin(0.35 * px + 0.5 * py)
        wave2 = 0.6 * math.cos(0.9 * px + 1.1 * py)
        target_z = wave1 + wave2
        
        updates[v] = [
            px + 0.5 * (cx - px),
            py + 0.5 * (cy - py),
            pz + 0.4 * (cz - pz) + (target_z - pz) * 0.12
        ]
        
    for v, xyz in updates.items():
        mesh.vertex_attributes(v, "xyz", xyz)

# =============================================================================
# 5. Remesh 與色彩渲染
# =============================================================================
V, F = mesh.to_vertices_and_faces()
V, F = trimesh_remesh((V, F), 0.45, 20, True)
final_mesh = Mesh.from_vertices_and_faces(V, F)

z_values = [final_mesh.vertex_attribute(v, 'z') for v in final_mesh.vertices()]
z_min, z_max = min(z_values), max(z_values)
for v in final_mesh.vertices():
    z = final_mesh.vertex_attribute(v, 'z')
    ratio = (z - z_min) / (z_max - z_min) if z_max != z_min else 0
    final_mesh.vertex_attribute(v, 'color', Color.from_i(ratio).rgb)

# =============================================================================
# 6. 輸出建模檔至桌面
# =============================================================================
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "Organic_Wave_Corridor.obj")
final_mesh.to_obj(file_path)
print(f"成功輸出建模檔至桌面: {file_path}")

# =============================================================================
# 7. 視覺化
# =============================================================================
viewer = Viewer()
viewer.scene.add(final_mesh, name="Organic_Columns_Model", show_lines=True)
viewer.show()