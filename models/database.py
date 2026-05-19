import sqlite3
import pandas as pd
import numpy as np
import datetime
import os

class Database:
    def __init__(self, db_path="currency_data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Khởi tạo cơ sở dữ liệu và các bảng cần thiết."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng lưu các cặp tiền tệ đang theo dõi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency TEXT NOT NULL,
                target_currency TEXT NOT NULL,
                UNIQUE(base_currency, target_currency)
            )
        ''')
        
        # Bảng lưu lịch sử tỷ giá
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rate REAL NOT NULL,
                FOREIGN KEY (pair_id) REFERENCES pairs (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_pair(self, base, target):
        """Thêm một cặp tiền tệ mới vào danh sách theo dõi."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs (base_currency, target_currency) VALUES (?, ?)", (base.upper(), target.upper()))
            conn.commit()
            return True, "Thêm thành công."
        except sqlite3.IntegrityError:
            return False, "Cặp tiền tệ này đã tồn tại."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
            
    def remove_pair(self, base, target):
        """Xóa một cặp tiền tệ khỏi danh sách."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Xóa lịch sử trước
            cursor.execute("""
                DELETE FROM history WHERE pair_id IN (
                    SELECT id FROM pairs WHERE base_currency = ? AND target_currency = ?
                )
            """, (base.upper(), target.upper()))
            # Xóa cặp tiền
            cursor.execute("DELETE FROM pairs WHERE base_currency = ? AND target_currency = ?", (base.upper(), target.upper()))
            conn.commit()
            return True, "Xóa thành công."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def get_all_pairs(self):
        """Lấy danh sách tất cả các cặp tiền tệ."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, base_currency, target_currency FROM pairs")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_history(self, pair_id, rate):
        """Thêm bản ghi lịch sử tỷ giá cho một cặp tiền."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (pair_id, rate) VALUES (?, ?)", (pair_id, rate))
        conn.commit()
        conn.close()

    def get_statistics(self):
        """
        Sử dụng Pandas để tính toán thống kê (Avg, Min, Max, Volatility)
        Trả về dictionary dạng {pair_name: {'rate': current, 'avg': avg, 'min': min, 'max': max, 'volatility': vol}}
        """
        conn = sqlite3.connect(self.db_path)
        
        # Load dữ liệu vào DataFrame
        query = '''
            SELECT p.base_currency || '/' || p.target_currency AS pair_name,
                   h.rate, h.timestamp
            FROM history h
            JOIN pairs p ON h.pair_id = p.id
            ORDER BY h.timestamp ASC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return {}

        stats = {}
        # Nhóm theo từng cặp tiền
        for pair_name, group in df.groupby('pair_name'):
            current_rate = group['rate'].iloc[-1]
            avg_rate = group['rate'].mean()
            min_rate = group['rate'].min()
            max_rate = group['rate'].max()
            volatility = group['rate'].std() if len(group) > 1 else 0.0
            
            # Xử lý NaN cho volatility
            if pd.isna(volatility):
                volatility = 0.0
                
            stats[pair_name] = {
                'current_rate': current_rate,
                'avg_rate': avg_rate,
                'min_rate': min_rate,
                'max_rate': max_rate,
                'volatility': volatility
            }
            
        return stats

    def get_history_dataframe(self, base, target):
        """Lấy DataFrame lịch sử tỷ giá của một cặp tiền cụ thể để vẽ biểu đồ."""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT h.timestamp, h.rate
            FROM history h
            JOIN pairs p ON h.pair_id = p.id
            WHERE p.base_currency = ? AND p.target_currency = ?
            ORDER BY h.timestamp ASC
        '''
        df = pd.read_sql_query(query, conn, params=(base.upper(), target.upper()))
        conn.close()
        # Chuyển đổi cột timestamp sang kiểu datetime của pandas
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def export_to_csv(self, file_path):
        """Xuất toàn bộ lịch sử ra file CSV."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = '''
                SELECT p.base_currency, p.target_currency, h.rate, h.timestamp
                FROM history h
                JOIN pairs p ON h.pair_id = p.id
                ORDER BY h.timestamp DESC
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()
            df.to_csv(file_path, index=False)
            return True, "Xuất dữ liệu thành công."
        except Exception as e:
            return False, str(e)
            
    def import_from_csv(self, file_path):
        """Nhập danh sách các cặp tiền từ file CSV (cột base/base_currency, target/target_currency)."""
        try:
            df = pd.read_csv(file_path)
            
            # Chuẩn hóa tên cột để hỗ trợ cả 'base'/'base_currency' và 'target'/'target_currency'
            col_mapping = {}
            for col in df.columns:
                col_lower = col.lower().strip()
                if col_lower in ['base', 'base_currency']:
                    col_mapping[col] = 'base'
                elif col_lower in ['target', 'target_currency']:
                    col_mapping[col] = 'target'
            
            df = df.rename(columns=col_mapping)
            
            if 'base' not in df.columns or 'target' not in df.columns:
                return False, "File CSV phải có cột 'base' (hoặc 'base_currency') và 'target' (hoặc 'target_currency')."
            
            success_count = 0
            for _, row in df.iterrows():
                base = str(row['base']).strip()
                target = str(row['target']).strip()
                if base and target:
                    res, _ = self.add_pair(base, target)
                    if res:
                        success_count += 1
            return True, f"Đã nhập thành công {success_count} cặp tiền tệ."
        except Exception as e:
            return False, str(e)
