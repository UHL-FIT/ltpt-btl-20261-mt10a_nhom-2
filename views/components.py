import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import sys
import subprocess

# Danh sách ~170 mã ISO tiền tệ phổ biến nhúng cứng
ISO_CURRENCIES = [
    "AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN",
    "BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BRL",
    "BSD","BTN","BWP","BYR","BZD","CAD","CDF","CHF","CLP","CNY",
    "COP","CRC","CUP","CVE","CZK","DJF","DKK","DOP","DZD","EGP",
    "ERN","ETB","EUR","FJD","FKP","GBP","GEL","GHS","GIP","GMD",
    "GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS",
    "INR","IQD","IRR","ISK","JMD","JOD","JPY","KES","KGS","KHR",
    "KMF","KPW","KRW","KWD","KYD","KZT","LAK","LBP","LKR","LRD",
    "LSL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRO",
    "MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO","NOK",
    "NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN","PYG",
    "QAR","RON","RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK",
    "SGD","SHP","SLL","SOS","SRD","STD","SVC","SYP","SZL","THB",
    "TJS","TMT","TND","TOP","TRY","TTD","TWD","TZS","UAH","UGX",
    "USD","UYU","UZS","VEF","VND","VUV","WST","XAF","XCD","XOF",
    "XPF","YER","ZAR","ZMW","ZWL"
]

class SplashScreen(ctk.CTkToplevel):
    """Màn hình chờ khi khởi động ứng dụng."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Khởi động...")
        self.geometry("420x260")
        self.overrideredirect(True)  # Ẩn thanh tiêu đề

        # Căn giữa màn hình
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 130
        self.geometry(f"+{x}+{y}")
        self.configure(fg_color="#1e1e24")

        ctk.CTkLabel(self, text="💱 Currency Tracker Pro",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#00ffcc").pack(pady=(50, 10))
        ctk.CTkLabel(self, text="Đang khởi tạo dữ liệu...",
                     font=ctk.CTkFont(size=13)).pack()
        self.progressbar = ctk.CTkProgressBar(self, width=320, progress_color="#00ffcc")
        self.progressbar.pack(pady=20)
        self.progressbar.set(0)
        self.protocol("WM_DELETE_WINDOW", lambda: None)


class AutocompleteEntry(ctk.CTkFrame):
    """
    Widget nhập mã ISO với dropdown gợi ý khi gõ chữ cái.
    Gợi ý hiện ngay bên dưới ô nhập liệu, không bị kẹt góc màn hình.
    """
    def __init__(self, parent, placeholder="Nhập mã ISO...", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=260)
        self.entry.pack(fill="x")

        self._dropdown = None
        self._listbox = None

        self.entry.bind("<KeyRelease>", self._on_keyrelease)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Down>", self._focus_listbox)
        self.entry.bind("<Escape>", lambda e: self._hide_dropdown())

    def _on_keyrelease(self, event):
        """Lọc gợi ý theo ký tự người dùng gõ."""
        if event.keysym in ("Down", "Up", "Return", "Escape", "Tab"):
            return

        typed = self.entry.get().strip().upper()
        if not typed:
            self._hide_dropdown()
            return

        matches = [c for c in ISO_CURRENCIES if c.startswith(typed)][:8]
        if matches:
            self._show_dropdown(matches)
        else:
            self._hide_dropdown()

    def _show_dropdown(self, matches):
        """Hiện dropdown ngay bên dưới ô nhập liệu."""
        self._hide_dropdown()

        # Lấy cửa sổ gốc (CTkToplevel của Add/Edit window) làm parent
        root = self.winfo_toplevel()

        self._dropdown = tk.Toplevel(root)
        self._dropdown.overrideredirect(True)
        self._dropdown.configure(bg="#2b2b2b")
        self._dropdown.attributes("-topmost", True)

        # Tính toán vị trí sau khi widget đã render xong
        self.update_idletasks()
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height() + 2
        w = max(self.entry.winfo_width(), 200)
        h = len(matches) * 28

        self._dropdown.geometry(f"{w}x{h}+{x}+{y}")

        self._listbox = tk.Listbox(
            self._dropdown,
            bg="#2b2b2b", fg="white",
            selectbackground="#1f538d",
            font=("Arial", 11),
            borderwidth=0, highlightthickness=0,
            activestyle="none"
        )
        self._listbox.pack(fill="both", expand=True)

        for m in matches:
            self._listbox.insert(tk.END, m)

        self._listbox.bind("<<ListboxSelect>>", self._on_select)
        self._dropdown.lift()

    def _hide_dropdown(self):
        """Hủy dropdown."""
        if self._dropdown:
            try:
                self._dropdown.destroy()
            except Exception:
                pass
            self._dropdown = None
            self._listbox = None

    def _focus_listbox(self, event):
        """Di chuyển focus xuống listbox khi bấm phím mũi tên xuống."""
        if self._listbox:
            self._listbox.focus_set()
            self._listbox.selection_set(0)

    def _on_select(self, event):
        """Điền mã được chọn vào ô nhập và đóng dropdown."""
        if not self._listbox:
            return
        sel = self._listbox.curselection()
        if sel:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self._listbox.get(sel[0]))
        self._hide_dropdown()
        self.entry.focus_set()

    def _on_focus_out(self, event):
        """Ẩn dropdown sau 200ms để kịp xử lý click vào listbox."""
        self.after(200, self._hide_dropdown)

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)


class AddPairWindow(ctk.CTkToplevel):
    """Cửa sổ thêm cặp tiền tệ mới."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Thêm cặp tiền tệ")
        self.geometry("360x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="➕ Thêm Cặp Tiền Tệ",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        ctk.CTkLabel(self, text="Tiền tệ gốc (Base):",
                     font=ctk.CTkFont(weight="bold")).pack(padx=20, anchor="w")
        self.autocomplete_base = AutocompleteEntry(self, placeholder="VD: USD")
        self.autocomplete_base.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self, text="Tiền tệ đích (Target):",
                     font=ctk.CTkFont(weight="bold")).pack(padx=20, anchor="w", pady=(10, 0))
        self.autocomplete_target = AutocompleteEntry(self, placeholder="VD: VND")
        self.autocomplete_target.pack(padx=20, pady=5, fill="x")

        ctk.CTkButton(self, text="💾 Lưu", command=self.save,
                      fg_color="#28a745", hover_color="#218838").pack(pady=20)

    def save(self):
        """Kiểm tra và lưu cặp tiền tệ mới."""
        base = self.autocomplete_base.get().strip().upper()
        target = self.autocomplete_target.get().strip().upper()

        if not base or not target:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ mã tiền tệ.", parent=self)
            return
        if len(base) != 3 or len(target) != 3:
            messagebox.showwarning("Sai định dạng", "Mã tiền tệ ISO phải có đúng 3 ký tự (VD: USD, VND).", parent=self)
            return
        if base == target:
            messagebox.showwarning("Không hợp lệ", "Tiền tệ gốc và đích không được giống nhau.", parent=self)
            return

        success, message = self.controller.add_pair(base, target)
        if success:
            messagebox.showinfo("Thành công", message, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message, parent=self)


