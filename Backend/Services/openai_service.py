from dotenv import load_dotenv
from openai import OpenAI
import os 
load_dotenv()


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
class OpenaiService:

    def __init__(self):
        self.client = OpenAI()
    
    async def call_openai_with_streaming(self, question):
        completion = self.client.chat.completions.create(
                messages= [
                    {"role": "system", "content":"You are a helpful assistant that can help people with anything"},
                    {"role": "user", "content": question}
                ],
                model="gpt-3.5-turbo",
                stream=True
            )
        answer = ""
        for chunk in completion:
            chunk_message = chunk.choices[0].delta.content 
            if chunk == None or chunk_message == None:
                print("empty chunk")
            else:
                print(chunk_message)
                yield chunk_message 
                answer += chunk_message
        print(answer)
