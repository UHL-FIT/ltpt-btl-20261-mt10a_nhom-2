import requests
import threading
import time

class APIService:
    def __init__(self, db, update_callback=None):
        """
        db: Đối tượng Database.
        update_callback: Hàm được gọi khi có dữ liệu mới.
        """
        self.db = db
        self.update_callback = update_callback
        self.is_running = False
        self.thread = None
        # Sử dụng API miễn phí open.er-api.com
        self.base_url = "https://open.er-api.com/v6/latest/"
        
    def fetch_rate(self, base_currency, target_currency):
        """Lấy tỷ giá cho 1 cặp tiền tệ."""
        try:
            response = requests.get(f"{self.base_url}{base_currency}", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") == "success":
                rates = data.get("rates", {})
                if target_currency in rates:
                    return rates[target_currency]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi lấy dữ liệu API ({base_currency}/{target_currency}): {e}")
            return None

    def _update_loop(self):
        """Vòng lặp chạy ngầm cập nhật tỷ giá mỗi 30 giây."""
        while self.is_running:
            try:
                pairs = self.db.get_all_pairs()
                updated = False
                for pair in pairs:
                    pair_id, base, target = pair
                    rate = self.fetch_rate(base, target)
                    if rate is not None:
                        self.db.add_history(pair_id, rate)
                        updated = True
                
                # Gọi callback cập nhật GUI nếu có dữ liệu mới
                if updated and self.update_callback:
                    self.update_callback()
                    
            except Exception as e:
                print(f"Lỗi trong vòng lặp cập nhật: {e}")
                
            # Đợi 3600 giây (1 giờ) trước khi cập nhật tiếp
            # API miễn phí chỉ cập nhật 1 lần/ngày, không cần gọi thường xuyên
            # Dùng vòng lặp nhỏ để có thể dừng thread nhanh khi tắt app
            for _ in range(3600):
                if not self.is_running:
                    break
                time.sleep(1)

    def start(self):
        """Bắt đầu tiến trình cập nhật tự động."""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._update_loop, daemon=True)
            self.thread.start()

    def stop(self):
        """Dừng tiến trình cập nhật."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
