import os
import google.generativeai as genai
import re
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model - using 2.5-flash for better free tier compatibility
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction="""You are a financial advisor. Create investment recommendations as JSON.

Always respond with ONLY valid JSON (no markdown, no ```json``` blocks).

Response format:
{
  "nodes": [
    {"id": "start", "position": {"x": 250, "y": 50}, "data": {"label": "Investment\\n₹Amount"}, "style": {"background": "bg-blue-100", "border": "border-blue-500"}},
    {"id": "option1", "position": {"x": 50, "y": 200}, "data": {"label": "Asset Class\\n₹Amount"}, "style": {"background": "bg-indigo-100", "border": "border-indigo-500"}}
  ],
  "edges": [
    {"id": "e1", "source": "start", "target": "option1", "label": "Percentage%", "style": {"stroke": "stroke-indigo-500"}}
  ]
}

Create 3-5 investment options based on their risk profile and amount."""
)

def get_gemini_response(user_input: str, risk: str) -> dict:
    """Get financial path recommendation from Gemini"""
    try:
        chat_session = model.start_chat(history=[])
        prompt = f"Investment amount: {user_input}\nRisk profile: {risk}\n\nProvide investment allocation as JSON only."
        
        response = chat_session.send_message(prompt)
        response_text = response.text.strip()
        
        # Try to parse as JSON directly
        if response_text.startswith('{'):
            resp = json.loads(response_text)
            return resp
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            resp = json.loads(json_match.group(1))
            return resp
        
        # Try to extract any JSON object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            resp = json.loads(json_match.group(0))
            return resp
        
        # If all fails, return a default structure
        return get_default_response(user_input, risk)
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return get_default_response(user_input, risk)
    except Exception as e:
        print(f"Error in get_gemini_response: {e}")
        return get_default_response(user_input, risk)

def get_default_response(user_input: str, risk: str) -> dict:
    """Return a default financial path recommendation"""
    if "conservative" in risk.lower():
        return {
            "nodes": [
                {"id": "start", "position": {"x": 250, "y": 50}, "data": {"label": f"Investment\n{user_input}"}, "style": {"background": "bg-blue-100", "border": "border-blue-500"}},
                {"id": "fixed", "position": {"x": 50, "y": 200}, "data": {"label": "Fixed Deposits\n40%"}, "style": {"background": "bg-green-100", "border": "border-green-500"}},
                {"id": "bonds", "position": {"x": 250, "y": 200}, "data": {"label": "Bonds\n35%"}, "style": {"background": "bg-blue-100", "border": "border-blue-500"}},
                {"id": "gold", "position": {"x": 450, "y": 200}, "data": {"label": "Gold\n25%"}, "style": {"background": "bg-yellow-100", "border": "border-yellow-500"}}
            ],
            "edges": [
                {"id": "e1", "source": "start", "target": "fixed", "label": "40%", "style": {"stroke": "stroke-green-500"}},
                {"id": "e2", "source": "start", "target": "bonds", "label": "35%", "style": {"stroke": "stroke-blue-500"}},
                {"id": "e3", "source": "start", "target": "gold", "label": "25%", "style": {"stroke": "stroke-yellow-500"}}
            ]
        }
    else:  # Moderate or aggressive
        return {
            "nodes": [
                {"id": "start", "position": {"x": 250, "y": 50}, "data": {"label": f"Investment\n{user_input}"}, "style": {"background": "bg-blue-100", "border": "border-blue-500"}},
                {"id": "index", "position": {"x": 50, "y": 200}, "data": {"label": "Index Funds\n40%"}, "style": {"background": "bg-indigo-100", "border": "border-indigo-500"}},
                {"id": "midcap", "position": {"x": 250, "y": 200}, "data": {"label": "Mid-Cap Stocks\n35%"}, "style": {"background": "bg-orange-100", "border": "border-orange-500"}},
                {"id": "gold", "position": {"x": 450, "y": 200}, "data": {"label": "Gold\n25%"}, "style": {"background": "bg-yellow-100", "border": "border-yellow-500"}}
            ],
            "edges": [
                {"id": "e1", "source": "start", "target": "index", "label": "40%", "style": {"stroke": "stroke-indigo-500"}},
                {"id": "e2", "source": "start", "target": "midcap", "label": "35%", "style": {"stroke": "stroke-orange-500"}},
                {"id": "e3", "source": "start", "target": "gold", "label": "25%", "style": {"stroke": "stroke-yellow-500"}}
            ]
        }

if __name__ == "__main__":
    test_query = "I have 10 lakh rupees"
    print("Test Query:", test_query)
    response = get_gemini_response(test_query, "moderate")
    print("Response:", json.dumps(response, indent=2))
