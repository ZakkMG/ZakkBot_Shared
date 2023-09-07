import praw
import threading
import random
import time
from datetime import datetime, timedelta

# Set up Reddit API credentials
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='')


