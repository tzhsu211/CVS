# PTT CVS Product Review Analysis

This project demonstrates a system for predicting product ratings based on reviews from PTT's CVS board using machine learning, specifically fine-tuning a pre-trained model. The tokenizer model used in this project is 'bert-base-chinese' and pre-trained model is 'ckiplab/albert-tiny-chinese-ws' which is a variant of ALBERT for Traditional Chinese text.

## Project Overview
* **Data Collection**: This project crawls product reviews from the CVS board of PTT, a popular bulletin board system in Taiwan. The crawler collects product names, links, stores, ratings, and user reviews.

* **Model Training**: The reviews and ratings are used to fine-tune a model based on the pre-trained ALBERT model (fine-tuned on traditional Chinese data by the CKIP Lab). The model learns to predict ratings from the reviews.

* **Evaluation**: The model's performance is evaluated using Mean Squared Error (MSE), and training progress is monitored via TensorBoard.

* **Dockerized Setup**: The entire environment is packaged into a Docker container, making it easy to set up, run, and scale the application.

