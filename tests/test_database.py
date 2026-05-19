import unittest
import os
import pandas as pd
import numpy as np
from models.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Sử dụng một database tạm thời để kiểm thử
        self.test_db_path = "test_currency.db"
        self.db = Database(self.test_db_path)

    def tearDown(self):
        # Xóa database tạm sau khi chạy test xong
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

    def test_add_remove_pair(self):
        # Test thêm cặp tiền mới
        success, msg = self.db.add_pair("USD", "VND")
        self.assertTrue(success)
        self.assertEqual(msg, "Thêm thành công.")

        # Test thêm cặp trùng lặp
        success, msg = self.db.add_pair("USD", "VND")
        self.assertFalse(success)
        self.assertEqual(msg, "Cặp tiền tệ này đã tồn tại.")

        # Test lấy danh sách tất cả các cặp
        pairs = self.db.get_all_pairs()
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1], "USD")
        self.assertEqual(pairs[0][2], "VND")

        # Test xóa cặp tiền
        success_del, msg_del = self.db.remove_pair("USD", "VND")
        self.assertTrue(success_del)
        self.assertEqual(len(self.db.get_all_pairs()), 0)

    def test_statistics_calculation(self):
        # Thêm cặp tiền và lịch sử tỷ giá
        self.db.add_pair("USD", "VND")
        pairs = self.db.get_all_pairs()
        pair_id = pairs[0][0]

        # Thêm 4 bản ghi tỷ giá lịch sử: 24000, 24500, 23500, 25000
        rates = [24000.0, 24500.0, 23500.0, 25000.0]
        for rate in rates:
            self.db.add_history(pair_id, rate)

        # Lấy kết quả thống kê (Pandas)
        stats = self.db.get_statistics()
        self.assertIn("USD/VND", stats)
        
        stat_usd_vnd = stats["USD/VND"]
        self.assertEqual(stat_usd_vnd["current_rate"], 25000.0) # Tỷ giá cuối cùng
        self.assertEqual(stat_usd_vnd["min_rate"], 23500.0)     # Thấp nhất
        self.assertEqual(stat_usd_vnd["max_rate"], 25000.0)     # Cao nhất
        
        # Trung bình: (24000 + 24500 + 23500 + 25000) / 4 = 24250.0
        self.assertEqual(stat_usd_vnd["avg_rate"], 24250.0)

        # Kiểm tra Volatility (độ lệch chuẩn mẫu - Standard Deviation)
        expected_std = np.std(rates, ddof=1) # pandas dùng ddof=1 mặc định
        self.assertAlmostEqual(stat_usd_vnd["volatility"], expected_std, places=4)

    def test_export_import_csv(self):
        # Thêm 2 cặp tiền tệ
        self.db.add_pair("USD", "VND")
        self.db.add_pair("EUR", "USD")

        # Tạo file CSV mẫu để import
        import_csv_path = "test_import.csv"
        df_import = pd.DataFrame({
            "base": ["GBP", "JPY"],
            "target": ["USD", "USD"]
        })
        df_import.to_csv(import_csv_path, index=False)

        # Test Import từ CSV
        success, msg = self.db.import_from_csv(import_csv_path)
        self.assertTrue(success)
        self.assertIn("Đã nhập thành công 2 cặp tiền tệ", msg)

        # Kiểm tra tổng số cặp sau khi import: 2 cặp gốc + 2 cặp import = 4 cặp
        pairs = self.db.get_all_pairs()
        self.assertEqual(len(pairs), 4)

        # Dọn dẹp file test import
        if os.path.exists(import_csv_path):
            os.remove(import_csv_path)

if __name__ == "__main__":
    unittest.main()
