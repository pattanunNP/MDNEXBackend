import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")

load_dotenv(dotenv_path)

MONGODB_USER = str(
    os.environ.get(
        "MONGODB_URL",
        "mongodb+srv://admin:8ZY4f8ybNyWV1wa0@mdnex.ijnzy.mongodb.net/UserDB?retryWrites=true&w=majority",
    )
)


REFRESH_SECERET_KEY = str(
    os.environ.get(
        "REFRESH_SECERET_KEY",
        "301772f9a90a90375fd4b4a1efb0bcc10cb0ff50fc8843281cba49657111afe3",
    )
)

ACCESS_SECERET_KEY = str(
    os.environ.get(
        "ACCESS_SECERET_KEY",
        "10a4843d4f1edd92eeb9f2e2aa48a7a13d39be3be2ea64c8214a388be90fdcf5",
    )
)


MAILGUN_API_KEY = str(
    os.environ.get(
        "MAILGUN_API_KEY", "c56bc946827aea9f4e42562f4cc08f32-1d8af1f4-de20447d"
    )
)

MAILGUN_DOMAIN = str(os.environ.get("MAILGUN_DOMAIN", "noreply@mg.standupcode.co"))

ROOT_URL = str(os.environ.get("ROOT_URL", "http://127.0.0.1:8000"))

FRONTEND_URL = str(os.environ.get("FRONTEND_URL", "http://localhost:3000"))

SECERET_EMAIL_KEY = str(
    os.environ.get(
        "SECERET_EMAIL_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hc3RlckBzdGFuZHVwY29kZS5jbyIsInV1aWQiOiJkZDA1ZWRlNC02MTQ3LTQwNjYtYTdjZC1jOGY5ODcyODVlNmQifQ.4zQWyeTHUk7QeSl1nnpcPjN6RClhD7ytl4sTDm0OSm0",
    )
)

