import configparser
import reddit_api
import openai_api
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Setup OpenAI API
openai_api_key = config['openai']['api_key']
openai_api.setup_openai_api(openai_api_key)

# Setup Reddit API
reddit = reddit_api.setup_reddit_api(config)

# Check if Reddit API is setup successfully
if reddit is None:
    logging.error("Failed to setup Reddit API.")
    exit()

# Main logic of the bot
while True:
    # Display options to the user
    print("Select an option:")
    print("1: Make a new post")
    print("2: Reply to unread notifications")
    print("3: Comment on the 5 newest posts in the subreddit")
    print("4: Exit")
    
    # Get user input
    user_input = input("Enter option number: ").strip()
    
    # Handle user input
    if user_input == "1":
        # Make a new post
        subreddit_name = "subsimgpt2interactive"  # specify the subreddit name
        reddit_api.make_new_post(reddit, subreddit_name)
        
    elif user_input == "2":
        # Reply to unread notifications
        # You can customize the response or generate it using GPT-3
        response = "Hello, this is ZakkBot replying to your message!"
        previous_interactions = {}
        reddit_api.reply_to_unread_notifications(reddit, response, previous_interactions)
        
    elif user_input == "3":
        # Comment on the 5 newest posts in the subreddit
        subreddit_name = "subsimgpt2interactive"  # specify the subreddit name
        response = "Hello, this is ZakkBot commenting on your post!"
        reddit_api.comment_on_new_posts(reddit, subreddit_name, response)
        
    elif user_input == "4":
        # Exit the program
        break
        
    else:
        print("Invalid option. Please enter a number between 1 and 4.")
