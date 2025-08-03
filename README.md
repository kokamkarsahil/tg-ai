# Telegram AI Bot

A Telegram userbot that integrates with Cerebras AI to provide intelligent responses to messages.

## Features

- Respond to messages with AI-generated content using the `.aireply <prompt>` command
- When replying to another message with `.aireply <prompt>`, the original message text is used as context for the AI
- Uses the qwen-3-32b model for generating responses

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -e .
   ```
   or if you're using uv:
   ```bash
   uv sync
   ```

3. Run `generate-session.py` to generate session

4. Set up your environment variables in the `.env` file:
   ```
   CEREBRAS_API_KEY=your_api_key_here
   TELEGRAM_API_ID=your_api_id_here
   TELEGRAM_API_HASH=your_api_hash_here
   TELEGRAM_SESSION_NAME=your_session_name_here
   ```

## Usage

1. Run the bot:
   ```bash
   python main.py
   ```

2. In Telegram, use the bot with the following command:
   - `.aireply <prompt>` - Send a prompt to the AI and get a response
   - When replying to a message with `.aireply <prompt>`, the replied message's text will be used as context

## How It Works

The bot listens for messages containing the `.aireply` command followed by a prompt. When detected, it:
1. Checks if the message is a reply to another message
2. If it is a reply, combines the replied message text as context with the prompt
3. Sends the prompt (with context if available) to Cerebras AI
4. Edits the original message with the AI-generated response

## Dependencies

- telethon - For Telegram client functionality
- cerebras-cloud-sdk - For interacting with Cerebras AI
- python-dotenv - For loading environment variables
