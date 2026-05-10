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
