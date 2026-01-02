"""
Direct test of Gemini API without ADK.
"""

import os
import asyncio
from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()

async def test_direct_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    use_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    model_name = os.environ.get("DEFAULT_MODEL", "gemini-2.0-flash")

    print(f"Model: {model_name}")
    print(f"Use Vertex: {use_vertex}")
    
    if use_vertex:
        client = Client(vertexai=True, project=project, location="us-central1")
    else:
        client = Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Write a 1-paragraph summary of the Saradha Chit Fund Scam."
        )
        print("\n--- Response ---")
        print(response.text)
        print(f"Length: {len(response.text)} chars")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_gemini())
