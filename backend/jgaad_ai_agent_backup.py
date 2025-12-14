import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from stock_data import get_stock_price, get_stock_week_return, resolve_stock_symbol

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.6,
  "top_p": 0.85,
  "top_k": 40,
  "max_output_tokens": 600,
}

system_instruction = """You are "BudgetIQ AI" - a financial advisor that ALWAYS provides direct answers.

CRITICAL - MUST DO:
1. ALWAYS give a direct answer about stocks, prices, and investments
2. NEVER suggest "check Google Finance" or "ask elsewhere"
3. NEVER ask users to find information elsewhere
4. ALWAYS answer in 2-4 sentences with actual information
5. If you know approximate prices from your training data, provide them
6. Be confident and helpful

For stock questions: Provide analysis and information you have.
For financial questions: Give practical advice directly.

Your job: Answer questions completely. Don't redirect users. Don't apologize. Just help them.
"""

# Use Gemini 2.5 Flash instead of Pro for better free tier compatibility
model = genai.GenerativeModel(
  model_name="models/gemini-2.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction,
)

def jgaad_chat_with_gemini(query, research=''):
    try:
        # Start a new chat session for each request
        chat_session = model.start_chat(history=[])
        
        # Prepare the prompt
        prompt = ""
        
        # Check if query is about stock prices or returns
        stock_data_info = ""
        query_lower = query.lower()
        
        try:
            if "stock price" in query_lower or "price of" in query_lower:
                # Extract stock name/symbol
                words = query.split()
                potential_symbol = None
                for i, word in enumerate(words):
                    if "price" in word.lower() and i + 1 < len(words):
                        potential_symbol = words[i + 1]
                        break
                
                if potential_symbol:
                    symbol = resolve_stock_symbol(potential_symbol)
                    price = get_stock_price(symbol)
                    if price:
                        stock_data_info = f"Current stock price for {potential_symbol}: {price}"
            
            elif "return" in query_lower or "performance" in query_lower:
                # Extract stock name for return info
                words = query.split()
                for i, word in enumerate(words):
                    if "return" in word.lower() and i > 0:
                        potential_symbol = words[i - 1]
                        symbol = resolve_stock_symbol(potential_symbol)
                        week_return = get_stock_week_return(symbol)
                        if week_return:
                            stock_data_info = f"Last week's return for {potential_symbol}: {week_return}"
                        break
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            # Continue without stock data if there's an error
        
        # Build the prompt with real data
        if research:
            prompt += f"Research Information:\n{research}\n\n"
        
        if stock_data_info:
            prompt += f"Real Data Available: {stock_data_info}\n\n"
        
        prompt += f"Question: {query}\n\nAnswer this directly in 2-3 sentences using the real data provided. Be concise and helpful."
        
        print(f"Sending query to Gemini 2.5 Flash: {query}")
        response = chat_session.send_message(prompt)
        print(f"Received response from Gemini")
        
        if not response or not response.text:
            return "I apologize, but I couldn't generate a response at this time. Please try again."
            
        return response.text
    except Exception as e:
        error_str = str(e)
        print(f"Error in chat_with_gemini: {error_str}")
        
        # Provide helpful error messages
        if "quota" in error_str.lower() or "429" in error_str:
            return "I'm temporarily rate-limited by the API. Please try again in a moment. For better performance, consider upgrading your API plan."
        elif "not found" in error_str.lower() or "404" in error_str:
            return "The AI model is temporarily unavailable. Please try again shortly."
        else:
            return f"I encountered an error while processing your request. Please try again later."
  
if __name__ == "__main__":
  # Sample test query
  test_query = "Research that should i invest in IT-companies now?"
  print("Test Query:", test_query)
  response = jgaad_chat_with_gemini(test_query)
  print("Response:", response)