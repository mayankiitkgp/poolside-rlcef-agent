import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

print(f"✓ API key loaded: {api_key[:20]}...")

try:
    client = Groq(api_key=api_key)
    
    # Test simple completion
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Groq!' in one sentence."}
        ],
        max_tokens=50,
        temperature=0.5
    )
    
    print("\n✅ Groq API working!")
    print(f"Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"\n❌ API call failed: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. Model name incorrect")
    print("3. Network/firewall issue")
    print("4. Groq service down")

