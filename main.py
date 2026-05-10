<<<<<<< HEAD
"""
main.py
=======
Khởi chạy ứng dụng "SmartAttend".
Thiết kế theo mô hình MVC sử dụng modules (không dùng class).

Phase 1: Giao diện CLI (Command Line Interface)
Phase 2: Nâng cấp lên GUI (Tkinter) — chỉ thay View + Controller, giữ nguyên Model.
"""

import sys
from utils.logger import setup_logger

__version__ = "1.0.0"
logger = setup_logger("main")

# Ép console sử dụng UTF-8 khi chạy file .exe để tránh lỗi UnicodeEncodeError
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from controllers import gui_controller
from controllers import cli_controller

if __name__ == "__main__":
    logger.info(f"=== Khởi chạy SmartAttend v{__version__} (Chế độ mặc định) ===")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        logger.info("Chuyển sang giao diện dòng lệnh (CLI) qua tham số.")
        cli_controller.chay_ung_dung()
    else:
        logger.info("Khởi động giao diện đồ hoạ (GUI).")
        gui_controller.chay_ung_dung()
=======
import customtkinter as ctk
from views.components import SplashScreen
from controllers.app_controller import AppController
import time

def main():
    # Khởi tạo cửa sổ root tạm thời cho SplashScreen
    root = ctk.CTk()
    root.withdraw() # Ẩn cửa sổ chính
    
    # Hiển thị SplashScreen
    splash = SplashScreen(root)
    root.update()
    
    # Giả lập thời gian load các module (hoặc có thể load thật ở đây)
    for i in range(101):
        time.sleep(0.01) # Fake loading
        splash.progressbar.set(i/100)
        root.update()
        
    time.sleep(0.5)
    
    # Đóng SplashScreen
    splash.destroy()
    root.destroy()
    
    # Khởi chạy Controller chính
    ctk.set_appearance_mode("Dark")  # Mặc định Dark mode
    ctk.set_default_color_theme("blue")
    
    app = AppController()
    try:
        app.start()
    except Exception as e:
        print(f"Lỗi khi khởi chạy ứng dụng: {e}")
    finally:
        app.stop()

if __name__ == "__main__":
    main()
>>>>>>> 80c8985 (Hoan thanh project Real-time Currency Tracker Pro)
