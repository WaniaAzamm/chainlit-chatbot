import os
import nest_asyncio
from dotenv import load_dotenv
from litellm import completion

user_input = input("Enter your question: ")

nest_asyncio.apply()

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = api_key

messages = [{"role": "user", "content": f"{user_input}"}]
response = completion(model="gemini/gemini-2.0-flash", messages=messages)
print(response['choices'][0]['message']['content'])