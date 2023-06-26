import praw
import logging
import os
import random
import re

def setup_reddit_api(config):
    try:
        reddit = praw.Reddit(
            client_id=config['reddit']['client_id'],
            client_secret=config['reddit']['client_secret'],
            username=config['reddit']['username'],
            password=config['reddit']['password'],
            user_agent="zakkbot"
        )
        return reddit
    except Exception as e:
        logging.error(f"Error setting up Reddit API: {e}")
        return None

def is_incomplete_sentence(sentence):
    # Check if the sentence ends with a punctuation mark
    if re.match(r'.*[.!?]\s*$', sentence):
        return False
    return True

def simulate_errors(response):
    # Introduce small typos or grammatical errors
    if random.random() < 0.05:
        index = random.randint(0, len(response) - 1)
        response = response[:index] + response[index + 1:]
    return response

def make_new_post(reddit, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    post_types = ['image', 'link', 'text']
    post_type = random.choice(post_types)
    
    try:
        if post_type == 'image':
            # Post an image from the "zakkbot pics" folder
            image_folder = "zakkbot pics"
            image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
            if image_files:
                image_file = random.choice(image_files)
                title = os.path.splitext(image_file)[0]
                subreddit.submit_image(title, os.path.join(image_folder, image_file))
                # Remove the used image
                os.remove(os.path.join(image_folder, image_file))
            else:
                print("No images found in the 'zakkbot pics' folder.")
        
        elif post_type == 'link':
            # Post a link from the "zakkbot_links.txt" file
            with open("zakkbot_links.txt", "r") as file:
                links = file.readlines()
            if links:
                link = random.choice(links).strip()
                # Remove the used link
                links.remove(link + '\n')
                with open("zakkbot_links.txt", "w") as file:
                    file.writelines(links)
                # Use a default title for link posts (you can customize this)
                title = "Check out this cool link!"
                subreddit.submit(title, url=link)
            else:
                print("No links found in the 'zakkbot_links.txt' file.")
        
        elif post_type == 'text':
            # Post a text post
            title = "This is a random text post"
            content = "Hello, I am ZakkBot and this is a random text post."
            subreddit.submit(title, selftext=content)
        
    except Exception as e:
        logging.error(f"Error making a new post: {e}")

def reply_to_unread_notifications(reddit, response, previous_interactions):
    try:
        for item in reddit.inbox.unread(limit=7):
            # Check if the message is an incomplete sentence
            if is_incomplete_sentence(item.body):
                clarification_response = "It seems like your sentence is incomplete. Could you please clarify?"
                item.reply(clarification_response)
                item.mark_read()
                continue
            
            # Context awareness
            context = previous_interactions.get(item.author.name, "")
            full_prompt = context + " " + item.body
            
            # Generate response
            response = generate_response(full_prompt(full_prompt, personality_prompt, 0.7, 50)
            
            # Error simulation
            response = simulate_errors(response)
            
            # Bot name awareness
            if "ZakkBot" in item.body:
                response = "Hi, I'm ZakkBot! " + response
            
            # Store interaction for context
            previous_interactions[item.author.name] = full_prompt + " " + response
            
            # Reply
            item.reply(response)
            item.mark_read()
    except Exception as e:
        logging.error(f"Error replying to unread notifications: {e}")

def comment_on_new_posts(reddit, subreddit_name, response):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.new(limit=5):
            post.reply(response)
    except Exception as e:
        logging.error(f"Error commenting on new posts: {e}")

