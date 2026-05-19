import customtkinter as ctk
from tkinter import ttk, filedialog
import tkinter.messagebox as messagebox
from views.components import AddPairWindow, EditPairWindow, ChartWindow, AboutWindow

class MainWindow(ctk.CTk):
    """Cửa sổ chính của ứng dụng Currency Tracker Pro."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._all_stats = {}  # Lưu toàn bộ dữ liệu để hỗ trợ tìm kiếm

        self.title("Real-time Currency Tracker Pro")
        self.geometry("1150x750")
        self.minsize(900, 600)

        # Layout chính: Sidebar (cột 0) + Nội dung (cột 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._create_sidebar()
        self._create_main_content()

    # ─────────────────────── SIDEBAR ───────────────────────
    def _create_sidebar(self):
        """Tạo thanh menu bên trái."""
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)  # Đẩy phần theme xuống dưới cùng

        # Logo
        ctk.CTkLabel(self.sidebar, text="💱 Currency\nTracker Pro",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#00ffcc").grid(row=0, column=0, padx=20, pady=(25, 20))

        # Các nút chức năng
        buttons = [
            ("➕  Thêm cặp tiền",   "#28a745", "#218838", self.open_add_window,    1),
            ("✏️  Sửa cặp đã chọn", "#007bff", "#0056b3", self.open_edit_window,   2),
            ("🗑️  Xóa cặp đã chọn", "#dc3545", "#c82333", self.remove_selected,    3),
            ("📈  Xem biểu đồ",     "#6f42c1", "#59359a", self.open_chart_window,  4),
            ("📥  Nhập CSV",         "#fd7e14", "#e8590c", self.import_csv,         5),
            ("📤  Xuất CSV",         "#17a2b8", "#138496", self.export_csv,         6),
            ("ℹ️  About",            "#6c757d", "#5a6268", self.open_about_window,  7),
        ]

        for text, color, hover, cmd, row in buttons:
            ctk.CTkButton(self.sidebar, text=text, command=cmd,
                          fg_color=color, hover_color=hover,
                          anchor="w", width=170).grid(row=row, column=0, padx=20, pady=5)

        # Đổi theme
        ctk.CTkLabel(self.sidebar, text="Giao diện:", anchor="w").grid(
            row=10, column=0, padx=20, pady=(10, 0))
        ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light", "System"],
                          command=lambda m: ctk.set_appearance_mode(m)).grid(
            row=11, column=0, padx=20, pady=(5, 20))

    # ─────────────────────── MAIN CONTENT ───────────────────────
    def _create_main_content(self):
        """Tạo khu vực nội dung chính."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)  # Bảng dữ liệu co giãn

        # Tiêu đề
        ctk.CTkLabel(self.main_frame, text="Bảng Tỷ Giá Trực Tuyến",
                     font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Stat cards
        self._create_stat_cards()

        # Thanh tìm kiếm (Row 2)
        self._create_search_bar()

        # Bảng dữ liệu (Treeview - Row 3)
        self._create_treeview()

        # Mini Calculator (Row 4)
        self._create_mini_calculator()

    def _create_search_bar(self):
        """Tạo thanh tìm kiếm dữ liệu trên bảng."""
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(search_frame, text="🔍 Tìm kiếm:",
                     font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                         placeholder_text="Nhập mã tiền tệ để lọc (VD: USD/VND hoặc EUR)...")
        self.search_entry.grid(row=0, column=1, sticky="ew")
        
        # Nút xóa trắng ô tìm kiếm
        ctk.CTkButton(search_frame, text="Xóa", width=60, 
                      command=lambda: self.search_var.set(""),
                      fg_color="gray40", hover_color="gray30").grid(row=0, column=2, padx=(10, 0))

    def _on_search_change(self, *args):
        """Kích hoạt khi nội dung tìm kiếm thay đổi."""
        self._render_table(self._all_stats)

    def _create_stat_cards(self):
        """Tạo 4 thẻ thống kê tổng quan."""
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

        self.stat_cards = {}
        headers = ["Tổng số cặp", "Biến động mạnh nhất", "Cập nhật lần cuối", "Cặp tiền theo dõi"]
        for i, header in enumerate(headers):
            card = ctk.CTkFrame(stats_frame, corner_radius=8, fg_color=("gray80", "gray20"))
            card.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            ctk.CTkLabel(card, text=header, font=ctk.CTkFont(size=11)).pack(pady=(8, 0))
            lbl = ctk.CTkLabel(card, text="--",
                               font=ctk.CTkFont(size=15, weight="bold"),
                               text_color="#00ffcc")
            lbl.pack(pady=(3, 8))
            self.stat_cards[header] = lbl

    def _create_treeview(self):
        """Tạo bảng hiển thị dữ liệu tỷ giá."""
        tree_frame = ctk.CTkFrame(self.main_frame)
        tree_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Style dark cho Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure("Treeview.Heading", background="#333333",
                        foreground="white", font=("Arial", 11, "bold"))

        cols = ("pair", "current", "avg", "min", "max", "volatility")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

        col_cfg = [
            ("pair",       "Cặp Tiền Tệ",    150, "center"),
            ("current",    "Tỷ Giá Hiện Tại", 130, "e"),
            ("avg",        "Trung Bình",       120, "e"),
            ("min",        "Thấp Nhất",        120, "e"),
            ("max",        "Cao Nhất",         120, "e"),
            ("volatility", "Độ Biến Động",     120, "e"),
        ]
        for col, text, width, anchor in col_cfg:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _create_mini_calculator(self):
        """Tạo ô tính nhanh quy đổi tiền tệ."""
        calc_frame = ctk.CTkFrame(self.main_frame, corner_radius=8,
                                  fg_color=("gray85", "gray18"))
        calc_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        calc_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(calc_frame, text="🧮 Quy đổi nhanh:",
                     font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=15, pady=12, sticky="w")

        # Ô nhập số tiền
        self.calc_amount = ctk.CTkEntry(calc_frame, placeholder_text="Nhập số tiền...", width=150)
        self.calc_amount.grid(row=0, column=1, padx=8, pady=12)

        # Dropdown chọn cặp tiền
        self.calc_pair_var = ctk.StringVar(value="-- Chọn cặp tiền --")
        self.calc_pair_menu = ctk.CTkOptionMenu(calc_frame, variable=self.calc_pair_var,
                                                values=["-- Chọn cặp tiền --"], width=160)
        self.calc_pair_menu.grid(row=0, column=2, padx=8, pady=12)

        ctk.CTkButton(calc_frame, text="Quy đổi", command=self.calculate,
                      width=90).grid(row=0, column=3, padx=8, pady=12)

        self.calc_result_label = ctk.CTkLabel(calc_frame, text="Kết quả: --",
                                              font=ctk.CTkFont(size=13, weight="bold"),
                                              text_color="#00ffcc")
        self.calc_result_label.grid(row=0, column=4, padx=15, pady=12)

    # ─────────────────────── LOGIC UI ───────────────────────
    def open_add_window(self):
        AddPairWindow(self, self.controller)

    def open_edit_window(self):
        """Mở cửa sổ sửa, kiểm tra có đúng 1 dòng được chọn không."""
        selected = self.tree.selection()
        if len(selected) == 0:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một cặp tiền tệ để sửa.")
            return
        if len(selected) > 1:
            messagebox.showwarning("Chọn nhiều hơn 1",
                                   "Chỉ được chọn 1 cặp tiền tệ để sửa tại một thời điểm.")
            return
        values = self.tree.item(selected[0], "values")
        if values:
            base, target = values[0].split("/")
            EditPairWindow(self, self.controller, base, target)

    def remove_selected(self):
        """Xóa các cặp tiền đang được chọn."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn cặp tiền tệ cần xóa.")
            return
        if not messagebox.askyesno("Xác nhận xóa",
                                   f"Bạn có chắc muốn xóa {len(selected)} cặp tiền đã chọn?"):
            return
        for item in selected:
            values = self.tree.item(item, "values")
            if values:
                base, target = values[0].split("/")
                self.controller.remove_pair(base, target)

    def open_chart_window(self):
        """Mở biểu đồ cho cặp tiền đang chọn."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một cặp tiền tệ để xem biểu đồ.")
            return
        values = self.tree.item(selected[0], "values")
        if values:
            base, target = values[0].split("/")
            ChartWindow(self, self.controller.db, base, target)

    def export_csv(self):
        """Xuất dữ liệu ra CSV."""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            initialfile="export_data.csv", title="Lưu file CSV")
        if not path:
            return
        success, msg = self.controller.export_data(path)
        if success:
            messagebox.showinfo("Thành công", msg)
        else:
            messagebox.showerror("Lỗi", msg)

    def import_csv(self):
        """Nhập dữ liệu từ CSV."""
        path = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            title="Mở file CSV")
        if not path:
            return
        success, msg = self.controller.import_data(path)
        if success:
            messagebox.showinfo("Thành công", msg)
        else:
            messagebox.showerror("Lỗi", msg)

    def open_about_window(self):
        AboutWindow(self)

    def calculate(self):
        """Tính quy đổi số tiền theo tỷ giá hiện tại."""
        amount_str = self.calc_amount.get().strip()
        pair = self.calc_pair_var.get()

        if not amount_str:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập số tiền cần quy đổi.")
            return
        if pair == "-- Chọn cặp tiền --" or "/" not in pair:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn cặp tiền tệ.")
            return
        try:
            amount = float(amount_str.replace(",", ""))
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Số tiền phải là một con số hợp lệ.")
            return

        stat = self._all_stats.get(pair)
        if not stat:
            messagebox.showwarning("Không có dữ liệu", "Chưa có tỷ giá cho cặp này.")
            return

        rate = stat["current_rate"]
        result = amount * rate
        base, target = pair.split("/")
        self.calc_result_label.configure(
            text=f"= {result:,.4f} {target}")

    # ─────────────────────── CẬP NHẬT DỮ LIỆU ───────────────────────
    def _render_table(self, stats: dict):
        """Vẽ lại bảng từ dictionary stats được truyền vào."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        query = self.search_var.get().strip().upper() if hasattr(self, 'search_var') else ""
        for pair_name, stat in stats.items():
            if query and query not in pair_name.upper():
                continue
            self.tree.insert("", "end", values=(
                pair_name,
                f"{stat['current_rate']:.4f}",
                f"{stat['avg_rate']:.4f}",
                f"{stat['min_rate']:.4f}",
                f"{stat['max_rate']:.4f}",
                f"{stat['volatility']:.6f}",
            ))

    def update_table(self, stats: dict):
        """Cập nhật toàn bộ bảng và bộ nhớ _all_stats."""
        self._all_stats = stats
        # Cập nhật dropdown mini-calculator
        pairs = list(stats.keys()) if stats else []
        self.calc_pair_menu.configure(values=pairs if pairs else ["-- Chọn cặp tiền --"])
        if not pairs:
            self.calc_pair_var.set("-- Chọn cặp tiền --")
        elif self.calc_pair_var.get() not in pairs:
            self.calc_pair_var.set(pairs[0])
        self._render_table(stats)

    def update_stats(self, total_pairs, hottest_pair, highest_volatility, last_update_time):
        """Cập nhật các thẻ thống kê."""
        self.stat_cards["Tổng số cặp"].configure(text=str(total_pairs))
        self.stat_cards["Cặp tiền theo dõi"].configure(text=hottest_pair)
        self.stat_cards["Biến động mạnh nhất"].configure(text=highest_volatility)
        self.stat_cards["Cập nhật lần cuối"].configure(text=last_update_time)
