from flask import Flask, render_template, request, session, redirect, url_for
import os
import tempfile
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session storage

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    if request.method == 'POST':
        # Check if a file is in the request
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and file.filename.endswith('.csv'):
            # Save the file temporarily
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            file.save(temp_file.name)
            session['temp_file'] = temp_file.name  # Store the path in session
            return redirect(url_for('cleaning'))  # Redirect to /data-cleaning
    return render_template('landing-page.html')

@app.route('/data-cleaning', methods=['GET'])
def cleaning():
    temp_file_path = session.get('temp_file')
    if not temp_file_path or not os.path.exists(temp_file_path):
        return 'No file to display', 400

    # Read the CSV file into a DataFrame
    data = pd.read_csv(temp_file_path)
    table_html = data.to_html(classes='table table-striped', index=False)

    return render_template('data-cleaning.html', table_html=table_html)

@app.route('/sign-in')
def signin():
    return render_template('signin-page.html')

@app.route('/sign-up')
def signup():
    return render_template('signup-page.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create-new')
def create():
    return render_template('create-new.html')

@app.route('/browse-file')
def browseFile():
    return render_template('browse-file.html')

@app.route('/account-setting')
def accountSetting():
    return render_template('account-setting.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')


if __name__ == "__main__":
    app.run(debug=True)
