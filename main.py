import os
from fastapi import FastAPI,HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# configure .env
load_dotenv()


generative_configure = {
    "temperature": 0.7,
    "max_output_tokens": 50,

}


# app 
app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])

# addaing frontend
app.mount("/static",StaticFiles(directory="static"),name="static")

#configure genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#Model 
model = genai.GenerativeModel (model_name="gemini-flash-latest",
    generation_config=generative_configure)


#route
@app.post("/")
async def quote_generator():
    try:
        prompt = ("who is walterwhite in breaking bad")
        response = model.generate_content(prompt)
        if not response:
            raise ValueError(" You are getting some result")
        return{"quote":response.text}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
