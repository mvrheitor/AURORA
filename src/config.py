from groq import Groq
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def get_client():
    return Groq()