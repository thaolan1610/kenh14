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
## kênh14_scraper.py
1. Import thư viện:
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import schedule
import datetime
2. Khai báo đường dẫn gốc
BASE_URL = "https://kenh14.vn"
CATEGORY_PATH = "/xa-hoi.chn"
3. Lấy link bài viết trên một trang
   def get_articles_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("div", class_="knswli-right"):
        title_tag = item.find("h3")
        if title_tag and title_tag.a:
            title = title_tag.get_text(strip=True)
            link = urljoin(BASE_URL, title_tag.a["href"])
            articles.append({"title": title, "url": link})
    return articles
4. Lấy nội dung chi tiết từng bài viết
def get_article_details(article):
    url = article.get("url")
    if not url:
        print("❌ Bỏ qua vì thiếu URL:", article)
        return {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
-Kiểm tra URL bài viết.
+Lấy nội dung HTML của bài viết.
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
+Lấy phần mô tả từ thẻ <meta name="description">.
    image_url = ""
    image_meta = soup.find("meta", property="og:image")
    if image_meta:
        image_url = image_meta.get("content", "")
+lấy ảnh đại diện bài viết từ thẻ <meta property="og:image">
    content = ""
    content_div = soup.find("div", class_="knc-content")
    if content_div:
        paragraphs = content_div.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
+Lấy nội dung văn bản trong bài viết, từ các thẻ <p> bên trong <div class="knc-content">.
    return {
        "Tiêu đề": article["title"],
        "Mô tả": description,
        "Hình ảnh": image_url,
        "Nội dung": content,
        "URL": article["url"]
    }
+Trả về một dict chứa toàn bộ thông tin bài viết.
5. Thu thập nhiều trang và lưu file Excel
  def collect_data():
    full_data = []
    max_pages = 5
+Thu thập từ 5 trang đầu tiên của chuyên mục Xã hội.
    for page in range(1, max_pages + 1):
        url = f"https://kenh14.vn/xa-hoi/trang-{page}.chn"
        print(f"📄 Đang lấy dữ liệu trang {page}: {url}")
        try:
            articles = get_articles_from_page(url)
            if not articles:
                print("✅ Không còn bài viết nào, dừng lại.")
                break
            for article in articles:
                detail = get_article_details(article)
                if detail:
                    full_data.append(detail)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Lỗi ở trang {page}: {e}")
+Lặp qua từng trang.
+Lấy danh sách bài viết và nội dung chi tiết từng bài.
+Lấy danh sách bài viết và nội dung chi tiết từng bài.
    if full_data:
        df = pd.DataFrame(full_data)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        excel_filename = f"kenh14_xahoi_{timestamp}.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"✅ Đã lưu {len(full_data)} bài viết vào {excel_filename}")
    else:
        print("⚠️ Không có bài viết nào.")
+Tạo file .xlsx chứa toàn bộ dữ liệu.
6. Thiết lập công việc theo lịch
def job():
    print(f"🕕 [{datetime.datetime.now()}] Bắt đầu thu thập dữ liệu Kenh14...")
    collect_data()
7. Chạy chính: tự động mỗi ngày
if __name__ == "__main__":
    schedule.every().day.at("22:17").do(job)  # Hoặc "06:00"
    job()  # Chạy ngay khi khởi động
    while True:
        schedule.run_pending()
        time.sleep(60)
+Gọi job()lần đầu tiên.
+Sau đó cứ 1 phút kiểm tra nếu tới lịch thì chạy lại.
## Tự động thu thập mỗi ngày
Sau khi chạy script, chương trình sẽ tự động:

Thu thập bài viết từ 5 trang đầu của chuyên mục Xã hội.

Tạo file Excel chứa toàn bộ dữ liệu.

Lập lịch chạy hàng ngày lúc 06:00 sáng (có thể thay đổi theo nhu cầu).
## Cách chạy chương trình
python kenh14_scraper.py




