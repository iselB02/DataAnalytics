from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing-page.html')

@app.route('/sign-in')
def signin():
    return render_template('signin-page.html')

@app.route('/sign-up')
def signup():
    return render_template('signup-page.html')

if __name__ == "__main__":
    app.run(debug=True)
