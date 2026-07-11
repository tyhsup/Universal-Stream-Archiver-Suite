# 🚀 Universal Stream Archiver Suite (Generic Interceptor Edition)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GPU: NVIDIA](https://img.shields.io/badge/GPU-NVIDIA%20NVENC-green)](https://developer.nvidia.com/video-codec-sdk)

一個高效且通用的網頁串流影音（M3U8）與字幕（WebVTT）自動攔截與下載工具。本工具透過 Selenium Wire 在背景監聽網路請求，不需依賴任何特定網站的 API 或登入驗證，只要網頁中播放影片，即可自動提取串流網址並調用 FFmpeg 進行下載。

---

## ✨ 核心特色

- **通用網頁影音攔截**：支援任意影音網站。貼上影片網頁網址，播放影片後程式即可自動捕獲 `.m3u8` 與 `.vtt` 字幕。
- **自動檔名擷取**：自動以網頁標題（`driver.title`）作為下載預設檔名，並自動清理 OS 不支援的特殊字元，亦支援下載前手動修改檔名。
- **硬體加速與 CPU 自動降級雙保險**：
  - 預設啟用 NVIDIA GPU 硬體加速（`h264_nvenc`）以進行超高速的轉碼與字幕燒錄。
  - 若系統無 NVIDIA 顯卡或 CUDA 驅動有誤，程式會**自動降級切換至 CPU 解碼**（`libx264`），確保在任何環境下皆能完成下載。
- **字幕自動燒錄**：若偵測到 WebVTT 字幕，程式會下載並在 FFmpeg 輸出時自動燒錄至 MP4 影片中。

---

## 🛠️ 快速開始與環境建置

### 1. 安裝 Python 依賴套件
推薦建立 Python 虛擬環境並安裝 `requirements.txt`：
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

> 💡 **相容性說明**：
> 本專案已將 `blinker` 鎖定在 `1.7.0`，並將 `pyOpenSSL` 鎖定在 `23.2.0`（cryptography == 41.0.7），以完美解決新版套件與 `selenium-wire` / `mitmproxy` 之間的 API 廢棄衝突。

### 2. 下載 Edge WebDriver
1. 查看您電腦的 Edge 瀏覽器版本（設定 > 關於 Microsoft Edge）。
2. 至 [Microsoft Edge Driver 官網](https://developer.microsoft.com/microsoft-edge/tools/webdriver/) 下載相同版本的驅動程式。
3. 將解壓縮出的 `msedgedriver.exe` 放置在與 `unified_archiver_tool.py` 相同的專案目錄下。

### 3. 設定 FFmpeg
請確保您的系統已安裝 `ffmpeg`，且已將其執行檔路徑加入至系統環境變數（`PATH`）中。

### 4. 執行工具
在虛擬環境中執行以下指令：
```powershell
& .venv\Scripts\python.exe unified_archiver_tool.py
```

---

## ⚙️ 執行流程與使用說明

1. **選擇功能**：啟動後輸入 `1`，並貼上您想下載影片的網頁網址。
2. **網頁載入與監聽**：程式會啟動瀏覽器載入網頁。如果影片沒有自動播放，**請手動在瀏覽器中點擊播放**。
3. **攔截與自動關閉**：一旦背景成功攔截到 `.m3u8` 串流，程式會自動關閉瀏覽器。
4. **確認檔名與下載**：終端機將提示您是否需要修改檔名，按 `Enter` 則採用預設網頁標題。接著程式會自動調用 FFmpeg 進行下載與字幕燒錄。所有下載檔案將儲存至專案目錄下的 `downloads/` 資料夾。

---

## ⚖️ 免責聲明

本軟體僅供個人學術研究、教育、或是個人備份之用。請勿用於任何商業用途。使用者下載他人影片時，需自行遵守該影音平台之使用者協議與著作權法規，作者與本專案不承擔任何法律責任。
