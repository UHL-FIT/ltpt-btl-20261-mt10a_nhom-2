from models.database import Database
from services.api_service import APIService
from views.main_gui import MainWindow
from datetime import datetime
import threading
import os

class AppController:
    """Controller điều phối giữa Model, View và Service."""
    def __init__(self):
        # Khởi tạo Model
        self.db = Database("currency_data.db")

        # Thêm dữ liệu mẫu ban đầu nếu DB còn trống
        if not self.db.get_all_pairs():
            self.db.add_pair("USD", "VND")
            self.db.add_pair("EUR", "USD")
            self.db.add_pair("USD", "JPY")

        # Khởi tạo View
        self.view = MainWindow(self)

        # Khởi tạo API Service
        self.api_service = APIService(self.db, self.on_data_updated)

    def start(self):
        """Khởi động ứng dụng: bắt đầu API worker và chạy main loop."""
        self.api_service.start()
        self.update_gui_data()
        self.view.mainloop()

    def stop(self):
        """Dừng API worker khi thoát ứng dụng."""
        self.api_service.stop()

    # ─────────────────────── CALLBACKS ───────────────────────
    def on_data_updated(self):
        """Gọi từ thread phụ khi có dữ liệu mới. Dùng after() để an toàn với GUI."""
        self.view.after(0, self.update_gui_data)

    def update_gui_data(self):
        """Lấy thống kê từ DB và đẩy lên View."""
        stats = self.db.get_statistics()
        self.view.update_table(stats)

        total = len(stats)
        hottest = "--"
        highest_vol = "--"
        max_vol = -1

        for pair_name, stat in stats.items():
            if stat["volatility"] > max_vol:
                max_vol = stat["volatility"]
                highest_vol = pair_name

        if stats:
            hottest = list(stats.keys())[0]

        self.view.update_stats(
            total_pairs=total,
            hottest_pair=hottest,
            highest_volatility=highest_vol,
            last_update_time=datetime.now().strftime("%H:%M:%S")
        )

    # ─────────────────────── ACTIONS ───────────────────────
    def add_pair(self, base, target):
        """Thêm cặp tiền và fetch ngay lập tức."""
        success, msg = self.db.add_pair(base, target)
        if success:
            self._fetch_single_pair(base, target)
        return success, msg

    def remove_pair(self, base, target):
        """Xóa cặp tiền và refresh bảng."""
        success, msg = self.db.remove_pair(base, target)
        if success:
            self.update_gui_data()
        return success, msg

    def export_data(self, file_path=None):
        """Xuất dữ liệu ra file CSV."""
        if file_path is None:
            file_path = os.path.join(os.getcwd(), "export_data.csv")
        return self.db.export_to_csv(file_path)

    def import_data(self, file_path):
        """Nhập danh sách cặp tiền từ file CSV."""
        success, msg = self.db.import_from_csv(file_path)
        if success:
            self.update_gui_data()
        return success, msg

    # ─────────────────────── HELPER ───────────────────────
    def _fetch_single_pair(self, base, target):
        """Fetch tỷ giá cho 1 cặp tiền ngay lập tức (chạy trên thread phụ)."""
        def task():
            rate = self.api_service.fetch_rate(base, target)
            if rate is not None:
                for pair in self.db.get_all_pairs():
                    if pair[1] == base and pair[2] == target:
                        self.db.add_history(pair[0], rate)
                        self.on_data_updated()
                        break
        threading.Thread(target=task, daemon=True).start()
