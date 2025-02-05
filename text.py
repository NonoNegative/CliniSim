import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'What is the third letter in the alphabet?'}
  response = await AsyncClient().chat(model='llama3.2', messages=[message])
  return response['message']['content']

print(asyncio.run(chat()))