import base64
from dotenv import load_dotenv
from openai import OpenAI
import os 
load_dotenv()

        # Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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
        print(completion) 
        for chunk in completion:
            chunk_message = chunk.choices[0].delta.content 
            if chunk == None or chunk_message == None:
                print("empty chunk")
            else:
                print(chunk_message)
                yield chunk_message 
                answer += chunk_message
        print(answer)


    async def read_image(self, base64_image, question):


        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": question
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
            stream = True
        )
        answer = ""
        print(completion) 
        for chunk in completion:
            chunk_message = chunk.choices[0].delta.content 
            if chunk == None or chunk_message == None:
                print("empty chunk")
            else:
                print(chunk_message)
                yield chunk_message 
                answer += chunk_message

        print(answer)