class EditPairWindow(ctk.CTkToplevel):
    """Cửa sổ sửa cặp tiền tệ đã có (xóa cặp cũ, thêm cặp mới)."""
    def __init__(self, parent, controller, old_base, old_target):
        super().__init__(parent)
        self.controller = controller
        self.old_base = old_base
        self.old_target = old_target
        self.title("Sửa cặp tiền tệ")
        self.geometry("360x340")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="✏️ Sửa Cặp Tiền Tệ",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text=f"Đang sửa: {old_base}/{old_target}",
                     font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Tiền tệ gốc mới:",
                     font=ctk.CTkFont(weight="bold")).pack(padx=20, anchor="w")
        self.autocomplete_base = AutocompleteEntry(self, placeholder="VD: USD")
        self.autocomplete_base.pack(padx=20, pady=5, fill="x")
        self.autocomplete_base.set(old_base)  # Điền sẵn giá trị cũ

        ctk.CTkLabel(self, text="Tiền tệ đích mới:",
                     font=ctk.CTkFont(weight="bold")).pack(padx=20, anchor="w", pady=(10, 0))
        self.autocomplete_target = AutocompleteEntry(self, placeholder="VD: VND")
        self.autocomplete_target.pack(padx=20, pady=5, fill="x")
        self.autocomplete_target.set(old_target)  # Điền sẵn giá trị cũ

        ctk.CTkButton(self, text="💾 Lưu thay đổi", command=self.save,
                      fg_color="#007bff", hover_color="#0056b3").pack(pady=20)

    def save(self):
        """Kiểm tra, xóa cặp cũ và thêm cặp mới."""
        new_base = self.autocomplete_base.get().strip().upper()
        new_target = self.autocomplete_target.get().strip().upper()

        if not new_base or not new_target:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ mã tiền tệ.", parent=self)
            return
        if len(new_base) != 3 or len(new_target) != 3:
            messagebox.showwarning("Sai định dạng", "Mã tiền tệ ISO phải có đúng 3 ký tự.", parent=self)
            return
        if new_base == new_target:
            messagebox.showwarning("Không hợp lệ", "Tiền tệ gốc và đích không được giống nhau.", parent=self)
            return

        # Xóa cặp cũ
        self.controller.remove_pair(self.old_base, self.old_target)
        # Thêm cặp mới
        success, message = self.controller.add_pair(new_base, new_target)
        if success:
            messagebox.showinfo("Thành công", f"Đã cập nhật thành {new_base}/{new_target}.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message, parent=self)


class ChartWindow(ctk.CTkToplevel):
    """Cửa sổ hiển thị biểu đồ biến động tỷ giá."""
    def __init__(self, parent, db, base, target):
        super().__init__(parent)
        self.db = db
        self.base = base
        self.target = target
        self.title(f"📈 Biểu đồ biến động: {base}/{target}")
        self.geometry("800x580")

        plt.style.use('dark_background')
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        self.draw_chart()

    def draw_chart(self):
        """Vẽ đồ thị đường từ dữ liệu lịch sử trong Database."""
        self.ax.clear()
        df = self.db.get_history_dataframe(self.base, self.target)

        if df.empty:
            self.ax.text(0.5, 0.5, "Chưa có dữ liệu lịch sử.\nHãy đợi ứng dụng cập nhật tỷ giá.",
                         ha='center', va='center', fontsize=13, color='gray')
        else:
            self.ax.plot(df['timestamp'], df['rate'],
                         marker='o', linestyle='-', color='#00ffcc', linewidth=2)
            self.ax.set_title(f"Tỷ giá {self.base}/{self.target} theo thời gian", color='white')
            self.ax.set_xlabel("Thời gian", color='white')
            self.ax.set_ylabel("Tỷ giá", color='white')
            self.ax.tick_params(colors='white')
            self.figure.autofmt_xdate()
            self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()


class AboutWindow(ctk.CTkToplevel):
    """Cửa sổ About - Thông tin phiên bản và mở file hướng dẫn."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Về ứng dụng")
        self.geometry("380x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="💱 Currency Tracker Pro",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00ffcc").pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Phiên bản: v1.0.0",
                     font=ctk.CTkFont(size=13)).pack()
        ctk.CTkLabel(self, text="Tác giả: Nhóm 2",
                     font=ctk.CTkFont(size=13)).pack(pady=3)
        ctk.CTkLabel(self, text="Ngày phát hành: 15/05/2025",
                     font=ctk.CTkFont(size=13)).pack()
        ctk.CTkLabel(self, text="Môn học: Lập trình Python",
                     font=ctk.CTkFont(size=13)).pack(pady=3)

        ctk.CTkFrame(self, height=1, fg_color="gray40").pack(fill="x", padx=30, pady=15)

        ctk.CTkButton(self, text="📄 Mở hướng dẫn sử dụng",
                      command=self.open_guide,
                      fg_color="#007bff", hover_color="#0056b3").pack(pady=5)
        ctk.CTkButton(self, text="Đóng", command=self.destroy,
                      fg_color="gray40", hover_color="gray30").pack(pady=5)

    def open_guide(self):
        """Mở file hướng dẫn sử dụng."""
        guide_path = os.path.join(os.getcwd(), "guide.txt")
        if not os.path.exists(guide_path):
            messagebox.showwarning("Không tìm thấy file",
                                   f"Không tìm thấy file hướng dẫn tại:\n{guide_path}", parent=self)
            return
        try:
            if sys.platform == "win32":
                os.startfile(guide_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", guide_path])
            else:
                subprocess.call(["xdg-open", guide_path])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {str(e)}", parent=self)
