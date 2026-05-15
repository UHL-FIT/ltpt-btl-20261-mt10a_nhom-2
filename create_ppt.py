from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Tạo Presentation
prs = Presentation()

def add_slide(title_text, content_bullets):
    # Layout 1 là Title and Content
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    
    # Set Title
    title = slide.shapes.title
    title.text = title_text
    
    # Set Content
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = content_bullets[0]
    
    for bullet in content_bullets[1:]:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0

# Slide 1: Title Slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "BÁO CÁO TIẾN ĐỘ DỰ ÁN\nReal-time Currency Tracker Pro"
subtitle.text = "Môn học: Lập trình Python\nThực hiện: Nhóm 2\nGiảng viên: Vũ Duy Sơn"

# Mảng dữ liệu các slide tiếp theo
slides_data = [
    {
        "title": "1. Mục tiêu dự án",
        "bullets": [
            "Xây dựng ứng dụng Desktop bằng Python giúp theo dõi tỷ giá ngoại tệ trực tuyến.",
            "Áp dụng kiến thức: OOP, Multi-threading, phân tích dữ liệu (Pandas), giao diện (CustomTkinter).",
            "Tuân thủ chặt chẽ mô hình thiết kế phần mềm MVC (Model - View - Controller)."
        ]
    },
    {
        "title": "2. Đã làm được gì? (Tổng quan)",
        "bullets": [
            "Hoàn thành 100% Core System: Xây dựng xong bộ khung ứng dụng.",
            "Cấu trúc thư mục chuẩn MVC: Phân tách rõ ràng Model, View, Controller.",
            "Tích hợp SQLite để lưu trữ lịch sử tỷ giá vĩnh viễn.",
            "Hoàn thiện tài liệu kiến trúc (SAD.md), yêu cầu (SRS.md) và nộp Github Classroom."
        ]
    },
    {
        "title": "3. Đã làm được gì? (Tính năng)",
        "bullets": [
            "Thiết kế giao diện Dark Mode chuyên nghiệp, thân thiện.",
            "Quản lý danh sách các mã ngoại tệ chuẩn ISO (Thêm/Sửa/Xóa).",
            "Tích hợp Pandas tính: Giá trung bình, cao nhất, thấp nhất và biến động.",
            "Đóng gói phần mềm ra file .exe chạy độc lập."
        ]
    },
    {
        "title": "4. Khó khăn gặp phải (Kỹ thuật)",
        "bullets": [
            "Khó khăn: Giao diện ứng dụng bị đơ khi gọi API lấy dữ liệu trên luồng chính.",
            "Khắc phục: Nhóm nghiên cứu sử dụng thư viện threading, đưa tác vụ gọi API xuống chạy ngầm (Background Worker) để không ảnh hưởng UX."
        ]
    },
    {
        "title": "5. Khó khăn gặp phải (Quy trình)",
        "bullets": [
            "Khó khăn: Xung đột code (Merge Conflicts) khi tải file bài mẫu từ Github về. Lỗi PyInstaller không build được do conflict markers.",
            "Khắc phục: Dùng lệnh Git xử lý xung đột, sửa file main.py và build thành công .exe."
        ]
    },
    {
        "title": "6. Kế hoạch tiếp theo (Tối ưu)",
        "bullets": [
            "Tinh chỉnh khoảng cách giao diện để phù hợp đa kích thước màn hình.",
            "Tối ưu hoá RAM khi tải hàng nghìn bản ghi vào biểu đồ Matplotlib.",
            "Bổ sung hiệu ứng chuyển động mượt mà hơn cho Splash Screen."
        ]
    },
    {
        "title": "7. Kế hoạch tiếp theo (Mở rộng)",
        "bullets": [
            "Tính năng Cảnh báo (Alert): Đổi màu đỏ/cam khi tỷ giá vượt ngưỡng nhất định.",
            "Mini-Calculator: Thêm công cụ máy tính nhỏ ở Sidebar để người dùng nhập số tiền và đổi trực tiếp theo tỷ giá thực."
        ]
    },
    {
        "title": "8. Kết luận & Hỏi đáp",
        "bullets": [
            "Dự án hiện đã hoàn thiện toàn bộ các chức năng cốt lõi theo đề bài.",
            "Xin cảm ơn thầy và các bạn đã lắng nghe!",
            "Nhóm xin phép nhận góp ý và câu hỏi từ mọi người."
        ]
    }
]

for slide_info in slides_data:
    add_slide(slide_info["title"], slide_info["bullets"])

prs.save('BaoCaoTienDo.pptx')
print("Tạo file BaoCaoTienDo.pptx thành công!")
