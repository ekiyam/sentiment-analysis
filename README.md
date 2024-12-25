# **Real-Time Sentiment Analysis on Social Media (Airlines on Twitter)**

## **Project Description**
This project focuses on building a robust real-time sentiment analysis application using Twitter data. The aim is to empower businesses (e.g., airlines) to make data-driven decisions and gain deeper insights into customer behavior by analyzing sentiment trends in tweets.

The application processes real-time data, classifies tweets into positive, negative, or neutral sentiments, and visualizes the results with interactive graphs. By utilizing a combination of traditional machine learning, deep learning, and advanced text representation methods, this project achieves highly accurate and optimized predictions.

---

## **Key Features**

### **1. Real-Time Data Collection**
- The script `sa.py` fetches tweets in real time using specific keywords or from a CSV file.
- The collected data is analyzed to classify sentiments dynamically.

### **2. Model Training**
- Multiple machine learning algorithms were trained to predict sentiments, including:
  - **Logistic Regression (LREG)**
  - **Support Vector Machines (SVM)**
  - **Multinomial Naive Bayes (MNB)**
  - **Random Forest (RF)**
  - **XGBoost**
  - **K-Nearest Neighbors (KNN)**

### **3. Text Representation Techniques**
- Implemented four approaches for representing textual data:
  - **TF-IDF (Term Frequency-Inverse Document Frequency)**
  - **Bag of Words (BoW)**
  - **Doc2Vec**
  - **Word2Vec**

### **4. RNN with LSTM Model**
- A Recurrent Neural Network (RNN) model with an **LSTM architecture** was developed to capture contextual relationships in textual data.

### **5. Visualization of Results**
- Predicted results are displayed through **interactive graphs** and visualizations for better interpretation of sentiment trends.

---

## **File Structure**

| **File Name**               | **Description**                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| `Airline-Sentiment-2-w-AA.csv` | Dataset containing training data for sentiment analysis (tweets related to airlines). |
| `Evaluation.ipynb`           | Jupyter notebook to evaluate and compare the performance of different models.   |
| `LSTM.ipynb`                 | Implementation and training of the RNN model with LSTM.                         |
| `XGboost_tester.py`          | Python script for testing and optimizing the XGBoost model.                     |
| `bow.ipynb`                  | Jupyter notebook for the Bag of Words approach.                                 |
| `doc2vec.ipynb`              | Implementation of the Doc2Vec text representation approach.                     |
| `tf-idf.ipynb`               | Implementation and evaluation of models based on TF-IDF.                        |
| `word2vec.ipynb`             | Jupyter notebook for the Word2Vec approach.                                     |
| `sa.py`                      | Main script for collecting tweets in real time, analyzing sentiments, and visualizing results. |
| `chromedriver.exe`           | Executable required for web scraping automation.                                |
| `README.md`                  | This documentation file.                                                       |

---

## **Methodology**

### **1. Data Preprocessing**
- Cleaning textual data by removing special characters, links, and irrelevant words.
- Tokenizing and lemmatizing text for uniformity.

### **2. Model Training**
- Each algorithm was trained using four text representation techniques (**TF-IDF**, **BoW**, **Doc2Vec**, **Word2Vec**).
- Models were evaluated using metrics such as **accuracy**, **precision**, **recall**, and **F1-score**.

### **3. Choosing the Optimal Model**
- The most accurate and optimized model was selected for deployment in real-time sentiment analysis.

### **4. Visualization and Deployment**
- Predictions were integrated into the script `sa.py` for practical use.
- Results were visualized using graphs and interactive plots.

---

## **Results and Applications**
- The trained models can classify tweet sentiments in real time with high accuracy.
- Businesses can use this application to:
  - **Monitor customer satisfaction.**
  - **Identify recurring issues.**
  - **Spot opportunities for service improvements.**

---

## **Technical Requirements**

- **Python 3.8 or later**
- Required libraries:
  - `scikit-learn`, `xgboost`, `tensorflow`, `pandas`, `matplotlib`, `seaborn`, `nltk`, `selenium`
- **Google Chrome browser** and `chromedriver.exe` for data scraping.

---

## **How to Use**

1. Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the main script to collect tweets and analyze sentiments:

   ```bash
   python sa.py

View the results through the interactive graphs generated.
