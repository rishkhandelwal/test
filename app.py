from flask import Flask, request, jsonify, render_template
import docx
from groq import Groq
from dotenv import load_dotenv
import os
import io

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

app = Flask(__name__)

def chat_with_openai(docx_file, user_input):
    # Extract the text from the docx file
    doc = docx.Document(io.BytesIO(docx_file.read()))
    text = ''
    for para in doc.paragraphs:
        text += para.text
    # Create a prompt from the text
    prompt = [{"role": "system","content": """Keep your answers very short, compact and concise. 
    Your answers should be deep into the context of Relationships. 
    If the user asked for any content which belongs to a different Coach, you should guide them to check out the Coach related to the input. 
    Don't comment on prompt(input). Provide response as a human would. 
    Don't reply to negative questions regarding any religion."""}, {"role": "user", "content": text + user_input}]
    # Call the Groq API
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=prompt
    )
    # Return the response
    response = chat_completion.choices[0].message.content
    sentences = response.split('. ')
    return sentences

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/api/manager-chat', methods=['POST'])
def chat():
    try:
        docx_file = request.files.get('docx_file')
        user_input = request.form.get('user_input')
        
        if not docx_file or not user_input:
            return jsonify({'error': 'Missing docx_file or user_input'}), 400
        
        response = chat_with_openai(docx_file, user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
