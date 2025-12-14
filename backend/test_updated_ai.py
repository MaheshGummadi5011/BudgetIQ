import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

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

model = genai.GenerativeModel(
    'models/gemini-2.5-flash',
    system_instruction=system_instruction,
    generation_config={'temperature': 0.7, 'max_output_tokens': 1500}
)

print('='*70)
print('TEST 1: Stock Price Query')
print('='*70)
chat = model.start_chat()
response = chat.send_message('what is the stock price of Adani green')
print(response.text)

print('\n' + '='*70)
print('TEST 2: Investment Recommendation')
print('='*70)
chat2 = model.start_chat()
response2 = chat2.send_message('Should I invest in IT companies now?')
print(response2.text)

print('\n' + '='*70)
print('TEST 3: Budgeting Advice')
print('='*70)
chat3 = model.start_chat()
response3 = chat3.send_message('What is a good monthly savings percentage?')
print(response3.text)

print('\n' + '='*70)
print('✓ ALL TESTS COMPLETED')
print('='*70)
