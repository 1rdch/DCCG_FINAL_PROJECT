#設計概念

配合大二設計之公園與綠園道，創造一個可供行人與居民通行的連接廊道。

#生成邏輯

參考Caret 6 (SXSW)之形狀，更改mesh pavilion的程式碼，調整開口與形狀，做出參數化拱頂。

＃環境安裝

1.下載Aniconda/Miniconda
    
Miniconda: [下載](https://www.anaconda.com/docs/getting-started/miniconda/main)
Aniconda:[下載](https://www.anaconda.com/)

2.安裝COMPUS資料庫

開啟Anaconda Powershell Prompt (miniconda3) (Windows), or Powershell (Windows), or Terminal (macOS).

首先，我們將 conda-forge 新增為 **conda** 取得套件的來源（channel）。這個設定在每台電腦上只需要做一次即可。

    conda config --add channels conda-forge
如果該指令沒有回傳任何內容，表示該 channel 已成功加入。

接下來，為這門課程建立一個新的環境，並且在此**明確指定 Python 版本為 3.9.10**，這個版本正是 **Rhino 8 隨附的 Python 版本**。

    conda create -n DCCG python=3.9.10 compas pyside6
回答**y**以繼續執行

（註：截至 **2025 年 10 月**，需要**明確安裝 pyside6**，才能讓 **compas_viewer** 透過 pip 正確安裝。）

完成後，請啟用（activate）該環境，這樣我們才能在其中安裝套件。

    conda activate DCCG

當環境被啟用後，**環境名稱會顯示在指令提示字元前方**。在這個例子中是 **(DCCG)**。接著請繼續安裝 **COMPAS_viewer**：

    pip install compas_viewer

這些步驟可能需要一點時間。過程中你可能會看到像這樣的警告，這是因為我們使用的某些模組尚未是穩定版本。當系統提示時，請輸入 y 以繼續。     

安裝完成。

