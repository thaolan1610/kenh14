import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import schedule

BASE_URL = "https://kenh14.vn"
CATEGORY_PATH = "/xa-hoi.chn"

# Lấy link từng bài viết trên 1 trang
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

# Lấy thông tin chi tiết từng bài viết
def get_article_details(article):
    url = article.get("url")
    if not url:
        print("❌ Bỏ qua vì thiếu URL:", article)
        return {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Mô tả từ <meta name="description">
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""

    # Ảnh bài viết
    image_url = ""
    image_meta = soup.find("meta", property="og:image")
    if image_meta:
        image_url = image_meta.get("content", "")

    # Nội dung bài viết
    content = ""
    content_div = soup.find("div", class_="knc-content")
    if content_div:
        paragraphs = content_div.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

    return {
        "Tiêu đề": article["title"],
        "Mô tả": description,
        "Hình ảnh": image_url,
        "Nội dung": content,
        "URL": article["url"]
    }

# Thu thập và lưu dữ liệu từ nhiều trang
def collect_data():
    full_data = []
    max_pages = 5  # 👉 Có thể thay đổi số trang cần quét

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
            time.sleep(1)  # ⏳ nghỉ giữa các trang
        except Exception as e:
            print(f"❌ Lỗi ở trang {page}: {e}")

    if full_data:
        df = pd.DataFrame(full_data)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"kenh14_xahoi_{timestamp}.csv"
        excel_filename = f"kenh14_xahoi_{timestamp}.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"✅ Đã lưu {len(full_data)} bài viết vào {excel_filename}")

    else:
        print("⚠️ Không có bài viết nào.")

# Lập lịch hoặc chạy thử ngay
def job():
    print("🕕 Bắt đầu thu thập dữ liệu Kenh14...")
    collect_data()

if __name__ == "__main__":
     #Chạy mỗi ngày lúc 6h sáng:
    schedule.every().day.at("6:00").do(job)

    while True:
        schedule.run_pending()  # Kiểm tra nếu có tác vụ nào cần thực hiện
        time.sleep(60)  # Đợi 1 phút trước khi kiểm tra lại
    


    