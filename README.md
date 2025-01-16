# PTT CVS Product Review Analysis

This project demonstrates a system for predicting product ratings based on reviews from PTT's CVS board using machine learning, specifically fine-tuning a pre-trained model. The tokenizer model used in this project is 'bert-base-chinese' and the pre-trained model is 'ckiplab/albert-tiny-chinese-ws', a variant of ALBERT for Traditional Chinese text.

## Project Overview
* **Data Collection**: This project crawls product reviews from the CVS board of PTT, a popular bulletin board system in Taiwan. The crawler collects product names, links, stores, ratings, and user reviews.

* **Model Training**: The reviews and ratings are used to fine-tune a model based on the pre-trained ALBERT model (fine-tuned on traditional Chinese data by the CKIP Lab). The model learns to predict ratings from the reviews.
 
* **Evaluation**: The model's performance is evaluated using Mean Squared Error (MSE), and training progress is monitored via TensorBoard.

* **Dockerized Setup**: The entire environment is packaged into a Docker container, making it easy to set up, run, and scale the application.
 
## Dataset
This dataset is collected from the [商品] posts on the PTT CVS board using web scraping. It contains user reviews of convenience store products along with corresponding ratings. Each entry includes the product name, price, store name, product specifications, caloric content, rating, and the user's review. This dataset is intended for predicting ratings based on the review content.

* **Product name/price 商品名稱/價格**: The name of the product and its price.
* **Link 頁面連結**: The link to the product review page.
* **Store/Brand Name 便利商店/廠商名稱**: The convenience store or brand where the product is sold.
* **Rating 評分**: The user's rating for the product (range: 0-100, with ratings below 60 being a recommendation to avoid).
* **Review 心得**: The user's detailed review, often including text and possibly image links.

Below is an example of the dataset:

* **Product name/price**: 素花枝丸/49NTD
* **Link**: https://www.ptt.cc/bbs/CVS/M.1570728137.A.0E7.html
* **Store/Brand Name**: 7-11
* **Rating**: 85
* **Review**: 好吃不油膩，缺點是有點貴！希望未來出更多素食產品~~

## Data Collection and Cleaning

### Data Collection (Web Scraping)
The dataset is collected through web scraping from the PTT CVS board, a popular online forum in Taiwan. We use Python's requests library to fetch the pages, and BeautifulSoup to parse the HTML content. The scraper specifically targets posts that start with "[商品]", indicating that they are product-related discussions.

The following information is extracted from each post:
* Product name and price
* Store/Brand Name
* User rating
* User review
* Page link
  
To ensure robust data collection, we use retries to handle connection issues and avoid overloading the server.

### Data Cleaning
After collecting the raw data, several cleaning steps are performed on the product reviews to ensure quality:
1. **Removing URLs**: URLs (mainly image links) are removed from the review text to avoid unnecessary clutter.
2. **Standardizing Store Names**: Store names are standardized into common names (e.g., "7-11", "全家").
3. **Removing Unwanted Text**: Certain phrases, such as disclaimers and promotional statements, are removed to focus on the core content.
4. **Extracting Ratings**: The product ratings are extracted, ensuring they fall within a valid range (0-100).
5. **Cleaning Reviews**: Unnecessary spaces, newlines, and unwanted text are removed from the reviews to ensure they are clean and readable.

## Model Training

## Evaluation

## Dockerized Setup

   
## Setup and Installation
### Prerequisites
* Python 3.x
* Docker (for Dockerized setup)
