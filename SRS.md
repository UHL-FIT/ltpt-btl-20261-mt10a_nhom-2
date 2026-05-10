# ĐẶC TẢ YÊU CẦU HỆ THỐNG (SRS)
**Dự án:** Real-time Currency Tracker Pro  
**Nhóm thực hiện:** Nhóm 2  

---

## 1. Giới thiệu
Tài liệu này mô tả chi tiết các yêu cầu chức năng (Functional Requirements) và phi chức năng (Non-Functional Requirements) đối với phần mềm "Real-time Currency Tracker Pro". Ứng dụng giúp người dùng theo dõi và phân tích sự biến động của tỷ giá các cặp tiền tệ trên thế giới theo thời gian thực.

## 2. Đối tượng Người dùng
* **Nhà đầu tư/Cá nhân:** Những người có nhu cầu theo dõi tỷ giá ngoại tệ thường xuyên để đưa ra quyết định giao dịch, mua bán.
* **Học sinh/Sinh viên:** Quan sát sự lên xuống của các cặp tiền tệ phục vụ cho bài tập môn tài chính.

## 3. Yêu cầu Chức năng (Functional Requirements)

### 3.1. Quản lý danh sách cặp tiền tệ
* **FR1. Thêm cặp tiền:** Người dùng nhập mã tiền tệ gốc (Base) và đích (Target) dưới chuẩn ISO 3 ký tự (VD: USD, VND). Hệ thống sẽ tự động thêm và bắt đầu theo dõi.
* **FR2. Xóa cặp tiền:** Chọn và xóa các cặp tiền không còn muốn theo dõi ra khỏi màn hình chính.
* **FR3. Validation:** Bắt lỗi nếu nhập thiếu, nhập sai định dạng 3 ký tự, hoặc thêm cặp tiền đã tồn tại.

### 3.2. Cập nhật và Hiển thị Tỷ giá
* **FR4. Lấy dữ liệu thời gian thực:** Hệ thống tự động gọi API (ExchangeRate-API) để cập nhật tỷ giá mới nhất của toàn bộ danh sách đang theo dõi.
* **FR5. Chu kỳ cập nhật:** Tự động làm mới dữ liệu mỗi 30 giây (Background worker) mà không cần người dùng thao tác.
* **FR6. Bảng hiển thị (Data Table):** Cập nhật dữ liệu lên bảng (Treeview) hiển thị tỷ giá hiện tại của các cặp tiền.

### 3.3. Thống kê và Biểu đồ
* **FR7. Tính toán chỉ số:** Hệ thống sử dụng lịch sử lưu trữ để tính tỷ giá trung bình (Avg), mức giá đỉnh (Max), mức giá đáy (Min) và độ biến động tiêu chuẩn (Volatility) cho mỗi cặp tiền.
* **FR8. Trực quan hóa:** Người dùng có thể nhấn nút "Xem biểu đồ" để hiển thị một cửa sổ vẽ đường cong (Line chart) biến động tỷ giá theo các mốc thời gian đã lưu.
* **FR9. Thẻ tổng quan:** Bảng Dashboard mini hiển thị "Tổng số cặp", "Cặp tiền nóng nhất", và "Cập nhật gần nhất".

### 3.4. Lưu trữ và Xuất dữ liệu
* **FR10. Lưu trữ Database:** Tỷ giá lấy về phải được ghi lại vào cơ sở dữ liệu (SQLite) nội bộ ngay lập tức để làm cơ sở cho biểu đồ sau này.
* **FR11. Export CSV:** Cho phép người dùng xuất toàn bộ lịch sử tỷ giá (Timestamp, Base, Target, Rate) ra file CSV phục vụ cho Excel hoặc ứng dụng khác.

## 4. Yêu cầu Phi chức năng (Non-Functional Requirements)
* **NFR1. Trải nghiệm người dùng (UX/UI):** Giao diện phải hiện đại, hỗ trợ Dark Mode mặc định, không sử dụng giao diện cổ điển có sẵn của hệ điều hành. Phải có màn hình Splash Screen chờ tải dữ liệu.
* **NFR2. Hiệu năng (Performance):** Quá trình lấy API phải chạy đa luồng (Multi-threading) để giao diện chính (GUI) không bị đơ hoặc giật lag trong quá trình chờ mạng phản hồi.
* **NFR3. Khả năng bảo trì:** Mã nguồn phải được cấu trúc theo mẫu MVC.
* **NFR4. Độ ổn định:** Phải xử lý bắt lỗi ngoại lệ (Timeout, Connection Error) khi không có mạng lưới internet, ứng dụng không được phép văng (Crash).
