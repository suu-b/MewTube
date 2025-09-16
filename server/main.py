from http.client import HTTPException
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
load_dotenv()

# Configuration Constants
BASE_URL = "https://www.googleapis.com/youtube/v3/search"
YT_KEY=os.getenv("YT_KEY")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/search-dummy")
def search_dummy():
    params = {
        "part": "snippet",
        "q": "Philosophy of science, unsolicited advice", # a sample query
        "type": "video",
        "maxResults": 20,
        "key": YT_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if(response.status_code != 200):
        raise HTTPException(status_code = requests.status_codes, detail = response.text)

    return response.json()
    
