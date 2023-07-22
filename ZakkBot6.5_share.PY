import openai
import os
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
                     user_agent='zakkbot')
# Set up OpenAI API credentials
openai.api_key = ""

subreddit = reddit.subreddit("SubSimGPT2Interactive")

temperature = 0.93
max_tokens = 220

personality_prompt = (".")

# Time window to check for new posts and comments
time_window = timedelta(hours=2)

# Function to check if a post or comment is recent enough
def is_recent(timestamp):
 return datetime.now() - timestamp <= time_window

# Function to process a new comment
def process_comment(comment):
    # Add comment to the bank if it is not already there
    if comment.id not in comments_bank:
        comments_bank.append(comment.id)
        # Process the comment if it contains trigger words
        if trigger_pattern.search(comment.body):
            # Do something
            pass

# Function to process a new post
def process_post(post):
    # Add post to the bank if it is not already there
    if post.id not in posts_bank:
        posts_bank.append(post.id)
        # Process the post if it contains trigger words
        if trigger_pattern.search(post.title) or trigger_pattern.search(post.selftext):
            # Do something
            pass

# Function to monitor the subreddit for new posts and comments
def monitor_subreddit():
    for post in subreddit.new(limit=5):
        post_title = post.title.strip()  # Remove any leading/trailing spaces
        post_body = post.selftext.strip()  # Remove any leading/trailing spaces
        # Find the index of the first occurrence of a period, exclamation mark, or question mark
        end_of_title_index = -1
        for c in ['.', '!', '?']:
                if c in post_title:
                    end_of_title_index = post_title.index(c)
                    break

    if end_of_title_index != -1:
        # Split the title and body of the post
        post_title = post_title[:end_of_title_index+1].strip()
        post_body = post_title[end_of_title_index+1:].strip()

    # Check if the bot has already commented on this post
    if post.id not in commented_posts:
        if is_recent(datetime.fromtimestamp(post.created_utc)):
            process_post(post)
            for comment in post.comments:
                if is_recent(datetime.fromtimestamp(comment.created_utc)):
                    process_comment(comment)

def generate_response(prompt):
    full_prompt = personality_prompt + " " + prompt
    response = ''
    
    while not response.strip():
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        ).choices[0].text.strip()
    
    return response

def get_random_post(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=100):
        if not post.stickied and not post.over_18:
            posts.append(post)
    if not posts:
        return None
    post = random.choice(posts)
    return {'title': post.title, 'url': post.url}

def random_image_url():
    return f'https://picsum.photos/seed/{random.randint(0, 1000000)}/800/600'

commented_posts = {}  # initialize an empty dictionary
comment_threads = {}  # Keep track of comments to avoid conflicting with own responses

def check_and_reply_to_notifications():
    unread_messages.sort(key=lambda x: x.created_utc)  # sort messages by creation time, oldest first
    for message in unread_messages:
        if isinstance(message, praw.models.Comment):
            # check if message was created within the last 6 hours
            if time.time() - message.created_utc > 10*60*60:
                continue
            prompt = message.body
            response = generate_response(prompt, message.author.name)
            message.reply(response)
            print(f"Replied to notification: {response}")
            with open("output.txt", "a", encoding='utf-8') as output_file:
                output_file.write(f"Interaction type: Notification reply\nPrompt: {prompt}\nResponse: {response}\nUsername: {message.author.name}\n\n")
            message.mark_read()
        elif isinstance(message, praw.models.Submission):
            # check if submission is locked
            if message.locked:
                continue
            # proceed with replying to comments if submission is not locked
            for comment in message.comments:
                if isinstance(comment, praw.models.Comment):
                    # check if comment was created within the last 6 hours
                    if time.time() - comment.created_utc > 6*60*60:
                        continue
                    prompt = comment.body
                    response = generate_response(prompt, comment.author.name)
                    comment.reply(response)
                    print(f"Replied to comment: {response}")
                    with open("output.txt", "a", encoding='utf-8') as output_file:
                        output_file.write(f"Interaction type: Comment reply\nPrompt: {prompt}\nResponse: {response}\nUsername: {comment.author.name}\n\n")
def process_submission(submission, reply_message):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments:
        if comment.locked:
            continue
        if comment.author is not None and comment.author.name == bot_username:
            continue
        if comment.id in processed_comments:
            continue
        comment.reply(reply_message)
        processed_comments.add(comment.id)
        
