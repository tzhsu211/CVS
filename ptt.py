import pandas as pd
import re, time, requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup

def review_remove(text:str) -> str:
    '''
    remove all the urls in content (mainly pics)
    '''  
    url_pattern = r'http[s]?://[^\s]+'

    remove_patterns = [
        r"(圖文內容 請務必圖文獨立 不可單獨貼網址或單獨文字內容)",
        r"與板工打勾勾約定:",
        r"此商品文之圖文皆為發文者原創，實際個人拍攝",
        r"若圖片內容為轉載，將附上出處。",
        r"針對商品之評論與評價皆建立於個人之實際體驗。",
        r"_______以上閱讀完畢Ctrl\+K刪除以示確實閱讀約定事項\\OuO。",
        r"未刪除視同未閱讀，板工保留不告知刪文之權利",
        r"===+" 
    ]
    for pattern in remove_patterns:
        text = re.sub(pattern, "", text)

    text = re.sub(url_pattern, '', text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

def store(text:str) -> str:
    '''
    Change store name to standardized version.
    '''
    s = text[0] 
    if s == '全':
        return "全家"
    elif s == '7' or s == '統' or text == '小7':
        return "7-11"
    elif s == '萊':
        return '萊爾富'
    elif s == 'o' or s== 'O' or s == "Ｏ":
        return 'OK'
    else:
        return None
    
def score(text: str):
    '''
    Extract score from text (returns the number score).
    '''
    score_ = re.sub(r"\(未滿60分為不推薦\)", "", text)
    score_ = re.search(r"(\d+)", score_)

    if score_:
        score_value = int(score_.group(1))
        if 0 <= score_value <= 100:
            return score_value
    return None
    
    
def title(text: str) -> str:
    '''
    Clean data (e.g., remove unwanted text like "區域型商品請註明").
    '''
    return re.sub(r"\(區域型商品請註明 試吃試用品請標示價格0元\)", "", text)

def fetch_page(url: str, retry_count: int):
    '''
    Fetch page with retries.
    '''
    for _ in range(retry_count):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            else:
                print(f"Error: {url} return status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error {e}, Retry...")    
        time.sleep(1)
        print(f"Failed to connect to {url}")
        return None
    
def fetch_article(page_num:int, base_url:str) -> list:
    '''
    Loop through all titles on the page and check if the title starts with "[商品]",
    if yes, append the link to a list.
    '''
    url = base_url.format(page_num)
    response = fetch_page(url= url, retry_count=3)
    if not response:
        return []
    soup = BeautifulSoup(response.text,'html.parser')
    articles = soup.find_all('div', class_ = 'r-ent')
    
    article_link = []   
    for article in articles:
        title_div = article.find('div', class_ = 'title')
        if title_div:
            title_text = title_div.get_text(strip = True)
            if title_text.startswith('[商品]'):
                link = title_div.find('a')['href']
                article_link.append(link)
    return article_link

def parse_content(content:str, article_link: str) -> dict:
    '''
    parse the product detail from the content.
    return a dict
    '''   
    product_data = {
        'product': '',
        'link':article_link,
        'store': '',
        'CVS': '',
        'rating':'',
        'review': ''
    }

    content = title(content)
    
    price_section = re.search(r"【商品名稱/價格】：\s*(.*?)\s*(?=\n|【)", content, re.DOTALL)
    if price_section and price_section.group(1).strip():
        price = price_section.group(1).strip().replace('\n\n', '\n')
        price = re.sub(r"[商品]", '', price)
        if len(price)<4:
            return None
        product_data['product'] = price

    store_section = re.search(r"【便利商店/廠商名稱】：\s*?(.+)\n", content)
    if store_section:
        store_name = store_section.group(1).strip()
        product_data['store'] = store_name
        product_data['CVS'] = store(store_name)
    
    rating_section = re.search(r"【評分】：\s*?(.*?)\n", content)
    if rating_section:
        rating = rating_section.group(1).strip() if rating_section else None
        product_data['rating'] = score(rating)
    
    review_section = re.search(r"【心得】：\s*(.*?)(?=【商品名稱/價格】|--\n)", content, re.DOTALL)
    if review_section:
        review_text = review_section.group(1).strip() if review_section else ''
        review_text = review_remove(review_text).strip()
        product_data['review'] = review_text
        
    if all(product_data[key] for key in product_data):
        return product_data    
    return None
        
def product_details(link: str):
    '''
    Fetch the page of each article and extract product details.
    '''
    article_link = f"https://www.ptt.cc{link}"
    article_response = fetch_page(article_link,3)
    if not article_response:
        return None
    
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    content = article_soup.find('div', class_ = 'bbs-screen bbs-content')
    
    if content:
        return parse_content(content.text, article_link)
    return None
    
if __name__ == '__main__':
    base_url = "https://www.ptt.cc/bbs/CVS/index{}.html"
    data = []
    total_products = 0

    for page_num in tqdm(range(2180, 3180)):
        article_links = fetch_article(page_num, base_url)
        page_products = 0
            
        for link in article_links:
            product_data = product_details(link = link)
            if product_data:
                data.append(product_data)
                page_products+=1
        
        total_products+= page_products
        print(f"\nNum of proudcts in page{page_num} :{page_products}, total num of products :{total_products}")
        time.sleep(1)  # Sleep between requests to avoid overloading the server
        
        # Save the data to a CSV file
        if page_num %10 ==0:
            df = pd.DataFrame(data)
            df.to_csv('cvs_products.csv', index=False, encoding='utf-8')
            print("Data saved: cvs_products.csv")

    print(f"All data saves, total num of products {total_products}")
    df = pd.DataFrame(data)
    df.to_csv('cvs_products.csv', index=False, encoding='utf-8')
        