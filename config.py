import os

user_name = os.getenv("SEC_USER_NAME", "Default Name")
user_email = os.getenv("SEC_USER_EMAIL", "default@email.com")

# SEC EDGAR
HEADERS = {"User-Agent": f"{user_name} ({user_email})"}

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"