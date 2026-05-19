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

# Danh sách mã ISO tiền tệ và tên quốc gia/khu vực tương ứng
CURRENCIES = {
    "AED": "Các Tiểu vương quốc Ả Rập Thống nhất (Dirham)", "AFN": "Afghanistan (Afghani)", "ALL": "Albania (Lek)",
    "AMD": "Armenia (Dram)", "ANG": "Curaçao và Sint Maarten (Guilder)", "AOA": "Angola (Kwanza)",
    "ARS": "Argentina (Peso)", "AUD": "Đô la Úc", "AWG": "Aruba (Florin)", "AZN": "Azerbaijan (Manat)",
    "BAM": "Bosnia và Herzegovina (Mark)", "BBD": "Barbados (Đô la)", "BDT": "Bangladesh (Taka)",
    "BGN": "Bulgaria (Lev)", "BHD": "Bahrain (Dinar)", "BIF": "Burundi (Franc)", "BMD": "Bermuda (Đô la)",
    "BND": "Brunei (Đô la)", "BOB": "Bolivia (Boliviano)", "BRL": "Brazil (Real)", "BSD": "Bahamas (Đô la)",
    "BTN": "Bhutan (Ngultrum)", "BWP": "Botswana (Pula)", "BYR": "Belarus (Rúp)", "BZD": "Belize (Đô la)",
    "CAD": "Đô la Canada", "CDF": "Congo (Franc)", "CHF": "Franc Thụy Sĩ", "CLP": "Chile (Peso)",
    "CNY": "Nhân dân tệ (Trung Quốc)", "COP": "Colombia (Peso)", "CRC": "Costa Rica (Colon)", "CUP": "Cuba (Peso)",
    "CVE": "Cape Verde (Escudo)", "CZK": "Cộng hòa Séc (Koruna)", "DJF": "Djibouti (Franc)", "DKK": "Đan Mạch (Krone)",
    "DOP": "Cộng hòa Dominica (Peso)", "DZD": "Algeria (Dinar)", "EGP": "Ai Cập (Bảng)", "ERN": "Eritrea (Nakfa)",
    "ETB": "Ethiopia (Birr)", "EUR": "Euro", "FJD": "Fiji (Đô la)", "FKP": "Quần đảo Falkland (Bảng)",
    "GBP": "Bảng Anh", "GEL": "Georgia (Lari)", "GHS": "Ghana (Cedi)", "GIP": "Gibraltar (Bảng)",
    "GMD": "Gambia (Dalasi)", "GNF": "Guinea (Franc)", "GTQ": "Guatemala (Quetzal)", "GYD": "Guyana (Đô la)",
    "HKD": "Đô la Hồng Kông", "HNL": "Honduras (Lempira)", "HRK": "Croatia (Kuna)", "HTG": "Haiti (Gourde)",
    "HUF": "Hungary (Forint)", "IDR": "Rupiah Indonesia", "ILS": "Israel (Shekel)", "INR": "Rupee Ấn Độ",
    "IQD": "Iraq (Dinar)", "IRR": "Iran (Rial)", "ISK": "Iceland (Krona)", "JMD": "Jamaica (Đô la)",
    "JOD": "Jordan (Dinar)", "JPY": "Yên Nhật", "KES": "Kenya (Shilling)", "KGS": "Kyrgyzstan (Som)",
    "KHR": "Campuchia (Riel)", "KMF": "Comoros (Franc)", "KPW": "Triều Tiên (Won)", "KRW": "Won Hàn Quốc",
    "KWD": "Kuwait (Dinar)", "KYD": "Quần đảo Cayman (Đô la)", "KZT": "Kazakhstan (Tenge)", "LAK": "Lào (Kip)",
    "LBP": "Li-băng (Bảng)", "LKR": "Sri Lanka (Rupee)", "LRD": "Liberia (Đô la)", "LSL": "Lesotho (Loti)",
    "LYD": "Libya (Dinar)", "MAD": "Ma-rốc (Dirham)", "MDL": "Moldova (Leu)", "MGA": "Madagascar (Ariary)",
    "MKD": "Bắc Macedonia (Denar)", "MMK": "Myanmar (Kyat)", "MNT": "Mông Cổ (Tugrik)", "MOP": "Ma Cao (Pataca)",
    "MRO": "Mauritania (Ouguiya)", "MUR": "Mauritius (Rupee)", "MVR": "Maldives (Rufiyaa)", "MWK": "Malawi (Kwacha)",
    "MXN": "Mexico (Peso)", "MYR": "Malaysia (Ringgit)", "MZN": "Mozambique (Metical)", "NAD": "Namibia (Đô la)",
    "NGN": "Nigeria (Naira)", "NIO": "Nicaragua (Cordoba)", "NOK": "Na Uy (Krone)", "NPR": "Nepal (Rupee)",
    "NZD": "Đô la New Zealand", "OMR": "Oman (Rial)", "PAB": "Panama (Balboa)", "PEN": "Peru (Sol)",
    "PGK": "Papua New Guinea (Kina)", "PHP": "Philippines (Peso)", "PKR": "Pakistan (Rupee)", "PLN": "Ba Lan (Zloty)",
    "PYG": "Paraguay (Guarani)", "QAR": "Qatar (Riyal)", "RON": "Romania (Leu)", "RSD": "Serbia (Dinar)",
    "RUB": "Rúp Nga", "RWF": "Rwanda (Franc)", "SAR": "Ả Rập Xê-út (Riyal)", "SBD": "Quần đảo Solomon (Đô la)",
    "SCR": "Seychelles (Rupee)", "SDG": "Sudan (Bảng)", "SEK": "Thụy Điển (Krona)", "SGD": "Đô la Singapore",
    "SHP": "Saint Helena (Bảng)", "SLL": "Sierra Leone (Leone)", "SOS": "Somalia (Shilling)", "SRD": "Suriname (Đô la)",
    "STD": "São Tomé và Príncipe (Dobra)", "SVC": "El Salvador (Colon)", "SYP": "Syria (Bảng)", "SZL": "Eswatini (Lilangeni)",
    "THB": "Baht Thái", "TJS": "Tajikistan (Somoni)", "TMT": "Turkmenistan (Manat)", "TND": "Tunisia (Dinar)",
    "TOP": "Tonga (Paʻanga)", "TRY": "Thổ Nhĩ Kỳ (Lira)", "TTD": "Trinidad và Tobago (Đô la)", "TWD": "Tân Đài Tệ",
    "TZS": "Tanzania (Shilling)", "UAH": "Ukraine (Hryvnia)", "UGX": "Uganda (Shilling)", "USD": "Đô la Mỹ",
    "UYU": "Uruguay (Peso)", "UZS": "Uzbekistan (Som)", "VEF": "Venezuela (Bolívar)", "VND": "Việt Nam Đồng",
    "VUV": "Vanuatu (Vatu)", "WST": "Samoa (Tala)", "XAF": "CFA Franc BEAC", "XCD": "Đô la Đông Caribbean",
    "XOF": "CFA Franc BCEAO", "XPF": "CFP Franc", "YER": "Yemen (Rial)", "ZAR": "Nam Phi (Rand)",
    "ZMW": "Zambia (Kwacha)", "ZWL": "Zimbabwe (Đô la)"
}

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

        matches = []
        for code, name in CURRENCIES.items():
            if typed in code or typed in name.upper():
                matches.append(f"{code} - {name}")
            if len(matches) >= 8:
                break

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
        w = max(self.entry.winfo_width(), 350)
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
        """Điền mã được chọn kèm tên quốc gia/khu vực vào ô nhập và đóng dropdown."""
        if not self._listbox:
            return
        sel = self._listbox.curselection()
        if sel:
            selected_text = self._listbox.get(sel[0])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_text)
        self._hide_dropdown()
        self.entry.focus_set()

    def _on_focus_out(self, event):
        """Ẩn dropdown sau 200ms để kịp xử lý click vào listbox."""
        self.after(200, self._hide_dropdown)

    def get(self):
        """Lấy 3 ký tự mã ISO từ ô nhập (tách bỏ phần tên nước/khu vực nếu có)."""
        val = self.entry.get().strip()
        if " - " in val:
            return val.split(" - ")[0].strip().upper()
        return val.upper()

    def set(self, value):
        """Đặt giá trị ô nhập (tự động kèm tên nước/khu vực gợi ý nếu có trong danh sách)."""
        self.entry.delete(0, tk.END)
        code = value.strip().upper()
        if code in CURRENCIES:
            self.entry.insert(0, f"{code} - {CURRENCIES[code]}")
        else:
            self.entry.insert(0, code)


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
        """Mở file hướng dẫn sử dụng (ưu tiên PDF, fallback TXT)."""
        guide_path = os.path.join(os.getcwd(), "guide.pdf")
        if not os.path.exists(guide_path):
            # Fallback sang guide.txt nếu không có PDF
            guide_path = os.path.join(os.getcwd(), "guide.txt")
            
        if not os.path.exists(guide_path):
            messagebox.showwarning("Không tìm thấy file",
                                   "Không tìm thấy file hướng dẫn sử dụng (guide.pdf hoặc guide.txt)!", parent=self)
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
