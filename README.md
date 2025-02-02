# PTT CVS Product Review Analysis

This project showcases a system that predicts product ratings based on reviews from the CVS board on PTT, using machine learning, specifically fine-tuning pre-trained models. The pre-trained models used for comparison include 'ckiplab/albert-tiny-chinese-ws', 'ckiplab/albert-base-chinese-ws', 'ckiplab/bert-base-chinese-ws', and 'google/bert-base-chinese'.

## Project Overview
* **Data Collection**: This project crawls product reviews from the CVS board of PTT, a popular bulletin board system in Taiwan. The crawler collects product names, links, stores, ratings, and user reviews.
* **Model Training**: The reviews and ratings are used to fine-tune several pre-trained models: albert-tiny-chinese-ws (a smaller version of ALBERT), ckiplab/albert-base-chinese-ws (the base version of ALBERT), ckiplab/bert-base-chinese-ws (a base variant of BERT), and google/bert-base-chinese (one of the most popular Chinese models). The CKIP models are trained in Traditional Chinese, which aligns with most of the review content, while the Google BERT model is widely recognized for its strong performance in Chinese NLP tasks. I fine-tune these models using the reviews to predict product ratings.
* **Evaluation**: The models' performance is evaluated using Mean Squared Error (MSE) and R-squared (R2). Training progress is monitored using TensorBoard.
 
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
The dataset is collected through web scraping from the PTT CVS board, a popular online forum in Taiwan. I use Python's requests library to fetch the pages, and BeautifulSoup to parse the HTML content. The scraper specifically targets posts that start with "[商品]", indicating that they are product-related discussions.

The following information is extracted from each post:
* Product name and price
* Store/Brand Name
* User rating
* User review
* Page link
  
To ensure robust data collection, we implement retries to handle connection issues and prevent overloading the server.

### Data Cleaning
After collecting the raw data, several cleaning steps are performed on the product reviews to ensure quality:
1. **Removing URLs**: URLs (mainly image links) are removed from the review text to avoid unnecessary clutter.
2. **Standardizing Store Names**: Store names are standardized into common names (e.g., "7-11", "全家").
3. **Removing Unwanted Text**: Certain phrases, such as disclaimers and promotional statements, are removed to focus on the core content.
4. **Extracting Ratings**: The product ratings are extracted, ensuring they fall within a valid range (0-100).
5. **Cleaning Reviews**: Unnecessary spaces, newlines, and unwanted text are removed from the reviews to ensure they are clean and readable.

In order to achieve our goal of predicting product ratings, only Review and Rating are used in model training.

## Model Training

### Model Selection and Initialization
In this project, we fine-tuned four pre-trained ALBERT and BERT models for the regression task:
- **albert-tiny-chinese-ws**: A lightweight, smaller variant of ALBERT.
- **ckiplab/albert-base-chinese-ws**: A larger, base variant of ALBERT.
- **ckiplab/bert-base-chinese-ws**: Base variant of BERT.
- **google/bert-base-chinese**: Google BERT base model.
BERT is a pre-trained NLP model initially introduced by Google. It is a large model that leverages a bidirectional Transformer architecture to capture the context of words from both the left and the right sides. While BERT achieves excellent performance on a variety of NLP tasks, its large size makes it computationally expensive.

ALBERT (A Lite BERT) is a smaller, more efficient variant of BERT. ALBERT reduces the model size by sharing parameters across layers, which significantly reduces the total number of parameters compared to BERT. Despite this reduction in size, ALBERT aims to match or even surpass BERT's performance on certain tasks. This efficiency is achieved through techniques like parameter sharing and factorized embedding parameterization, allowing ALBERT to maintain strong performance while being more computationally efficient.

### Model Structure Adjustment
Since this is a regression task, the final layers of all models were replaced with a linear layer appropriate for regression. The final layer outputs a single value, representing the predicted score for the product review.

### Training and Evaluation
The models were trained using HuggingFace Transformers, and training progress was monitored via TensorBoard. Early stopping was implemented with a patience of 2 epochs to avoid unnecessary computation and prevent overfitting, which ensured that models stopped training once they reached a plateau in validation performance. Training results for all models were evaluated based on:
- **Training Loss**
- **Validation Loss**
- **Mean Squared Error (MSE)**
- **R-squared (R2)**

### Model Comparison and Results

#### **Tiny Model (`ckiplab/albert-tiny-chinese-ws`)**
The **tiny model** demonstrated a rapid decrease in training loss from 1.0466 to 0.1079 over 7 epochs. However, it showed clear signs of **overfitting**, as the validation loss decreased from 0.8678 to 0.7109, and the MSE showed diminishing improvements across epochs. 

