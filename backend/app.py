from flask import Flask, request, jsonify
from onboard import *
from flask_cors import CORS
import subprocess
import re
from jgaad_ai_agent_backup import jgaad_chat_with_gemini
import gemini_fin_path
from logger_config import log_request, log_error, log_info

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    log_info('Home endpoint accessed')
    return jsonify({'status': 'BudgetIQ API is running', 'version': '1.0'})

# =================== DYNAMIC APIS ===================
@app.route('/agent', methods=['POST'])
def agent():
    try:
        inp = request.form.get('input')
        if not inp:
            return jsonify({'error': 'No input provided'}), 400

        print(f"Received query: {inp}")
        
        # First try direct Gemini response
        try:
            direct_response = jgaad_chat_with_gemini(inp)
            if direct_response:
                return jsonify({
                    'output': direct_response,
                    'source': 'gemini',
                    'status': 'success'
                })
        except Exception as e:
            print(f"Gemini direct response failed: {str(e)}")
        
        # Fallback to agent if Gemini fails
        try:
            process = subprocess.Popen(
                ['python', 'agent.py', inp],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            output = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    print(f"Agent output: {line.strip()}")
                    output.append(line)
            
            output_str = ''.join(output)
            process.wait()

            final_answer = re.search(r'<Response>(.*?)</Response>', output_str, re.DOTALL)
            if final_answer:
                return jsonify({
                    'output': final_answer.group(1).strip(),
                    'thought': output_str,
                    'source': 'agent',
                    'status': 'success'
                })
            else:
                return jsonify({
                    'error': 'Could not extract response from agent',
                    'raw_output': output_str
                }), 500
                
        except Exception as e:
            print(f"Agent processing failed: {str(e)}")
            return jsonify({
                'error': f'Agent processing failed: {str(e)}',
                'status': 'error'
            }), 500
            
    except Exception as e:
        print(f"General error in /agent endpoint: {str(e)}")
        return jsonify({
            'error': f'An unexpected error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/ai-financial-path', methods=['POST'])
def ai_financial_path():
    if 'input' not in request.form:
        return jsonify({'error': 'No input provided'}), 400
        
    input_text = request.form.get('input','')
    risk = request.form.get('risk', 'conservative')
    print(input_text)
    try:
        response = gemini_fin_path.get_gemini_response(input_text, risk)
        return jsonify(response)
    except Exception as e:
        print(f"Error in ai_financial_path: {str(e)}")
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500

# =================== STATIC APIS ===================
@app.route('/auto-bank-data', methods=['GET'])
def AutoBankData():
    return bank_data

@app.route('/auto-mf-data', methods=['GET'])
def AutoMFData():
    return mf_data


# =================== CONENCTION APIS ===================

# =================== BOTS ===================
# @

if __name__ == "__main__":
    app.run(debug=True)