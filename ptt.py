import pandas as pd
import re, time, requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("always")

def remove_url(text:str) -> str:
    '''
    remove all the urls in content (mainly pics)
    '''
    
    url_pattern = r'http[s]?://[^\s]+'
    
    modified_text = re.sub(url_pattern, '', text)
    modified_text = re.sub(r"\n+", "\n", modified_text)
    
    return modified_text

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
    
def score(text:str):
    '''
    Extract score from text (returns the number score).
    '''
    score_ = re.sub(r"\(未滿60分為不推薦\)", "", text)
    score_ = re.search(r"(\d+)", score_)
    
    if score_:
        return score_.group(1)
    return None
    
    
def title(text: str) -> str:
    '''
    Clean data (e.g., remove unwanted text like "區域型商品請註明").
    '''
    modified_text = re.sub(r"\(區域型商品請註明 試吃試用品請標示價格0元\)", "", text)
    return modified_text

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
        if len(price)<3:
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
    
    review_section = re.search(r"【心得】：\s*?(.*?)--\n", content, re.DOTALL)
    if review_section:
        review_text = review_section.group(1).strip() if review_section else ''
        review_text = remove_url(review_text).strip()
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
    else:
        return None
    
if __name__ == '__main__':
    base_url = "https://www.ptt.cc/bbs/CVS/index{}.html"
    data = []
    for page_num in tqdm(range(3100, 3150)):
        article_links = fetch_article(page_num, base_url)
            
        for link in article_links:
            product_data = product_details(link = link)
            if product_data:
                data.append(product_data)
        
        time.sleep(1)  # Sleep between requests to avoid overloading the server
        
        # Save the data to a CSV file
        df = pd.DataFrame(data)
        df.to_csv('cvs_products.csv', index=False, encoding='utf-8')
        print("Data saved: cvs_products.csv")

        