import argparse
from collections import namedtuple
import json
import os
import re

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tweepy


# selenium on heroku
GOOGLE_CHROME_BIN = os.environ['GOOGLE_CHROME_BIN']
CHROME_DRIVER = os.environ['CHROME_DRIVER']
# twitter
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
# slack
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

PACKT_FREE_LEARNING = "https://www.packtpub.com/packt/offers/free-learning"
UPDATE_MSG = """Packt Free Learning of the day:
{title} by {author} (published: {pub_date})

{link}

{expires} ... grab it now!
"""


Book = namedtuple('Book', 'title author pub_date expires')


def _create_update(book):
    return UPDATE_MSG.format(title=book.title,
                             author=book.author,
                             pub_date=book.pub_date,
                             link=PACKT_FREE_LEARNING,
                             expires=book.expires)


def _get_options():
    options = Options()
    options.add_argument("--headless")
    options.binary_location = GOOGLE_CHROME_BIN
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return options


def _get_expired(timer):
    hh_mm_ss = re.sub(r'.*(\d{2}:\d{2}:\d{2}).*', r'\1', timer)
    title = 'This title'
    try:
        hours = int(hh_mm_ss.split(':')[0])
    except ValueError:
        return f'{title} expires today'

    if hours == 0:
        return f'{title} is about to expire'
    else:
        return f'{title} expires in {hours} hours'


def get_packt_book():
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER,
                              options=_get_options())
    driver.get(PACKT_FREE_LEARNING)

    find_class = driver.find_element_by_class_name

    title = find_class('product__title').text
    author = find_class('product__author').text
    pub_date = find_class('product__publication-date').text
    timer = find_class('countdown__title').text.splitlines()[-1]

    driver.quit()

    book = Book(title, author, pub_date, _get_expired(timer))
    return _create_update(book)


def twitter_authenticate():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


def post_to_twitter(book_post):
    try:
        api = twitter_authenticate()
        api.update_status(book_post)
        print(f'Shared title on Twitter')
    except Exception as exc:
        print(f'Error posting to Twitter: {exc}')


def post_to_slack(book_post):
    payload = {'text': book_post}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(SLACK_WEBHOOK_URL,
                         data=json.dumps(payload),
                         headers=headers)
    if resp.status_code == 200:
        print(f'Shared title on Slack')
    else:
        print(f'Error posting to Slack: {resp.status_code}')


if __name__ == '__main__':
    description = 'Packt free book (video) of the day'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--twitter', action='store_true',
                        help="Post title to Twitter")
    parser.add_argument('-s', '--slack', action='store_true',
                        help="Post title to Slack")
    args = parser.parse_args()

    book_update = get_packt_book()
    print(book_update)

    if args.slack:
        post_to_slack(book_update)

    if args.twitter:
        post_to_twitter(book_update)
