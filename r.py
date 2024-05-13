from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gradio_client import Client
import os
import requests

# Initialize the Gradio client
client = Client("Qwen/Qwen1.5-110B-Chat-demo")
#Api Telegram
TOKEN = "Key Telegram Bot"
#Elevenlabs Api
api_key = ""
#Charater Promt AI
system=""
# Define the chat function
def chat(update, context):
    history=[]
    # Get the user's message
    user_input = update.message.text

    # Make prediction only if the message starts with "!ami"
    if user_input.startswith("!amivoice"):
        # Extract the query from the message
        query = user_input[len("!amivoice"):].strip()
        print("[VQ]:",query)
        
        # Make prediction using Gradio client
        result = client.predict(
            query = query,
            history = history,
            system = system,
            api_name="/model_chat"
        )

        # Get the response from the Gradio model
        response_text = result[1][0][1]
        print("[VA]:", response_text)

        # Convert text to speech
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/gedzfqL7OGdPbwm0ynTP"
        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
          }
        data = {
        "text": response_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.21,
            "similarity_boost": 0.12
           }
         }
        response = requests.post(url, json=data, headers=headers)
    
        with open('a.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        # Send the voice response to the user
        update.message.reply_voice(voice=open("a.mp3", "rb"))
        #Synthesis voice limitation warning   
        update.message.reply_text("У меня есть ограничения на количество войсов,не используйте если вам не нужно голосовой ответ ")
        # Delete the temporary MP3 file
        os.remove("a.mp3")
        
    # Check if the user wants a voice response
    elif user_input.startswith("!ami"):
        # Extract the query from the message
        query = user_input[len("!ami"):].strip()
        print("[Q]:",query)

        # Make prediction using Gradio client
        result = client.predict(
            query = query,
            history = history,
            system = system,
            api_name="/model_chat"
        )
        
        # Get the response from the Gradio model
        response_text = result[1][0][1]
        print("[A]:",response_text)
        # Reply to the user with the response
        update.message.reply_text(response_text)


def main():
    # Set up the Telegram bot
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add a message handler to the dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    # Add a command handler for the !amivoice command
    dp.add_handler(CommandHandler("amivoice", chat))

    # Add a command handler for the !ami command
    dp.add_handler(CommandHandler("ami", chat))
    print("Start Bot")
    # Start the bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C
    updater.idle()
    print("Bot On")

if __name__ == '__main__':
    main()