def handle_user_input():
    num_comments = 0
    num_posts = 0
    num_replies = 0
    user_dict = {}

    with open("output.txt", "a", encoding='utf-8') as output_file:
        while True:
            if num_comments % 5 == 0:
                user_input = input("Press '1' to post a comment, '2' to create a post, '3' to reply to notifications, '4' to process comments on existing threads, '5' to crosspost a random post: ")
            while user_input not in ('1', '2', '3', '4', '5'):
                user_input = input("Invalid input. Press '1' to post a comment, '2' to create a post, '3' to reply to notifications, '4' to process comments on existing threads, '5' to crosspost a random post: ")
            if user_input == '1':
                # Keep track of the post IDs that the bot has already commented on
                commented_post_ids = []
                # Get the 10 newest posts from the subreddit
                new_posts = list(subreddit.new(limit=10))
                for post in new_posts:
                    if num_comments >= 5:
                        break
                    # Check if the post is within the last 36 hours
                    if datetime.utcnow().timestamp() - post.created_utc > 129600:
                        continue
                    # Check if the bot has already commented on this post
                    if post.id in commented_post_ids:
                        continue
                    prompt = post.title + '\n' + post.selftext
                    response = generate_response(prompt)
                    post.reply(response)
                    print(f"Posted comment: {response}")
                    output_file.write(f"Interaction type: Comment\nPrompt: {prompt}\nResponse: {response}\nUsername: {post.author.name}\n\n")
                    user_dict[post.author.name] = True
                    num_comments += 1
                    # Add the current post ID to the list of commented post IDs
                    commented_post_ids.append(post.id)
                    time.sleep(5)  # Add a delay of 5 seconds between comments
              

            elif user_input == '2':
                if num_posts >= 1:
                 print("Sorry, you can only create one post per input cycle.")
                 continue
    
                # Generate a prompt for the post
                prompt = " u/Mistread_GPT3 has been offline for a day."
    
                # Generate a title for the post
                title_generation = generate_response(prompt + " Give me a title.")
                title = title_generation[:100]  # Truncate title to make it shorter
    
                # Generate the body of the post
                body_generation = generate_response(prompt + ".")
                body = body_generation[:1500]  # Limit the body length
    
                # Submit the post
                subreddit.submit(title, selftext=body)
                print(f"Posted a new text post with title: {title}")
    
                # Log the post
                output_file.write(f"Interaction type: Post\nPrompt: {prompt}\nTitle: {title}\nBody: {body}\nUsername: {reddit.user.me().name}\n\n")
                user_dict[reddit.user.me().name] = True
                num_posts += 1
                time.sleep(5)  # Add a delay of 5 seconds between posts


            elif user_input == '3':
                unread_messages = reddit.inbox.unread()
                unread_messages = sorted(unread_messages, key=lambda x: x.created_utc)
                for message in unread_messages:
                    if num_replies >= 7:
                        break
                    if isinstance(message, praw.models.Comment):
                        prompt = message.body
                        response = generate_response(prompt)
                        message.reply(response)
                        print(f"Replied to notification: {response}")
                        output_file.write(f"Interaction type: Notification reply\nPrompt: {prompt}\nResponse: {response}\nUsername: {message.author.name}\n\n")
                        user_dict[message.author.name] = True
                        num_replies += 1
                        time.sleep(3)  # Add a delay of 1 second between notification replies
                        message.mark_read()
                        
            elif user_input == '4':
                threads = subreddit.new(limit=5)
                for thread in threads:
                    if isinstance(thread, praw.models.Comment) and thread.id not in comment_threads:
                        comment_threads[thread.id] = True
                        for comment in thread.replies:
                            if comment.author.name == reddit.user.me().name:
                                prompt = comment.body
                                response = generate_response(prompt)
                                comment.reply(response)
                                print(f"Replied to comment: {response}")
                                output_file.write(f"Interaction type: Comment reply\nPrompt: {prompt}\nResponse: {response}\nUsername: {comment.author.name}\n\n")
                                user_dict[comment.author.name] = True
                                time.sleep(1)  # Add a delay of 1 second between replies
            elif user_input == '5':
                # Crosspost a random post from a set of subreddits
                subreddits = ['memes', 'Dragonballsuper', 'aww', 'worldnews', 'antijokes', 'giraffesdontexist']
                subreddit_name = random.choice(subreddits)
                post = get_random_post(subreddit_name)
                if post is None:
                    continue
                title = f"Crosspost from r/{subreddit_name}: {post['title']}"
                if len(title) > 100:
                    title = title[:97] + "..."
                url = post['url']
                subreddit.submit(title, url=url)
                print(f"Crossposted a post from r/{subreddit_name}: {title}")

            if len(user_dict) >= 5:
                print("You have reached the limit of 5 interactions per input cycle. Try again later.")
                break       

            # Save the user dictionary to a file after each interaction cycle
            with open("user_dict.txt", "a") as f:
                f.write(str(user_dict))


handle_user_input()

# Start a thread to listen for user input
input_thread = threading.Thread(target=handle_user_input)
input_thread.daemon = True
input_thread.start()

# Keep the main thread alive
while True:
    pass

