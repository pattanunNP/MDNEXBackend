import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

MONGODB_USER = str(os.environ.get("MONGODB_URL", "mongodb+srv://admin:8ZY4f8ybNyWV1wa0@mdnex.ijnzy.mongodb.net/UserDB?retryWrites=true&w=majority"))


SECERET_KEY = str(os.environ.get("SECERET_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW5fbWFzdGVya2V5IiwiZW1haWwiOiJhZG1pbkBzdGFuZHVwY29kZS5jbyJ9.XCrCZtxSH89ohXCf-M5MCdp1P0FMEh8SHRwbv0Qsl1w"))

MAILGUN_API_KEY = str(os.environ.get("MAILGUN_API_KEY","c56bc946827aea9f4e42562f4cc08f32-1d8af1f4-de20447d"))

MAILGUN_DOMAIN = str(os.environ.get("MAILGUN_DOMAIN","noreply@mg.standupcode.co"))

ROOT_URL= str(os.environ.get("ROOT_URL", "http://127.0.0.1:8000"))

FRONTEND_URL =str(os.environ.get("FRONTEND_URL", "http://localhost:3000"))

SECERET_EMAIL_KEY = str(os.environ.get("SECERET_EMAIL_KEY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hc3RlckBzdGFuZHVwY29kZS5jbyIsInV1aWQiOiJkZDA1ZWRlNC02MTQ3LTQwNjYtYTdjZC1jOGY5ODcyODVlNmQifQ.4zQWyeTHUk7QeSl1nnpcPjN6RClhD7ytl4sTDm0OSm0"))