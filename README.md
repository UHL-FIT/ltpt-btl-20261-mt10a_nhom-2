[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-QmD8cHQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23869451&assignment_repo_type=AssignmentRepo)

# Real-time Currency Tracker Pro 💱

Ứng dụng Desktop quản lý tỷ giá tiền tệ theo thời gian thực được xây dựng bằng Python và CustomTkinter. Phần mềm áp dụng chuẩn mô hình MVC (Model-View-Controller) giúp dễ dàng bảo trì và mở rộng.

## ✨ Tính năng nổi bật
1. **Theo dõi tỷ giá thời gian thực**: Lấy dữ liệu tỷ giá tự động từ ExchangeRate-API chạy ngầm mỗi 30 giây mà không làm đơ ứng dụng.
2. **Giao diện hiện đại (Dark Mode)**: Sử dụng CustomTkinter cung cấp trải nghiệm mượt mà, tối màu hiện đại với bảng dữ liệu hiển thị trực quan.
3. **Thống kê chuyên sâu**: Tự động tính toán các chỉ số thống kê tài chính như Tỷ giá trung bình (Avg), Thấp nhất (Min), Cao nhất (Max) và Độ biến động (Volatility) nhờ sức mạnh của thư viện `pandas`.
4. **Biểu đồ trực quan**: Vẽ đồ thị biến động tỷ giá theo thời gian thực (Line chart) thông qua thư viện `matplotlib`.
5. **Quản lý dữ liệu linh hoạt**: Lưu trữ lịch sử vĩnh viễn trên cơ sở dữ liệu `SQLite` và hỗ trợ xuất dữ liệu ra file `.csv` chỉ với một cú click.

## 📂 Cấu trúc Dự án (MVC Architecture)
```
currency_tracker_pro/
├── controllers/             # Logic điều hướng và trung gian (app_controller.py)
├── models/                  # Quản lý Database SQLite và thao tác Pandas (database.py)
├── services/                # Background Worker xử lý gọi API (api_service.py)
├── views/                   # Giao diện chính và các cửa sổ phụ (main_gui.py, components.py)
├── main.py                  # Entry point (Khởi chạy ứng dụng)
├── requirements.txt         # Khai báo các thư viện Python
├── README.md                # Tài liệu dự án (bạn đang đọc)
├── SRS.md                   # Đặc tả Yêu cầu Hệ thống
└── SAD.md                   # Thiết kế Kiến trúc Phần mềm
```

## 🛠 Hướng dẫn cài đặt và sử dụng

### 1. Khởi tạo môi trường
Dự án cung cấp sẵn file `setup_env.bat` (dành cho Windows). Nhấp đúp chuột để tự động tạo môi trường ảo `.venv` và tải tất cả các thư viện cần thiết.
Hoặc cài đặt thủ công bằng lệnh:
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
Mở Terminal tại thư mục gốc của dự án và chạy:
```bash
python main.py
```

### 3. Đóng gói ra File Thực thi (.exe)
Bạn có thể chạy script `build.bat` để sử dụng `PyInstaller` biên dịch ứng dụng thành file `.exe` hoạt động độc lập (nếu có yêu cầu).

## 👥 Nhóm phát triển (Nhóm 2)
* **Trần Trung Hiếu** - Xây dựng kiến trúc MVC, thiết kế cơ sở dữ liệu, phát triển giao diện GUI.
* *(Ghi chú: Nếu nhóm có thêm thành viên, hãy bổ sung tên và MSSV tại đây)*

---
*Dự án Bài tập lớn - Môn Lập trình Python.*
