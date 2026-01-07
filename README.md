#設計概念

配合大二設計之公園與綠園道，創造一個可供行人與居民通行的連接廊道。

#生成邏輯

參考Caret 6 (SXSW)之形狀，更改mesh pavilion的程式碼，調整開口與形狀，做出參數化拱頂。

＃環境安裝

1.下載Aniconda/Miniconda
    Miniconda:[下載](https://www.anaconda.com/docs/getting-started/miniconda/main)
    Aniconda:[下載](https://www.anaconda.com/)

2.安裝COMPUS資料庫

    開啟Anaconda Powershell Prompt (miniconda3) (Windows), or Powershell (Windows), or Terminal (macOS).

    首先，我們將 **conda**-forge 新增為 **conda** 取得套件的來源（channel）。這個設定在每台電腦上只需要做一次即可。

    **conda config --add channels conda-forge**
    如果該指令沒有回傳任何內容，表示該 channel 已成功加入。
    conda create -n DCCG python=3.9.10 compas pyside6
        y
    conda activate DCCG
    pip install compas_viewer
        y
