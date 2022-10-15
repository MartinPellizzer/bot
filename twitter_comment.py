import spacy
from collections import OrderedDict

import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By

nlp = spacy.load('en_core_web_lg')


def get_quotes():
    with open(f'zen_quotes.csv', encoding='latin1') as f:
        rows = csv.reader(f, delimiter='`')
        rows = [quote for quote in rows]
        return rows


def generate_comment(tweet):
    tweet = nlp(tweet)

    quotes = []
    for quote in get_quotes():
        w = nlp(quote[0])
        score = tweet.similarity(w)
        quotes.append(
            {
                'text': quote[0],
                'score': score
            }
        )

    sorted_quotes = sorted(quotes, key=lambda d: d['score'], reverse=True)
    return sorted_quotes[1]['text']


def comment():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("user-data-dir=C:\\Users\\admin\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

    driver = None
    driver = webdriver.Chrome(executable_path='C:\\drivers\\chromedriver_107', chrome_options=options)
    time.sleep(3)

    driver.get("https://twitter.com")
    time.sleep(7)

    try: tweets = [e for e in driver.find_elements(By.XPATH, '//article')]
    except: return 'no_tweets_found'

    links = []
    for e in tweets:
        try: 
            link = e.find_element(By.XPATH, './/time/..').get_attribute('href')
            links.append(link)
        except: 
            pass

    print(len(links))

    with open('tweets_done.csv') as f:
        reader = csv.reader(f)
        links_done = [row[0] for row in reader if row]

    for i, link in enumerate(links):
        if i >= 6: break
        if link in links_done: continue
        if 'quotes_worth_quoting' in link: continue
        
        driver.get(link)
        time.sleep(3)
        try: tweet_text = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
        except: continue
        
        comment = generate_comment(tweet_text)

        try: driver.find_element(By.XPATH, '//div[@data-testid="like"]').click()
        except: continue
        time.sleep(3)

        driver.find_element(By.XPATH, '//div[@aria-label="Tweet text"]').send_keys(comment)
        time.sleep(3)

        driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]').click()
        time.sleep(3)

        with open('tweets_done.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([link])

    driver.quit()

    return ''