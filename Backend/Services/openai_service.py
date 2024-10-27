import base64
from dotenv import load_dotenv
from openai import OpenAI
import os 
load_dotenv()

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
class OpenaiService:

    def __init__(self):
        self.client = OpenAI()
    
    async def call_openai_with_streaming(self, question, data=None, history: list = []):
        completion = self.client.chat.completions.create(
                messages= [
                    *history,
                    {"role": "system", "content":"You are a helpful assistant that can help people with anything"},
                    {"role": "user", "content": question}
                ],
                model="gpt-4o-mini",
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

    def call_openai_without_streaming(self, question, data=None, history: list = []):
        completion = self.client.chat.completions.create(
                messages= [
                    *history,
                    {"role": "system", "content":"You are a helpful assistant that can help people with anything"},
                    {"role": "user", "content": question}
                ],
                model="gpt-4o-mini",
                stream=False
            )
        if completion.choices[0].message.content == None:
            return ""
        return completion.choices[0].message.content


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


    def build_llm_document_query(self, query: str, vector_result: list):
        llm_query = f"Please answer the following question: {query} using the provided information: "
        for result in vector_result:
            llm_query += f"{result.payload['text']} "

        return llm_query


    def generate_image(self, prompt: str):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        if image_url == None:
            return ""
        return image_url