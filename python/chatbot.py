import os
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion
import json

# Load top-secret potions... I mean environment variables 🧪
load_dotenv()

# Pull out the magical Gemini API key from the hat 🎩
gemini_api_key = os.getenv("GEMINI_API_KEY")

# If the magic key isn't found, throw a dramatic tantrum 😤
if not gemini_api_key:
    raise ValueError("🛑 GEMINI_API_KEY not found! Did you forget to whisper it into the .env file?")

@cl.on_chat_start
async def start():
    """Summon the chatbot spirit when someone enters the realm."""
    cl.user_session.set("chat_history", [])  # Fresh memory slate 🧠

    await cl.Message(content="👋 Hey there, I'm **Wania AI**, your slightly quirky assistant! How can I sprinkle some help today? 🪄").send()

@cl.on_message
async def main(message: cl.Message):
    """Hear the user's cries and respond with AI wisdom (or nonsense, depends)."""
    
    # Dramatic pause for thinking... 🤔💭
    msg = cl.Message(content="🤯 My brain is buzzing... give me a sec!")
    await msg.send()

    # Dig into my dusty scrolls of past conversations
    history = cl.user_session.get("chat_history") or []
    
    # Scribble down the user's latest chant
    history.append({"role": "user", "content": message.content})

    try:
        # Ask the great and powerful Gemini for wisdom 🧙‍♂️
        response = completion(
            model="gemini/gemini-2.0-flash",
            api_key=gemini_api_key,
            messages=history
        )
        
        response_content = response.choices[0].message.content

        # Replace thinking noises with actual knowledge
        msg.content = f"🧠 Aha! Here's what I found:\n\n{response_content}"
        await msg.update()

        # Save this magical answer for future scrolls
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

        # Optional gossip logs
        print(f"User said: {message.content}")
        print(f"Wania AI replied: {response_content}")

    except Exception as e:
        msg.content = f"💥 Oops! My circuits got fried: {str(e)}"
        await msg.update()
        print(f"😱 Error in spellcasting: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """When the user disappears into the mist, archive the prophecy."""
    history = cl.user_session.get("chat_history") or []

    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
    print("📜 The tale has been recorded in the sacred archives (chat_history.json).")
