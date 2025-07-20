from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# The file where the single paste will be stored
DATA_FILE = "paste.txt"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get text from the form and save it to the file
        content = request.form.get('content', '')
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        # Redirect to the GET route to show the updated content
        return redirect(url_for('index'))

    # For a GET request, read the content from the file
    current_text = ""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_text = f.read()

    return render_template('index.html', current_text=current_text)

if __name__ == '__main__':
    # The host '0.0.0.0' makes the server accessible from outside the Docker container
    app.run(host='0.0.0.0', port=5000)