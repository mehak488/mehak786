<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Exam Question Generator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f6f8;
      padding: 20px;
    }
    .container {
      max-width: 700px;
      margin: auto;
      background: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 { text-align: center; }
    label { font-weight: bold; }
    textarea, select, button {
      width: 100%;
      margin-top: 8px;
      margin-bottom: 16px;
      padding: 10px;
      font-size: 16px;
    }
    button {
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    button:hover { background: #1e40af; }
    .output {
      white-space: pre-wrap;
      background: #f1f5f9;
      padding: 15px;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Question Generator</h1>

    <label>Subject / Topic</label>
    <textarea id="topic" placeholder="e.g. Data Structures, DBMS, Web Development"></textarea>

    <label>Question Type</label>
    <select id="type">
      <option value="mcq">MCQs</option>
      <option value="short">Short Answer</option>
      <option value="long">Long Answer</option>
    </select>

    <label>Difficulty Level</label>
    <select id="difficulty">
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard">Hard</option>
    </select>

    <label>Number of Questions</label>
    <select id="count">
      <option value="5">5</option>
      <option value="10">10</option>
      <option value="15">15</option>
    </select>

    <button onclick="generateQuestions()">Generate Questions</button>

    <h3>Generated Questions</h3>
    <div id="result" class="output">Questions will appear here...</div>
  </div>

  <script>
    async function generateQuestions() {
      const topic = document.getElementById('topic').value;
      const type = document.getElementById('type').value;
      const difficulty = document.getElementById('difficulty').value;
      const count = document.getElementById('count').value;

      if (!topic) {
        alert('Please enter a topic');
        return;
      }

      document.getElementById('result').innerText = 'Generating questions...';

      /*
        BACKEND NOTE:
        Replace the fetch URL with your backend API.
        Backend should call OpenAI / any LLM.
      */

      try {
        const response = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic, type, difficulty, count })
        });

        const data = await response.json();
        document.getElementById('result').innerText = data.questions;
      } catch (error) {
        document.getElementById('result').innerText = 'Error generating questions.';
      }
    }
  </script>
</body>
</html>

<!-- ================= PYTHON BACKEND (Flask) =================
Save this as app.py -->

"""
Requirements:
- Python 3.9+
- pip install flask openai
"""

from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/api/generate', methods=['POST'])
def generate_questions():
    data = request.json

    topic = data.get('topic')
    q_type = data.get('type')
    difficulty = data.get('difficulty')
    count = data.get('count')

    prompt = f"""
    Generate {count} {difficulty} level {q_type} exam questions on the topic: {topic}.

    If MCQs, include 4 options.
    Do not include answers unless asked.
    Format clearly.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an exam question generator."},
                {"role": "user", "content": prompt}
            ]
        )

        questions = response['choices'][0]['message']['content']
        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

<!-- ================= END PYTHON BACKEND ================= -->
