import base64
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
        for chunk in completion:
            chunk_message = chunk.choices[0].delta.content 
            if chunk == None or chunk_message == None:
                print("empty chunk")
            else:
                yield chunk_message 
                answer += chunk_message


    def read_audio(self, audio):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio,
        )
        print(transcription.text)
        return self.call_openai_with_streaming(transcription.text)
    

    def create_embedding(self, text):
        embedding_model = "text-embedding-3-small"
        result = self.client.embeddings.create(input=text, model=embedding_model)
        return result
