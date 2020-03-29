import requests
import sqlite3

from bs4 import BeautifulSoup

urls = ['https://twitter.com/CAgovernor']

# send a request to retrieve HTML from twitter
# use bs4 to parse HTML into properties
# return list of tweet and properties
def get_tweets(url):

    # retrieving HTML 
    try:
        data = requests.get(url)
    except:
        print('FAILED TO RETRIEVE TWEETS FROM ', url)

    # parsing HTML
    html = BeautifulSoup(data.text, 'html.parser')
    timeline = html.select('#timeline li.stream-item')

    all_tweets = []

    for tweet in timeline:
        tweet_id = tweet['data-item-id']
        tweet_loc = 'CA'
        #tweet_handle = 
        raw_tweet_text = tweet.select('p.tweet-text')

        # check to ensure tweet is text, else ignore text
        if len(raw_tweet_text) > 0:
            tweet_text = tweet.select('p.tweet-text')[0].get_text()
            all_tweets.append((tweet_loc, tweet_text))

    return all_tweets

def init_db():

    for url in urls:
        aggregated_tweets.extend(get_tweets(url))

    conn = sqlite3.connect('thingweneed.db')
                              
    c = conn.cursor()
    
    c.execute('CREATE TABLE TWEETS (state, text)')
    c.execute('CREATE TABLE USERS (state, phone_number)')

    for t_dict in aggregated_tweets:
        c.execute('INSERT INTO TWEETS VALUES (?, ?)', (t_dict[0], t_dict[1]))

    conn.commit()
    conn.close()

def refresh_tweets():

    conn = sqlite3.connect('thingweneed.db')
                              
    c = conn.cursor()
    c.execute('DROP TABLE TWEETS')

    for url in urls:
        aggregated_tweets.extend(get_tweets(url))
    
    c.execute('CREATE TABLE TWEETS (state, text)')

    for t_dict in aggregated_tweets:
        c.execute('INSERT INTO TWEETS VALUES (?, ?)', (t_dict[0], t_dict[1]))

    conn.commit()
    conn.close()

def add_user(state, phone_number):
    conn = sqlite3.connect('thingweneed.db')
    c = conn.cursor()
    c.execute('INSERT INTO USERS VALUES (?, ?)', (state, phone_number))

    conn.commit()
    conn.close()

def remove_user(phone_number):
    conn = sqlite3.connect('thingweneed.db')
    c = conn.cursor()
    c.execute('DELETE FROM USERS WHERE USERS.phone_number = ?', (phone_number))

    conn.commit()
    conn.close()

def get_call_list():
    conn = sqlite3.connect('thingweneed.db')
    c = conn.cursor()

    c.execute('SELECT phone_number, USERS.state, text FROM TWEETS, USERS WHERE TWEETS.state = USERS.state')
    l = c.fetchall()

    conn.commit()
    conn.close()

    return l

if __name__ == "__main__":
    
    init_db()
    add_user('CA', '86')
    print(get_call_list())
