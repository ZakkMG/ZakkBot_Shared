# ZakkBot - A Reddit Bot

ZakkBot is a Reddit bot that interacts with users on Reddit. It can make new posts, reply to unread notifications, and comment on new posts in a subreddit. The bot uses OpenAI's GPT-3 for generating responses.

## Features

- Make a new post in a subreddit (text, image, or link).
- Reply to unread notifications with context awareness.
- Comment on the 5 newest posts in a subreddit.
- Simulate human-like errors in responses.
- Configurable personality.

## Getting Started

### Prerequisites

- Python 3.6 or higher.
- A Reddit account with developer access for creating a bot.
- An API key from OpenAI for using GPT-3.

### Installation

1. Clone this repository or download the source code.

    ```
    git clone https://github.com/yourusername/zakkbot.git
    ```

2. Navigate to the project directory.

    ```
    cd zakkbot
    ```

3. Install the required Python libraries.

    ```
    pip install -r requirements.txt
    ```

4. Create a Reddit application through your Reddit account to obtain the `client_id` and `client_secret`.

5. Obtain an API key from OpenAI for using GPT-3.

6. Edit the `config.ini` file with your Reddit and OpenAI API credentials.

### Naming Your Bot

We encourage you to give your bot a unique name to make it special and identifiable. To change the name of your bot, edit the `user_agent` field in the `reddit_api.py` file. Additionally, you can customize the bot's responses and personality to reflect its unique name.

### Usage

1. Run the main script.

    ```
    python main.py
    ```

2. Follow the prompts in the console to interact with the bot.

## Configuration

The `config.ini` file contains the configuration for the Reddit API and OpenAI API. Make sure to fill in the `client_id`, `client_secret`, `username`, `password`, and `api_key` fields with your credentials.

## Contributing

Contributions are welcome! Please read the contributing guidelines before making any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
