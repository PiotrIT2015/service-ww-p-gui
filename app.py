from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Funkcja do komunikacji z silnikiem Java
def run_java_engine(input_data):
    try:
        # Wywołanie silnika Java
        process = subprocess.Popen(['java', '-jar', 'engine.jar'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        output, error = process.communicate(input=input_data)
        if process.returncode != 0 or error:
            return f"Error: {error}"
        return output.strip()
    except Exception as e:
        return str(e)

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint do przetwarzania danych użytkownika
@app.route('/process', methods=['POST'])
def process():
    user_input = request.form.get('user_input')
    result = run_java_engine(user_input)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
