**專案名稱：** 2022 Autonomous Field Robot

**簡介**
- 本專案為 2022 年校園場域自主機器人競賽作品，整合影像辨識、Arduino 控制與序列通訊，目標為在田間路徑/色牌/水果辨識任務中自動導航與操作。

**目錄概覽**
- `Main/`：主要控制程式、各版本 (`Main_v6` ~ `Main_v10_Final`) 與影像辨識模組（`color_sign_recog.py`, `fruit_recog.py`）。
- `Main_v10_Final/`：最接近最終整合的版本，含 `Main_Final.py` 與對應的 Arduino 程式 `Main_v10_Final.ino`。
- `Integrated_Test/`：整合測試範例與 Sign_IT 測試程式。
- `Tool/`：輔助工具，例如擷取影像、灰階處理等。
- `Tracking/`：追蹤車相關 Arduino 程式與控制草稿。
- `Test/`：各種小型硬體測試（Servo、Relay、RGB LED、灌溉等）。

**主要技術與套件**
- 程式語言：`Python`、`C/C++`（Arduino）
- 影像處理：`OpenCV`、`numpy`
- 序列通訊：`pyserial`（Python 與 Arduino 間通訊）
- 開發環境：Ubuntu / Arduino IDE

**主要模組與檔案（精要）**
- `Main/Main_Final.py`：總控制流程範例（請參考 `Main_v10_Final/Main_Final.py` 作為最終整合參考）。
- `Main_v10_Final/Main_Final.py`：最終整合的 Python 控制程式。
- `Main_v10_Final/Main_v10_Final.ino`：對應的 Arduino 韌體。
- `Main/color_sign_recog.py`：色牌（標誌）辨識模組。
- `Main/fruit_recog.py`：水果辨識模組。
- `Main/arduino_util.cpp`、`Main/arduino_util.h`：PC/Arduino 的通訊與控制輔助函式（在多個子目錄出現以支援不同版本）。
- `Integrated_Test/Sign_IT/Sign_IT.py`：標誌辨識整合測試腳本。
- `Tool/takePictures.py`：擷取影像的工具腳本。

（工作檔案請參考倉庫中各資料夾內容）

**快速上手（執行範例）**
1. 建立 Python 虛擬環境並安裝相依套件：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # 若無 requirements.txt，至少安裝: opencv-python numpy pyserial
```

2. 執行最終整合範例（在裝置連接且 Arduino 已燒錄對應韌體下）：

```bash
cd Main_v10_Final
python3 Main_Final.py
```

3. 若要測試相機或影像模組，可執行：

```bash
python3 Tool/takePictures.py
python3 Main/color_sign_recog.py
python3 Main/fruit_recog.py
```

**Arduino（硬體）說明**
- Arduino 程式分散在多個資料夾（`Main/Arduino_Main_v*`、`Main_v6/Arduino_Main_v6`、`Main_v10_Final` 等），上傳前請在 Arduino IDE 選擇正確板子與 COM 埠。
- `arduino_util.cpp` / `arduino_util.h` 提供馬達、伺服、感測器等控制輔助函式。

**成果與測試報告（摘要）**
- 完成項目：色牌辨識、簡易水果辨識、序列通訊整合、多版 Arduino 韌體樣本、若干硬體測試程式。
- 可改進處：模型/演算法參數最佳化、辨識在不同光照與背景下的穩健度提升、控制迴路（PID）調校。

**開發與貢獻**
- 若要加入或修改：Fork → 建分支 → 發 PR。請在 PR 中描述變更、測試案例與執行方式。

**後續建議**
- 補上 `requirements.txt`（列出 `opencv-python`, `numpy`, `pyserial` 等），並在 `Main_v10_Final` 加入範例配置檔與更詳盡的執行說明。
- 可將常用的 Arduino 與 Python 通訊協定（payload 格式）書面化為 `docs/protocol.md`。

**聯絡**
- 若有問題或需要協助，請於專案內提出 Issue。

---
（此 README 由專案自動遍歷後重寫，僅作總覽；如需更細的執行腳本或測試報告，可指定我進一步生成。）
