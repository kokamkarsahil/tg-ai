import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from cerebras.cloud.sdk import Cerebras

# Load environment variables
load_dotenv()

# Telegram credentials
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
session_name = os.getenv('TELEGRAM_SESSION_NAME')

# Cerebras API key
cerebras_api_key = os.getenv('CEREBRAS_API_KEY')

# Initialize clients
client = TelegramClient(session_name, api_id, api_hash)
cerebras = Cerebras(api_key=cerebras_api_key)

@client.on(events.NewMessage(pattern=r'\.aireply (.+)'))
async def handle_aireply(event):
    # Get the prompt from the command
    prompt = event.pattern_match.group(1)
    
    # Check if the message is a reply to another message
    if event.is_reply:
        # Get the replied message
        replied_message = await event.get_reply_message()
        # Use the replied message's text as context
        context = replied_message.text
        # Combine context and prompt
        full_prompt = f"Context: {context}\n\nPrompt: {prompt}"
    else:
        # Use only the prompt
        full_prompt = prompt
    
    # Send a temporary message while processing
    processing_message = await event.edit("Processing your request with Cerebras AI...")
    
    try:
        # Send the prompt to Cerebras AI
        response = cerebras.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],
            model="qwen-3-32b",
            max_completion_tokens=16382,
            temperature=0.6,
            top_p=0.9
        )
        
        # Get the AI response
        ai_response = response.choices[0].message.content
        
        # Edit the original message with the AI response
        await event.edit(ai_response)
    except Exception as e:
        # Handle any errors
        await event.edit(f"Error occurred: {str(e)}")

# Run the client
async def main():
    await client.start()
    print("Telegram AI Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
