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

## 🛠️ Quick Start & Prerequisites
Please refer to the [Customization Guide](#-customization-guide) before running the tool on different platforms.

1. **Install Dependencies**:
   pip install selenium-wire requests tqdm
   
2. Download Edge WebDriver (Crucial):

   Check your Edge browser version: Settings > About Microsoft Edge.

   Download the matching driver from Microsoft Edge Driver Official Site.

   Place the msedgedriver.exe file in the same folder as unified_archiver_tool.py.

3. Setup FFmpeg: Ensure FFmpeg with CUDA support is installed and added to your system PATH.

4. Run:
  python unified_archiver_tool.py

🔍 Customization Guide
To adapt this tool for your specific target website, update the following in unified_archiver_tool.py:
1. Update Base URLs & Domain
   At the top of the script, modify the BASE_URL and API path variables. This is the most critical step for adapting to other sites:

   ### Change these values to your target platform
      1).BASE_URL = "https://your-target-site.com"
   
      2.)API_PATH = f"{BASE_URL}/api/v2/path/to/content"
   
3. Adjust JSON Structure
   The function get_course_structure() parses the website's API. Since different sites use different JSON keys, you must update the mapping:

   Item ID: Change item.get('programContentId') to match the ID key of your platform.

   Folder Name: Change d.get('contentSectionTitle') to the key representing categories/sections.

   File Name: Change d.get('title') to the key representing the lesson title.
4. URL Interception Logic
   In capture_urls_via_listening(), the script filters network traffic for .m3u8 and .vtt. If your platform uses different file extensions or unique query parameters (like token= instead of Signature=), update the filter conditions there.

🔍 How to Obtain Session Credentials
The tool mimics an authenticated session using credentials from your browser's Developer Tools (F12):

Target ID: The unique identifier found in the URL of the content (e.g., .../programs/**target-id-123**).

Authorization Bearer Token: Found in the Network tab under Request Headers (copy the string after Bearer ).

⚙️ Phase Execution Logic
To prevent a messy console output, the tool executes in two distinct phases:

Phase 1 (Capture): Browsers open one-by-one to intercept links.

Tip: If a capture hangs, press F5 in the pop-up browser to refresh the stream.

Phase 2 (Download): Once all links are gathered, the background GPU engine starts. A single consolidated tqdm progress bar tracks the overall status.

⚖️ Disclaimer
This software is provided for personal educational backup only. Users are responsible for complying with the Terms of Service of their respective platforms.
