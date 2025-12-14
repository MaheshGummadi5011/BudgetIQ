import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

load_dotenv()

# Configure API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Test 1: Check if model is available
print("=" * 50)
print("TEST 1: Checking available models")
print("=" * 50)
try:
    for m in genai.list_models():
        if 'gemini' in m.name.lower():
            print(f"✓ Found: {m.name}")
except Exception as e:
    print(f"✗ Error listing models: {e}")

# Test 2: Test Gemini 1.5 Flash (known working)
print("\n" + "=" * 50)
print("TEST 2: Testing Gemini 1.5 Flash (baseline)")
print("=" * 50)
try:
    model_flash = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-002",
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 500,
        }
    )
    
    chat_flash = model_flash.start_chat(history=[])
    response_flash = chat_flash.send_message("What is budgeting?")
    
    print(f"✓ Gemini 1.5 Flash Response:")
    print(f"  Length: {len(response_flash.text)} characters")
    print(f"  Preview: {response_flash.text[:200]}...")
    
except Exception as e:
    print(f"✗ Gemini 1.5 Flash Error: {e}")

# Test 3: Test Gemini 2.5 Pro
print("\n" + "=" * 50)
print("TEST 3: Testing Gemini 2.5 Pro")
print("=" * 50)
try:
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    system_instruction = """You are a knowledgeable personal financial advisor. Provide concise, practical financial advice."""
    
    model_pro = genai.GenerativeModel(
        model_name="models/gemini-2.5-pro",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )
    
    chat_pro = model_pro.start_chat(history=[])
    print("Sending test query to Gemini 2.5 Pro...")
    
    response_pro = chat_pro.send_message("What is a good monthly budget allocation for savings?")
    
    print(f"✓ Gemini 2.5 Pro Response:")
    print(f"  Length: {len(response_pro.text)} characters")
    print(f"  Preview: {response_pro.text[:200]}...")
    
except Exception as e:
    print(f"✗ Gemini 2.5 Pro Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Compare quality with financial question
print("\n" + "=" * 50)
print("TEST 4: Quality Comparison (Financial Question)")
print("=" * 50)

test_question = "Should I invest in IT companies right now given current market conditions?"

try:
    print("\nGemini 1.5 Flash Response:")
    chat1 = model_flash.start_chat(history=[])
    resp1 = chat1.send_message(test_question)
    print(resp1.text[:300] + "...")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nGemini 2.5 Pro Response:")
    chat2 = model_pro.start_chat(history=[])
    resp2 = chat2.send_message(test_question)
    print(resp2.text[:300] + "...")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
