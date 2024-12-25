import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment, polarity

def scrape_tweets(username, password, num_tweets, keyword_entry, file_name):
    driver = webdriver.Chrome(executable_path='D:\\Program Files\\PFE\\SA_pipline\\chromedriver.exe')
    driver.get("https://twitter.com/login")

    # Increase wait time to 20 seconds
    wait = WebDriverWait(driver, 20)

    try:
        # Log in
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        username_input = driver.find_element(By.XPATH, "//input[@name='text']")
        username_input.send_keys(username)
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Suivant')]")  # Adjust for French
        next_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password_input = driver.find_element(By.XPATH, "//input[@name='password']")
        password_input.send_keys(password)
        log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Se connecter')]")  # Adjust for French
        log_in.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))

        # Search for the keyword
        search_url = f"https://twitter.com/search?q={keyword_entry}&src=typed_query&f=live"
        driver.get(search_url)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']")))

        UserTags, TimeStamps, Tweets, Replys, reTweets, Likes = [], [], [], [], [], []

        while len(Tweets) < num_tweets:
            articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
            for article in articles:
                try:
                    tweet_handle = article.find_element(By.XPATH, ".//div/div[2]/div[1]/div/div/div[2]/div/div[1]/a/div/span").text
                    UserTags.append(tweet_handle)
                except:
                    UserTags.append('')

                try:
                    TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    TimeStamps.append(TimeStamp)
                except:
                    TimeStamps.append('')

                try:
                    Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                    Tweets.append(Tweet)
                except:
                    Tweets.append('')

                try:
                    Reply = article.find_element(By.XPATH, ".//div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span").text
                    Replys.append(Reply)
                except:
                    Replys.append('')

                try:
                    reTweet = article.find_element(By.XPATH, ".//div[2]/div[4]/div/div[2]/div/div/div[2]/span/span/span").text
                    reTweets.append(reTweet)
                except:
                    reTweets.append('')

                try:
                    Like = article.find_element(By.XPATH, ".//div[2]/div[4]/div/div[3]/div/div/div[2]/span/span/span").text
                    Likes.append(Like)
                except:
                    Likes.append('')

            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(3)

            if len(Tweets) >= num_tweets:
                break

        driver.quit()

        df = pd.DataFrame(zip(UserTags, TimeStamps, Tweets, Replys, reTweets, Likes),
                          columns=['UserTags', 'TimeStamps', 'Tweets', 'Replys', 'reTweets', 'Likes'])
        df.to_excel(rf"{file_name}.xlsx", index=False)
        return df

    except Exception as e:
        print(f"Exception occurred: {e}")
        print(f"Current URL: {driver.current_url}")
        print(driver.page_source)
        driver.quit()

# Streamlit App
st.title("Sentiment Analysis Dashboard")

option = st.selectbox("Choose an option", ["Insert Text", "Upload CSV", "Scrape Tweets"])

if option == "Insert Text":
    user_text = st.text_area("Enter your text here")
    if st.button("Analyze"):
        sentiment, score = analyze_sentiment(user_text)
        st.write(f"Sentiment: {sentiment}, Score: {score}")

elif option == "Upload CSV":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        text_column = st.selectbox("Select the text column", df.columns)
        time_column = st.selectbox("Select the time column (optional)", [None] + list(df.columns))

        if st.button("Analyze"):
            df['Sentiment'], df['Polarity'] = zip(*df[text_column].apply(analyze_sentiment))

            # Plot Tweet Length Distribution
            df['Text Length'] = df[text_column].apply(len)
            plt.figure(figsize=(10, 5))
            sns.histplot(df['Text Length'], bins=30)
            st.pyplot(plt.gcf())

            # Plot Sentiment Count and Percentage
            sentiment_count = df['Sentiment'].value_counts()
            sentiment_percentage = df['Sentiment'].value_counts(normalize=True) * 100

            plt.figure(figsize=(10, 5))
            sns.barplot(x=sentiment_count.index, y=sentiment_count.values)
            st.pyplot(plt.gcf())

            st.write("Sentiment Percentage:")
            st.write(sentiment_percentage)

            # Plot Sentiment Over Time
            if time_column:
                df['Datetime'] = pd.to_datetime(df[time_column])
                sentiment_over_time = df.groupby([df['Datetime'].dt.date, 'Sentiment']).size().unstack(fill_value=0)
                sentiment_over_time.plot(kind='bar', stacked=True, figsize=(10, 5))
                st.pyplot(plt.gcf())

elif option == "Scrape Tweets":
    keyword = st.text_input("Enter keyword")
    num_tweets = st.number_input("Number of tweets to scrape", min_value=1, max_value=1000, step=1, value=100)
    username = st.text_input("Enter Twitter username")
    password = st.text_input("Enter Twitter password", type="password")
    file_name = st.text_input("Enter name for the output file")

    if st.button("Scrape and Analyze"):
        df = scrape_tweets(username, password, num_tweets, keyword, file_name)

        df['Sentiment'], df['Polarity'] = zip(*df['Tweets'].apply(analyze_sentiment))

        # Plot Tweet Length Distribution
        df['Text Length'] = df['Tweets'].apply(len)
        plt.figure(figsize=(10, 5))
        sns.histplot(df['Text Length'], bins=30)
        st.pyplot(plt.gcf())

        # Plot Sentiment Count and Percentage
        sentiment_count = df['Sentiment'].value_counts()
        sentiment_percentage = df['Sentiment'].value_counts(normalize=True) * 100

        plt.figure(figsize=(10, 5))
        sns.barplot(x=sentiment_count.index, y=sentiment_count.values)
        st.pyplot(plt.gcf())

        st.write("Sentiment Percentage:")
        st.write(sentiment_percentage)

        # Plot Sentiment Over Time
        df['Datetime'] = pd.to_datetime(df['TimeStamps'])
        sentiment_over_time = df.groupby([df['Datetime'].dt.date, 'Sentiment']).size().unstack(fill_value=0)
        sentiment_over_time.plot(kind='bar', stacked=True, figsize=(10, 5))
        st.pyplot(plt.gcf())
