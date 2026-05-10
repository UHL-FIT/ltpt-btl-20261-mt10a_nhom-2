import customtkinter as ctk
import tkinter.messagebox as messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Khởi động...")
        self.geometry("400x250")
        # Ẩn thanh tiêu đề
        self.overrideredirect(True)
        
        # Căn giữa màn hình
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        self.configure(fg_color="#1e1e24")
        
        # Title
        self.label_title = ctk.CTkLabel(self, text="Real-time Currency Tracker Pro", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00ffcc")
        self.label_title.pack(pady=(60, 20))
        
        # Loading
        self.label_loading = ctk.CTkLabel(self, text="Đang tải dữ liệu...", font=ctk.CTkFont(size=14))
        self.label_loading.pack()
        
        self.progressbar = ctk.CTkProgressBar(self, width=300, progress_color="#00ffcc")
        self.progressbar.pack(pady=20)
        self.progressbar.set(0)
        self.progressbar.start()
        
        # Tránh việc user tắt bằng alt+f4
        self.protocol("WM_DELETE_WINDOW", lambda: None)

class AddPairWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Thêm cặp tiền tệ")
        self.geometry("350x250")
        self.resizable(False, False)
        
        # Căn giữa so với parent
        self.transient(parent)
        self.grab_set()
        
        self.label_base = ctk.CTkLabel(self, text="Tiền tệ gốc (Ví dụ: USD):", font=ctk.CTkFont(weight="bold"))
        self.label_base.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.entry_base = ctk.CTkEntry(self, placeholder_text="Mã ISO (USD, EUR...)")
        self.entry_base.pack(pady=5, padx=20, fill="x")
        
        self.label_target = ctk.CTkLabel(self, text="Tiền tệ đích (Ví dụ: VND):", font=ctk.CTkFont(weight="bold"))
        self.label_target.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.entry_target = ctk.CTkEntry(self, placeholder_text="Mã ISO (VND, JPY...)")
        self.entry_target.pack(pady=5, padx=20, fill="x")
        
        self.btn_save = ctk.CTkButton(self, text="Lưu", command=self.save, fg_color="#28a745", hover_color="#218838")
        self.btn_save.pack(pady=20)
        
    def save(self):
        base = self.entry_base.get().strip().upper()
        target = self.entry_target.get().strip().upper()
        
        if not base or not target:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ mã tiền tệ.")
            return
            
        if len(base) != 3 or len(target) != 3:
            messagebox.showwarning("Lỗi", "Mã tiền tệ ISO phải có 3 ký tự.")
            return
            
        success, message = self.controller.add_pair(base, target)
        if success:
            messagebox.showinfo("Thành công", message)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message)

class ChartWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, base, target):
        super().__init__(parent)
        self.db = db
        self.base = base
        self.target = target
        
        self.title(f"Biểu đồ biến động: {base}/{target}")
        self.geometry("800x600")
        
        plt.style.use('dark_background')
        
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        self.draw_chart()
        
    def draw_chart(self):
        self.ax.clear()
        df = self.db.get_history_dataframe(self.base, self.target)
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center', fontsize=14)
        else:
            self.ax.plot(df['timestamp'], df['rate'], marker='o', linestyle='-', color='#00ffcc')
            self.ax.set_title(f"Tỷ giá {self.base}/{self.target} theo thời gian", color='white')
            self.ax.set_xlabel("Thời gian", color='white')
            self.ax.set_ylabel("Tỷ giá", color='white')
            self.ax.tick_params(colors='white')
            
            # Format X axis để xoay nhãn
            self.figure.autofmt_xdate()
            self.ax.grid(True, linestyle='--', alpha=0.3)
            
        self.canvas.draw()
