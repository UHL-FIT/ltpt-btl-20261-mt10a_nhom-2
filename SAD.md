# TÀI LIỆU THIẾT KẾ KIẾN TRÚC PHẦN MỀM (SAD)
**Dự án:** Real-time Currency Tracker Pro  
**Nhóm thực hiện:** Nhóm 2  

---

## 1. Mẫu Kiến trúc Hệ thống (Architectural Pattern)
Hệ thống được thiết kế hoàn toàn theo mẫu kiến trúc **MVC (Model-View-Controller)**. 
Mẫu kiến trúc này giúp phân tách rạch ròi giữa giao diện người dùng, logic nghiệp vụ, và lưu trữ dữ liệu, đáp ứng tốt cho một ứng dụng có giao diện Desktop đồ họa phức tạp.

## 2. Thiết kế Các Thành Phần (Component Design)

### 2.1. Lớp Model (`models/`)
* **Vai trò:** Quản lý toàn bộ cấu trúc dữ liệu và tương tác trực tiếp với cơ sở dữ liệu SQLite.
* **Component chính:** `Database` (`database.py`)
  * Quản lý hai bảng `pairs` (Danh sách cặp tiền) và `history` (Lịch sử tỷ giá).
  * Trích xuất dữ liệu thô từ SQLite, load vào `pandas.DataFrame` để xử lý và tính toán thống kê (Mean, Min, Max, Standard Deviation cho Volatility).
  * Xử lý thao tác Import/Export CSV.

### 2.2. Lớp View (`views/`)
* **Vai trò:** Xây dựng Giao diện người dùng (GUI) và thu thập thao tác của người dùng. Không chứa logic truy xuất database.
* **Component chính:**
  * `MainWindow` (`main_gui.py`): Màn hình chính sử dụng `customtkinter` và `tkinter.ttk.Treeview`. Hiển thị bảng tổng hợp tỷ giá và thẻ thống kê.
  * `components.py`: Chứa các thành phần UI mở rộng:
    * `SplashScreen`: Màn hình chờ tải dữ liệu.
    * `AddPairWindow`: Cửa sổ thêm mã tiền tệ.
    * `ChartWindow`: Cửa sổ nhúng thư viện `matplotlib` để render biểu đồ Line Chart trực quan.

### 2.3. Lớp Controller (`controllers/`)
* **Vai trò:** Cầu nối trung gian. Lắng nghe các sự kiện (Events) từ View, gọi Model để xử lý, và trả dữ liệu về View để cập nhật lên màn hình.
* **Component chính:** `AppController` (`app_controller.py`)
  * Khởi tạo Model và View.
  * Cung cấp các hàm handler (ví dụ: `add_pair`, `remove_pair`) mà View sẽ gọi khi người dùng bấm nút.

### 2.4. Lớp Service (`services/`)
* **Vai trò:** Xử lý các tác vụ ngoại vi, đặc biệt là các tác vụ mạng/bất đồng bộ (Asynchronous) để không làm treo giao diện.
* **Component chính:** `APIService` (`api_service.py`)
  * Chạy trên một luồng phụ (`threading.Thread`).
  * Liên tục thực hiện HTTP GET Request tới ExchangeRate-API mỗi 30 giây.
  * Gọi callback (`view.after()`) để báo hiệu Controller cập nhật View an toàn từ luồng chính.

## 3. Sơ đồ Luồng Dữ liệu (Data Flow)
1. **Background Update:** `APIService` (Thread 2) gọi API lấy JSON -> Gửi dữ liệu tỷ giá mới -> `AppController` -> Lưu vào `Model` (SQLite).
2. **GUI Refresh:** `APIService` gọi callback -> `AppController` lấy dữ liệu thống kê từ `Model` (qua `pandas`) -> Cập nhật lên `Treeview` và `Label` ở `View`.
3. **User Action (Ví dụ: Mở biểu đồ):** Người dùng chọn cặp tiền và bấm nút ở `View` -> Mở `ChartWindow` -> Lấy `DataFrame` lịch sử từ `Model` -> Render đồ thị `matplotlib`.
