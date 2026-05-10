import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from views.components import AddPairWindow, ChartWindow
import os
import subprocess
import sys

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title("Real-time Currency Tracker Pro")
        self.geometry("1100x700")
        
        # Thiết lập grid layout 1x2 (1 hàng, 2 cột)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._create_sidebar()
        self._create_main_content()
        
    def _create_sidebar(self):
        # Frame sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Đẩy nút dưới cùng xuống
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Currency Tracker", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00ffcc")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        self.btn_add = ctk.CTkButton(self.sidebar_frame, text="Thêm cặp tiền tệ", command=self.open_add_pair_window)
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_remove = ctk.CTkButton(self.sidebar_frame, text="Xóa cặp đã chọn", command=self.remove_selected, fg_color="#dc3545", hover_color="#c82333")
        self.btn_remove.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_chart = ctk.CTkButton(self.sidebar_frame, text="Xem biểu đồ", command=self.open_chart_window)
        self.btn_chart.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_export = ctk.CTkButton(self.sidebar_frame, text="Xuất CSV", command=self.export_csv)
        self.btn_export.grid(row=4, column=0, padx=20, pady=10)
        
        self.btn_guide = ctk.CTkButton(self.sidebar_frame, text="Hướng dẫn PDF", command=self.open_guide)
        self.btn_guide.grid(row=5, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Giao diện:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def _create_main_content(self):
        # Frame chính
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Tiêu đề
        self.header_label = ctk.CTkLabel(self.main_frame, text="Bảng Giá Trực Tuyến", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Stat cards (Frame chứa các label thống kê)
        self.stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        for i in range(4):
            self.stats_frame.grid_columnconfigure(i, weight=1)
            
        self.stat_cards = {}
        headers = ["Cặp tiền nóng nhất", "Biến động mạnh nhất", "Cập nhật gần nhất", "Tổng số cặp"]
        for i, header in enumerate(headers):
            card = ctk.CTkFrame(self.stats_frame, corner_radius=8, fg_color=("gray80", "gray20"))
            card.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            lbl_title = ctk.CTkLabel(card, text=header, font=ctk.CTkFont(size=12))
            lbl_title.pack(pady=(10, 0))
            lbl_value = ctk.CTkLabel(card, text="--", font=ctk.CTkFont(size=16, weight="bold"), text_color="#00ffcc")
            lbl_value.pack(pady=(5, 10))
            self.stat_cards[header] = lbl_value

        # Treeview (Bảng dữ liệu)
        # Sử dụng ttk.Treeview với style dark
        self.tree_frame = ctk.CTkFrame(self.main_frame)
        self.tree_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#333333", foreground="white", font=('Arial', 11, 'bold'))
        
        columns = ("pair", "current", "avg", "min", "max", "volatility")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        self.tree.heading("pair", text="Cặp Tiền Tệ")
        self.tree.heading("current", text="Tỷ Giá Hiện Tại")
        self.tree.heading("avg", text="Trung Bình")
        self.tree.heading("min", text="Thấp Nhất")
        self.tree.heading("max", text="Cao Nhất")
        self.tree.heading("volatility", text="Độ Biến Động")
        
        self.tree.column("pair", width=150, anchor="center")
        self.tree.column("current", width=120, anchor="e")
        self.tree.column("avg", width=120, anchor="e")
        self.tree.column("min", width=120, anchor="e")
        self.tree.column("max", width=120, anchor="e")
        self.tree.column("volatility", width=120, anchor="e")
        
        # Scrollbar cho Treeview
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def open_add_pair_window(self):
        AddPairWindow(self, self.controller)
        
    def remove_selected(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cặp tiền tệ trong bảng để xóa.")
            return
            
        values = self.tree.item(selected_item, 'values')
        if values:
            pair_str = values[0]
            base, target = pair_str.split('/')
            if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {pair_str}?"):
                success, msg = self.controller.remove_pair(base, target)
                if success:
                    messagebox.showinfo("Thành công", msg)
                else:
                    messagebox.showerror("Lỗi", msg)
                    
    def open_chart_window(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cặp tiền tệ trong bảng để xem biểu đồ.")
            return
            
        values = self.tree.item(selected_item, 'values')
        if values:
            pair_str = values[0]
            base, target = pair_str.split('/')
            ChartWindow(self, self.controller.db, base, target)
            
    def export_csv(self):
        success, msg = self.controller.export_data()
        if success:
            messagebox.showinfo("Thành công", msg)
        else:
            messagebox.showerror("Lỗi", msg)
            
    def open_guide(self):
        guide_path = os.path.join(os.getcwd(), "guide.txt")
        if not os.path.exists(guide_path):
            messagebox.showwarning("Lỗi", f"Không tìm thấy file hướng dẫn tại {guide_path}")
            return
            
        try:
            if sys.platform == "win32":
                os.startfile(guide_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", guide_path])
            else:
                subprocess.call(["xdg-open", guide_path])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {str(e)}")
            
    def update_table(self, stats):
        """Cập nhật dữ liệu vào bảng Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Thêm dữ liệu mới
        for pair_name, stat in stats.items():
            current = f"{stat['current_rate']:.4f}"
            avg = f"{stat['avg_rate']:.4f}"
            min_r = f"{stat['min_rate']:.4f}"
            max_r = f"{stat['max_rate']:.4f}"
            vol = f"{stat['volatility']:.4f}"
            
            self.tree.insert("", "end", values=(pair_name, current, avg, min_r, max_r, vol))
            
    def update_stats(self, total_pairs, hottest_pair, highest_volatility, last_update_time):
        """Cập nhật các label thống kê"""
        self.stat_cards["Tổng số cặp"].configure(text=str(total_pairs))
        self.stat_cards["Cặp tiền nóng nhất"].configure(text=hottest_pair)
        self.stat_cards["Biến động mạnh nhất"].configure(text=highest_volatility)
        self.stat_cards["Cập nhật gần nhất"].configure(text=last_update_time)
