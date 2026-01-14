import os
import time
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from seleniumwire import webdriver
from selenium.webdriver.edge.options import Options

# --- 1. Modular Configuration ---
print("=== 🚀 Universal Stream Archiver Suite (Fixed Version) ===")

BASE_URL = "https://your-target-site.com"
API_PATH = f"{BASE_URL}/api/v2/programs"

TARGET_ID = input("🔑 Please enter Target ID (Program ID): ").strip()
BEARER_TOKEN = input("🔑 Please enter Bearer Token: ").strip()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Authorization": f"Bearer {BEARER_TOKEN}",
}

def clean_name(name):
    """Sanitize folder and file names for OS compatibility."""
    for char in '<>:"/\\|?*': name = name.replace(char, "_")
    return name.strip()

def get_course_structure():
    """Fetch the full course hierarchy via API."""
    list_url = f"{API_PATH}/{TARGET_ID}/contents"
    try:
        r = requests.get(list_url, headers=HEADERS)
        r.raise_for_status()
        id_list = r.json()
        structure = []
        print(f"📡 Scanning course list from API...")
        for item in id_list:
            c_id = item.get('programContentId') 
            res = requests.get(f"{list_url}/{c_id}", headers=HEADERS)
            d = res.json()
            if d.get('contentBodyId'):
                structure.append({
                    'id': c_id,
                    'folder': clean_name(d.get('contentSectionTitle') or "Uncategorized"),
                    'title': clean_name(d.get('title', 'Untitled'))
                })
        return structure
    except Exception as e:
        print(f"❌ Failed to fetch list: {e}")
        return []

def capture_urls_via_listening(unit):
    """Launch browser to intercept URLs."""
    # Using getcwd() to be compatible with all execution environments
    script_dir = os.getcwd()
    automation_user_data = os.path.join(script_dir, "automation_profile")
    
    options = Options()
    options.add_argument(f"--user-data-dir={automation_user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--mute-audio")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    wire_options = {'auto_config': True, 'verify_ssl': False}
    # If you use Chrome, change this to webdriver.Chrome
    driver = webdriver.Edge(options=options, seleniumwire_options=wire_options)
    
    m3u8_url, vtt_url = None, None
    m3u8_candidates = []

    try:
        target_url = f"{BASE_URL}/programs/{TARGET_ID}/contents/{unit['id']}"
        driver.get(target_url)
        print(f"🎬 Intercepting: {unit['title']}")
        
        start_time = time.time()
        while (time.time() - start_time < 60):
            for request in driver.requests:
                if request.response:
                    url = request.url
                    if '.m3u8' in url:
                        if url not in m3u8_candidates: m3u8_candidates.append(url)
                    if '.vtt' in url and not vtt_url: vtt_url = url
            
            if any("1080" in u for u in m3u8_candidates): break
            time.sleep(1)

        if m3u8_candidates:
            m3u8_url = next((u for u in m3u8_candidates if "1080" in u), None) or \
                       next((u for u in m3u8_candidates if "720" in u), None) or \
                       m3u8_candidates[0]
        return m3u8_url, vtt_url
    finally:
        driver.quit()

def download_worker(task):
    """FFmpeg background worker with GPU acceleration."""
    m3u8, vtt, folder, title = task
    os.makedirs(folder, exist_ok=True)
    video_path = os.path.join(folder, f"{title}.mp4")
    
    if os.path.exists(video_path): return f"✅ Skipping {title}"

    # Unique temporary VTT to avoid conflicts in multi-threading
    temp_vtt = f"temp_{int(time.time())}_{abs(hash(title)) % 1000}.vtt"
    try:
        if vtt:
            r = requests.get(vtt)
            with open(temp_vtt, "wb") as f: f.write(r.content)
            
        cmd = ['ffmpeg', '-y', '-hwaccel', 'cuda', '-i', m3u8]
        if vtt and os.path.exists(temp_vtt):
            vtt_fixed = temp_vtt.replace("\\", "/").replace(":", "\\:")
            cmd += ['-vf', f"subtitles={vtt_fixed}:force_style='FontSize=18,BackColor=&H80000000,BorderStyle=4,Outline=0'"]
        
        cmd += [
            '-c:v', 'h264_nvenc', '-preset', 'p4', 
            '-c:a', 'aac', '-b:a', '192k', 
            video_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                       creationflags=0x08000000 if os.name == 'nt' else 0)
        return f"✨ Finished: {title}"
    except Exception as e: return f"❌ Error: {title} ({e})"
    finally:
        if os.path.exists(temp_vtt): 
            try: os.remove(temp_vtt)
            except: pass

def process_batch_download(unit_list):
    """Sequential Capture then Parallel Download."""
    captured_tasks = []
    
    print(f"\n--- Phase 1: Capturing URLs ({len(unit_list)} units) ---")
    for unit in unit_list:
        m3u8, vtt = capture_urls_via_listening(unit)
        if m3u8:
            captured_tasks.append((m3u8, vtt, unit['folder'], unit['title']))
        else:
            print(f"⚠️ Capture Failed for: {unit['title']}")

    if captured_tasks:
        print(f"\n--- Phase 2: Starting Parallel GPU Download ---")
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(tqdm(executor.map(download_worker, captured_tasks), 
                                total=len(captured_tasks), 
                                desc="Overall Progress"))
            for res in results: print(res)

# --- Main Logic ---
course_units = get_course_structure()
if course_units:
    print(f"\n✅ Total units loaded: {len(course_units)}")
    while True:
        print("\n--- Main Menu ---")
        print("1. Download ALL units")
        print("2. Search & Download specific unit")
        print("3. Exit")
        choice = input("👉 Select an option (1-3): ").strip()

        if choice == '1':
            process_batch_download(course_units)
        elif choice == '2':
            search_key = input("🔍 Enter lesson name keyword: ").strip()
            matches = [u for u in course_units if search_key.lower() in u['title'].lower()]
            if not matches:
                print("❓ No matching results.")
            else:
                for idx, match in enumerate(matches):
                    print(f"  [{idx+1}] {match['title']}")
                sel = input("👉 Select number (or Enter to cancel): ")
                if sel.isdigit() and 1 <= int(sel) <= len(matches):
                    process_batch_download([matches[int(sel)-1]])
        elif choice == '3' or choice.lower() == 'exit':
            break

