# Kenh14 Scraper

Công cụ thu thập dữ liệu từ chuyên mục **Xã hội** của trang [Kenh14.vn](https://kenh14.vn/xa-hoi.chn) và lưu vào file CSV.

##Tính năng
Thu thập tiêu đề, mô tả, nội dung và ảnh đại diện từ các bài viết.

Lưu dữ liệu vào file Excel .

Tự động chạy hàng ngày lúc 6:00 sáng.


## Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (trình quản lý gói Python)

## Cài đặt

1. **Clone project về máy:**

git clone https://github.com/your-username/kenh14-scraper.git
cd kenh14-scraper
2.Cài đặt các thư viện cần thiết:
pip install -r requirements.txt
3. Nếu muốn xuất ra file .xlsx, cần cài thêm:
pip install openpyxl

## File requirements.txt
requests
beautifulsoup4
pandas
schedule
openpyxl
## Tự động thu thập mỗi ngày
Sau khi chạy script, chương trình sẽ tự động:

Thu thập bài viết từ 5 trang đầu của chuyên mục Xã hội.

Tạo file Excel chứa toàn bộ dữ liệu.

Lập lịch chạy hàng ngày lúc 06:00 sáng (có thể thay đổi theo nhu cầu).
## Cách chạy chương trình
python kenh14_scraper.py




