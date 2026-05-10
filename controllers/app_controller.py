from models.database import Database
from services.api_service import APIService
from views.main_gui import MainWindow
import time
from datetime import datetime
import os

class AppController:
    def __init__(self):
        # Khởi tạo Model
        self.db = Database("currency_data.db")
        
        # Thêm một số dữ liệu ban đầu nếu chưa có
        if not self.db.get_all_pairs():
            self.db.add_pair("USD", "VND")
            self.db.add_pair("EUR", "USD")
            self.db.add_pair("USD", "JPY")
        
        # Khởi tạo View (GUI) nhưng chưa hiện (để main.py quyết định)
        self.view = MainWindow(self)
        
        # Khởi tạo Service API
        self.api_service = APIService(self.db, self.on_data_updated)
        
    def start(self):
        """Bắt đầu ứng dụng"""
        self.api_service.start()
        # Chạy một lần cập nhật ngay lập tức nếu cần
        self.update_gui_data()
        self.view.mainloop()
        
    def stop(self):
        """Dừng ứng dụng"""
        self.api_service.stop()

    def on_data_updated(self):
        """Callback được gọi từ APIService khi có dữ liệu mới (chạy ở thread khác)."""
        # Sử dụng after() để đưa việc cập nhật GUI về main thread
        self.view.after(0, self.update_gui_data)
        
    def update_gui_data(self):
        """Lấy dữ liệu từ DB và cập nhật lên View."""
        stats = self.db.get_statistics()
        self.view.update_table(stats)
        
        total_pairs = len(stats)
        hottest_pair = "--"
        highest_vol = "--"
        max_vol_val = -1
        
        for pair_name, stat in stats.items():
            if stat['volatility'] > max_vol_val:
                max_vol_val = stat['volatility']
                highest_vol = pair_name
                
        if stats:
            # Chọn đại cặp đầu tiên hoặc logic khác làm hottest_pair
            hottest_pair = list(stats.keys())[0]
            
        last_update = datetime.now().strftime("%H:%M:%S")
        
        self.view.update_stats(
            total_pairs=total_pairs,
            hottest_pair=hottest_pair,
            highest_volatility=highest_vol,
            last_update_time=last_update
        )

    def add_pair(self, base, target):
        """Xử lý yêu cầu thêm cặp tiền từ View."""
        success, msg = self.db.add_pair(base, target)
        if success:
            # Gửi yêu cầu cập nhật ngay
            self._fetch_single_pair(base, target)
        return success, msg
        
    def remove_pair(self, base, target):
        """Xử lý yêu cầu xóa cặp tiền từ View."""
        success, msg = self.db.remove_pair(base, target)
        if success:
            self.update_gui_data()
        return success, msg

    def export_data(self):
        """Xử lý yêu cầu xuất dữ liệu ra CSV."""
        export_path = os.path.join(os.getcwd(), "export_data.csv")
        return self.db.export_to_csv(export_path)

    def _fetch_single_pair(self, base, target):
        """Fetch tỷ giá cho cặp mới thêm ngay lập tức mà không đợi 30s."""
        import threading
        
        def fetch_task():
            rate = self.api_service.fetch_rate(base, target)
            if rate is not None:
                pairs = self.db.get_all_pairs()
                for pair in pairs:
                    if pair[1] == base and pair[2] == target:
                        self.db.add_history(pair[0], rate)
                        self.on_data_updated()
                        break
                        
        threading.Thread(target=fetch_task, daemon=True).start()
