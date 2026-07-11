import os
import re
import time
import requests
import subprocess
import uuid
from seleniumwire import webdriver
from selenium.webdriver.edge.options import Options

# --- 1. Modular Configuration ---
print("=== 🚀 Universal Stream Archiver Suite (Generic Interceptor) ===")

def clean_name(name):
    """Sanitize folder and file names for OS compatibility."""
    # 移除或取代 OS 檔案系統不允許的字元
    for char in '<>:"/\\|?*':
        name = name.replace(char, "_")
    return name.strip()

def intercept_stream_urls(target_url):
    """Launch browser to load target page and intercept streaming and subtitle URLs."""
    script_dir = os.getcwd()
    automation_user_data = os.path.join(script_dir, "automation_profile")
    
    options = Options()
    options.add_argument(f"--user-data-dir={automation_user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--mute-audio")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    wire_options = {'auto_config': True, 'verify_ssl': False}
    
    print("\n🌐 正在啟動瀏覽器載入網頁...")
    driver = webdriver.Edge(options=options, seleniumwire_options=wire_options)
    
    m3u8_url, vtt_url = None, None
    m3u8_candidates = []
    page_title = "downloaded_video"
    
    try:
        driver.get(target_url)
        # 取得網頁 Title 並清理作為預設檔名
        raw_title = driver.title or "video"
        page_title = clean_name(raw_title)
        print(f"🎬 已載入網頁: {page_title}")
        print("💡 正在監聽網路請求。若影片未自動播放，請手動點擊瀏覽器中的播放按鈕。")
        
        start_time = time.time()
        timeout = 45  # 設定較寬裕的 45 秒超時
        
        while (time.time() - start_time < timeout):
            # 遍歷攔截到的 requests
            for request in driver.requests:
                if request.response:
                    url = request.url
                    # 偵測 HLS 串流
                    if '.m3u8' in url:
                        if url not in m3u8_candidates:
                            m3u8_candidates.append(url)
                    # 偵測 WebVTT 字幕
                    if '.vtt' in url and not vtt_url:
                        vtt_url = url
            
            # 若已攔截到 m3u8，且其中包含常見的高解析度特徵，可提前結束
            if any("1080" in u for u in m3u8_candidates):
                break
                
            time.sleep(1)
            
        if m3u8_candidates:
            # 優先篩選 1080p -> 720p -> 其他
            m3u8_url = next((u for u in m3u8_candidates if "1080" in u), None) or \
                       next((u for u in m3u8_candidates if "720" in u), None) or \
                       m3u8_candidates[0]
                       
        return m3u8_url, vtt_url, page_title
    except Exception as e:
        print(f"❌ 攔截串流時發生錯誤: {e}")
        return None, None, page_title
    finally:
        driver.quit()

def download_worker(task):
    """FFmpeg background worker with GPU acceleration."""
    m3u8, vtt, folder, title = task
    os.makedirs(folder, exist_ok=True)
    video_path = os.path.join(folder, f"{title}.mp4")
    
    if os.path.exists(video_path):
        return f"✅ 影片已存在，跳過下載: {video_path}"
        
    print(f"📥 開始下載影片: {title}")
    
    # 產生具備 UUID 的唯一字幕暫存檔，防止多工衝突
    temp_vtt = f"temp_{uuid.uuid4().hex[:8]}.vtt"
    try:
        if vtt:
            print(f"💬 偵測到字幕檔，正在下載字幕: {vtt}")
            r = requests.get(vtt)
            r.raise_for_status()
            with open(temp_vtt, "wb") as f:
                f.write(r.content)
            
        # 建立 FFmpeg 下載指令，預設啟用 NVIDIA GPU 硬體加速 (CUDA + h264_nvenc)
        cmd = ['ffmpeg', '-y', '-hwaccel', 'cuda', '-i', m3u8]
        
        if vtt and os.path.exists(temp_vtt):
            # 處理 Windows 檔案路徑中冒號與反斜線在 subtitles 濾鏡中的跳脫問題
            vtt_fixed = temp_vtt.replace("\\", "/").replace(":", "\\:")
            cmd += ['-vf', f"subtitles={vtt_fixed}:force_style='FontSize=18,BackColor=&H80000000,BorderStyle=4,Outline=0'"]
            
        cmd += [
            '-c:v', 'h264_nvenc', '-preset', 'p4', 
            '-c:a', 'aac', '-b:a', '192k', 
            video_path
        ]
        
        # 啟動 FFmpeg 進行下載，背景執行
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                       creationflags=0x08000000 if os.name == 'nt' else 0)
                       
        if os.path.exists(video_path):
            return f"✨ 下載完成: {video_path}"
        else:
            # 降級備份：若 NVIDIA GPU 加速失敗（可能無對應顯示卡），嘗試使用 CPU 進行下載
            print("⚠️ GPU 加速下載失敗，嘗試使用 CPU 重新下載...")
            cpu_cmd = ['ffmpeg', '-y', '-i', m3u8]
            if vtt and os.path.exists(temp_vtt):
                vtt_fixed = temp_vtt.replace("\\", "/").replace(":", "\\:")
                cpu_cmd += ['-vf', f"subtitles={vtt_fixed}:force_style='FontSize=18,BackColor=&H80000000,BorderStyle=4,Outline=0'"]
            cpu_cmd += [
                '-c:v', 'libx264', '-preset', 'fast', 
                '-c:a', 'aac', '-b:a', '192k', 
                video_path
            ]
            subprocess.run(cpu_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                           creationflags=0x08000000 if os.name == 'nt' else 0)
            if os.path.exists(video_path):
                return f"✨ 下載完成 (CPU 備援): {video_path}"
            else:
                return f"❌ 下載失敗: 無法使用 FFmpeg 產生 MP4 檔案。"
    except Exception as e:
        return f"❌ 下載出錯: {title} ({e})"
    finally:
        if os.path.exists(temp_vtt): 
            try:
                os.remove(temp_vtt)
            except:
                pass

def main():
    while True:
        print("\n--- 功能選單 ---")
        print("1. 輸入網址攔截並下載影片與字幕")
        print("2. 離開")
        choice = input("👉 請選擇功能 (1-2): ").strip()
        
        if choice == '1':
            url = input("🔗 請貼上影片網頁網址: ").strip()
            if not url:
                print("⚠️ 網址不可為空。")
                continue
                
            m3u8, vtt, title = intercept_stream_urls(url)
            if m3u8:
                print(f"\n🎯 攔截成功！")
                print(f"🎥 串流網址: {m3u8}")
                if vtt:
                    print(f"💬 字幕網址: {vtt}")
                print(f"📂 預設檔名: {title}")
                
                # 讓使用者可自訂檔名，按 Enter 鍵則保留預設值
                custom_title = input(f"📝 請輸入儲存檔名 (直接按 Enter 使用預設標題): ").strip()
                final_title = clean_name(custom_title) if custom_title else title
                
                # 執行下載
                result = download_worker((m3u8, vtt, "downloads", final_title))
                print(result)
            else:
                print("❌ 攔截失敗：超時或在網頁中未偵測到 .m3u8 串流。")
        elif choice == '2' or choice.lower() == 'exit':
            print("👋 感謝使用，再見！")
            break
        else:
            print("⚠️ 無效的選擇。")

if __name__ == "__main__":
    main()
