# 🚀 Universal Stream Archiver Suite (Visual Edition)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GPU: NVIDIA](https://img.shields.io/badge/GPU-NVIDIA%20NVENC-green)](https://developer.nvidia.com/video-codec-sdk)

A high-performance toolkit for archiving M3U8 video streams. It features an integrated menu for batch processing or targeted patching, optimized for NVIDIA GPU acceleration.

## ✨ Key Features
- **Two-Phase Workflow**: Sequential URL capture followed by parallel GPU downloading for a clean UI.
- **Hardware Acceleration**: High-speed encoding using NVIDIA NVENC (`h264_nvenc`).
- **Smart Quality Detection**: Prioritizes 1080p/720p streams automatically.
- **Compatibility**: Burned subtitles (.vtt) and standardized AAC 192kbps audio.

## 🛠️ Quick Start
Please refer to the [Customization Guide](#-customization-guide) before running the tool on different platforms.

1. **Install Dependencies**:
   pip install selenium-wire requests tqdm
   
3. Setup FFmpeg: Ensure FFmpeg with CUDA support is in your system PATH.

4. Run:
  python unified_archiver_tool.py

🔍 Customization Guide
  To adapt this tool for your specific target website, update the following in unified_archiver_tool.py:

  BASE_URL: The root domain of the platform.

  API_PATH: The endpoint structure for fetching course contents.

  JSON Keys: Update programContentId, contentSectionTitle, and title to match the target API's response keys.

⚖️ Disclaimer
This software is provided for personal educational backup only. Users are responsible for complying with the Terms of Service of their respective platforms.
