import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.8,
  "top_k": 40,
  "max_output_tokens": 1500,
}

system_instruction = """You are "BudgetIQ AI", a knowledgeable and helpful personal financial advisor. You assist users with all aspects of financial planning, analysis, and decision-making.

Your capabilities include:
- Stock price information and market analysis
- Company financial data and performance analysis
- Investment recommendations and strategies
- Portfolio management guidance
- Budgeting and expense tracking
- Retirement planning
- Debt management and elimination
- Tax planning considerations
- Emergency fund planning
- Risk tolerance assessment
- Market trends and economic insights

Guidelines:
1. Provide clear, accurate, and helpful financial information
2. Use available research data when provided to enhance your responses
3. Offer balanced perspectives on investment decisions
4. Acknowledge limitations (e.g., real-time updates may have a cutoff date)
5. Encourage users to consult professionals for personalized advice
6. Be conversational, friendly, and engaging
7. Help users understand financial concepts clearly
8. Provide practical, actionable insights

Answer all financial queries comprehensively. If you don't have real-time data, explain what information you do have and suggest where they can find current data. Do NOT refuse to answer financial questions - instead, provide the best answer you can with available information.
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
        if research:
            prompt += f"Research Information:\n{research}\n\n"
        prompt += f"Question: {query}\n\nPlease provide a detailed analysis and answer."
        
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