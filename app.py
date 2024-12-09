from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session storage (although not used now)

@app.route('/')
def landingPage():
    return render_template('landing-page.html')

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
def createnew():
    return render_template('create-new.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/browse-file')
def browseFile():
    return render_template('browse.html')

@app.route('/account-setting')
def accountSetting():
    return render_template('account-setting.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')


if __name__ == "__main__":
    app.run(debug=True)
