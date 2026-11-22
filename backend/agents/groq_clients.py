
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client():

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Check your .env file."
        )

    return Groq(api_key=GROQ_API_KEY)


def generate_response(prompt):

    client = get_groq_client()

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=1200
    )

    return completion.choices[0].message.content


if __name__ == "__main__":

    try:
        answer = generate_response(
            "Explain what a hospital incident reporting procedure is "
            "in two simple sentences."
        )

        print("\n========== GROQ RESPONSE ==========")
        print(answer)
        print("\nGroq API test successful!")

    except Exception as error:
        print("\nGroq API test failed:")
        print(error)
