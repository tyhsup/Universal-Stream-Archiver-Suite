# 🚀 Universal Stream Archiver Suite (Generic Interceptor Edition)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GPU: NVIDIA](https://img.shields.io/badge/GPU-NVIDIA%20NVENC-green)](https://developer.nvidia.com/video-codec-sdk)

A high-performance, generic toolkit for archiving M3U8 video streams and WebVTT subtitles. It captures streaming traffic dynamically in the background using Selenium Wire, removing the need for platform-specific APIs or manual credential tokens. Just load any video page, play the video, and the tool handles the rest automatically.

---

## ✨ Key Features

- **Generic Stream Interception**: Supports any video streaming website. Simply enter the webpage URL, play the video, and the program will automatically capture the `.m3u8` playlist and `.vtt` subtitle files.
- **Auto-Title Detection & Sanitization**: Dynamically retrieves the webpage title (`driver.title`) as the default filename and automatically strips OS-forbidden characters (e.g., `<>:"/\\|?*`). You can also customize the filename before downloading.
- **Hardware Acceleration with CPU Fallback**:
  - Uses NVIDIA GPU hardware acceleration (`h264_nvenc`) by default for ultra-fast transcoding and subtitle burning.
  - Automatically falls back to **CPU encoding** (`libx264`) if no NVIDIA GPU is detected or if CUDA drivers fail, ensuring maximum compatibility.
- **Automatic Subtitle Burn-In**: Downloads WebVTT subtitles if available and automatically hard-burns them into the output MP4 file using FFmpeg filters.

---

## 🛠️ Quick Start & Prerequisites

### 1. Install Dependencies
It is highly recommended to set up a Python virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

> 💡 **Dependency Notes**:
> The `blinker` library is locked to `1.7.0` and `pyOpenSSL` is locked to `23.2.0` (with `cryptography == 41.0.7`) to bypass package deprecation conflicts with `selenium-wire` / `mitmproxy`.

### 2. Download Edge WebDriver
1. Check your Microsoft Edge version (Settings > About Microsoft Edge).
2. Download the matching driver from the [Microsoft Edge Driver Site](https://developer.microsoft.com/microsoft-edge/tools/webdriver/).
3. Extract and place the `msedgedriver.exe` file inside the same root folder as `unified_archiver_tool.py`.

### 3. Setup FFmpeg
Ensure `ffmpeg` is installed on your system and added to your system environment variables (`PATH`).

### 4. Run the Tool
Execute the following command within the virtual environment:
```powershell
& .venv\Scripts\python.exe unified_archiver_tool.py
```

---

## ⚙️ How It Works

1. **Option Selection**: Start the script, type `1`, and paste the target video webpage URL.
2. **Page Loading & Capture**: The script launches the browser. If the video does not auto-play, **manually click play** in the browser to trigger the stream requests.
3. **Automatic Interception**: Once the `.m3u8` stream is successfully intercepted, the browser window will close automatically.
4. **Filename Confirmation & Download**: The terminal will prompt you for an optional custom filename. Press `Enter` to use the webpage title. The program will then download and burn subtitles using FFmpeg. All downloaded videos are saved in the `downloads/` directory.

---

## ⚖️ Disclaimer

This software is provided for personal educational backup purposes only. Users are responsible for complying with the Terms of Service and Copyright regulations of their respective platforms. The authors are not responsible for any misuse of this tool.
