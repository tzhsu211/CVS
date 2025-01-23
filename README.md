# PTT CVS Product Review Analysis

This project demonstrates a system for predicting product ratings based on reviews from PTT's CVS board using machine learning, specifically fine-tuning a pre-trained model. The tokenizer model used in this project is 'bert-base-chinese' and the pre-trained models used for comparison are 'ckiplab/albert-tiny-chinese-ws' and 'ckiplab/albert-base-chinese-ws'.

## Project Overview
* **Data Collection**: This project crawls product reviews from the CVS board of PTT, a popular bulletin board system in Taiwan. The crawler collects product names, links, stores, ratings, and user reviews.

* **Model Training**: The reviews and ratings are used to fine-tune two pre-trained models: `albert-tiny-chinese-ws` (a small version of ALBERT) and `ckiplab/albert-base-chinese-ws` (a base version of ALBERT). The models are fine-tuned on the reviews to predict product ratings.
 
* **Evaluation**: The model's performance is evaluated using Mean Squared Error (MSE) and R-squared (R2). Training progress is also monitored via TensorBoard.

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

### Model Selection and Initialization
In this project, we fine-tune two pre-trained ALBERT models for the regression task:
- **albert-tiny-chinese-ws**: A lightweight, smaller variant of ALBERT.
- **ckiplab/albert-base-chinese-ws**: A larger, base variant of ALBERT.

Both models use the **bert-base-chinese** tokenizer for tokenization. We aim to compare the impact of model size (tiny vs. base) on regression performance for predicting product ratings from reviews.

### Model Structure Adjustment
Since this is a regression task, both models' final layers are replaced with a linear layer suitable for regression. The last layer outputs a single value representing the predicted score for the product review.

### Training and Evaluation
The models were trained using Hugging Face Transformers, and the training progress was monitored via TensorBoard. Training results for both models were evaluated based on:
- **Training Loss**
- **Validation Loss**
- **Mean Squared Error (MSE)**
- **R-squared (R2)**

## Model Comparison and Results

### Tiny Model (`albert-tiny-chinese-ws`)
The **tiny model** demonstrated a rapid decrease in training loss from 0.8447 to 0.0869 over 6 epochs. However, it showed clear signs of **overfitting**, as the validation loss only decreased from 0.88 to 0.7, and the MSE showed diminishing improvement across epochs.

| Epoch | Training Loss | Validation Loss | MSE   | R2    |
|-------|---------------|-----------------|-------|-------|
| 1     | 0.8447        | 0.8883          | 0.8883 | 0.0926 |
| 2     | 0.7168        | 0.6970          | 0.6970 | 0.2880 |
| 3     | 0.5550        | 0.6762          | 0.6762 | 0.3092 |
| 4     | 0.2410        | 0.7097          | 0.7097 | 0.2750 |
| 5     | 0.1484        | 0.7290          | 0.7290 | 0.2552 |
| 6     | 0.0869        | 0.7035          | 0.7035 | 0.2814 |

### Base Model (`ckiplab/albert-base-chinese-ws`)
The **base model** performed significantly better than the tiny model, with the training loss dropping from 0.7595 to 0.0827. More importantly, the validation loss decreased from 0.6957 to around 0.47, indicating better generalization. However, from the 3rd epoch onwards, progress slowed, and performance improvements became marginal, suggesting that **early stopping** could be beneficial.

| Epoch | Training Loss | Validation Loss | MSE   | R2    |
|-------|---------------|-----------------|-------|-------|
| 1     | 0.7595        | 0.6957          | 0.6957 | 0.2893 |
| 2     | 0.6043        | 0.6403          | 0.6403 | 0.3459 |
| 3     | 0.4923        | 0.4826          | 0.4826 | 0.5070 |
| 4     | 0.2478        | 0.4521          | 0.4521 | 0.5382 |
| 5     | 0.1350        | 0.4772          | 0.4772 | 0.5125 |
| 6     | 0.0827        | 0.4712          | 0.4712 | 0.5187 |

### Conclusion:
- **Tiny Model**: Showed overfitting, with a significant gap between training and validation loss. MSE improvement was minimal, and the model's performance stabilized after the 3rd epoch.
- **Base Model**: Outperformed the tiny model with a substantial decrease in both training and validation loss. The model's validation performance suggests better generalization, though further improvement was limited after the 3rd epoch. **Early stopping** could be explored to avoid overfitting.

## Evaluation
The evaluation is done using the Mean Squared Error (MSE) and R-squared (R2) metrics. Both models are evaluated using these metrics, and the results are monitored throughout the training process.

## Dockerized Setup

   
## Setup and Installation
### Prerequisites
* Python 3.x
* Docker (for Dockerized setup)