| Epoch | Training Loss | Validation Loss | MSE    | R2     |
|-------|---------------|-----------------|--------|--------|
| 1     | 1.0466        | 0.8678          | 0.8678 | 0.1135 |
| 2     | 0.8377        | 0.7559          | 0.7559 | 0.2278 |
| 3     | 0.6353        | 0.7577          | 0.7577 | 0.2260 |
| 4     | 0.4008        | 0.7263          | 0.7263 | 0.2580 |
| 5     | 0.2420        | 0.6836          | 0.6836 | 0.3017 |
| 6     | 0.1733        | 0.7007          | 0.7007 | 0.2842 |
| 7     | 0.1079        | 0.7109          | 0.7109 | 0.2738 |

#### **Base Model (`ckiplab/albert-base-chinese-ws`)**
The **base model** performed significantly better than the tiny model, with the training loss dropping from 1.0879 to 0.0764. More importantly, the validation loss decreased from 0.7929 to 0.5285, indicating better generalization. From the 3rd epoch onwards, the rate of improvement slowed, with diminishing returns on both the training and validation loss. This suggests that **early stopping** was effective in preventing further overfitting, and training could have been stopped earlier for an optimal result.

| Epoch | Training Loss | Validation Loss | MSE    | R2     |
|-------|---------------|-----------------|--------|--------|
| 1     | 1.0879        | 0.7929          | 0.7929 | 0.1900 |
| 2     | 0.6558        | 0.6462          | 0.6462 | 0.3399 |
| 3     | 0.5119        | 0.8537          | 0.8537 | 0.1278 |
| 4     | 0.2953        | 0.5346          | 0.5346 | 0.4539 |
| 5     | 0.2177        | 0.5197          | 0.5197 | 0.4691 |
| 6     | 0.1346        | 0.5378          | 0.5378 | 0.4506 |
| 7     | 0.0764        | 0.5285          | 0.5285 | 0.4601 |

#### **BERT Model (`ckiplab/bert-base-chinese-ws`)**
The **BERT model** showed the most consistent improvement in both training and validation loss, with a training loss dropping from 0.9133 to 0.1467. The validation loss also decreased from 0.5979 to 0.4766. The **R2 score** remained high, indicating strong generalization.

| Epoch | Training Loss | Validation Loss | MSE    | R2     |
|-------|---------------|-----------------|--------|--------|
| 1     | 0.9133        | 0.5979          | 0.5979 | 0.3892 |
| 2     | 0.6050        | 0.5964          | 0.5964 | 0.3907 |
| 3     | 0.4737        | 0.5990          | 0.5990 | 0.3881 |
| 4     | 0.2897        | 0.4497          | 0.4497 | 0.5406 |
| 5     | 0.2016        | 0.5614          | 0.5614 | 0.4265 |
| 6     | 0.1467        | 0.4766          | 0.4766 | 0.5131 |

#### **Google BERT (`google/bert-base-chinese`)**
The **Google BERT** model exhibited strong performance, with the training loss dropping from 0.7514 to 0.1815, and the validation loss decreasing from 0.6246 to 0.4544. The **R2 score** peaked at 0.5886 in epoch 4, showing good performance overall.

| Epoch | Training Loss | Validation Loss | MSE    | R2     |
|-------|---------------|-----------------|--------|--------|
| 1     | 0.7514        | 0.6246          | 0.6246 | 0.3619 |
| 2     | 0.5945        | 0.6337          | 0.6337 | 0.3526 |
| 3     | 0.4973        | 0.4710          | 0.4710 | 0.5188 |
| 4     | 0.3020        | 0.4027          | 0.4027 | 0.5886 |
| 5     | 0.2426        | 0.4609          | 0.4609 | 0.5292 |
| 6     | 0.1815        | 0.4544          | 0.4544 | 0.5358 |

### Conclusion:
- **Tiny Model (`albert-tiny-chinese-ws`)**: Showed overfitting with a significant gap between training and validation loss. The MSE improvement was minimal, and the model's performance stabilized after the 3rd epoch.
- **Base Model (`ckiplab/albert-base-chinese-ws`)**: Outperformed the tiny model with substantial decreases in both training and validation loss. The model showed better generalization, though improvements slowed after the 3rd epoch. **Early stopping** helped prevent overfitting by halting training early when further improvements became marginal.
- **BERT Model (`ckiplab/bert-base-chinese-ws`)**: Performed consistently well with a steady decrease in both training and validation loss. The model showed strong generalization with high R2 scores.
- **Google BERT (`google/bert-base-chinese`)**: Delivered strong results with steady improvement and good generalization, especially with the highest R2 score in epoch 4.

<img width="1308" alt="image" src="https://github.com/user-attachments/assets/5682ed9b-fc09-40d4-b294-c439df7f20ea" />

In summary, the **Google BERT** and **BERT base** models showed the best overall performance, suggesting that fine-tuning these models for additional epochs and hyperparameter tuning could yield even better results.

## Evaluation
Evaluation is done using the Mean Squared Error (MSE) and R-squared (R2) metrics. Both models are evaluated using these metrics, and the results are monitored throughout the training process.

### Prerequisites
* Python 3.x
* Colab (for GPU if needed)
