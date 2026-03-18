from flask import Flask, redirect, render_template, request, session, url_for
from flask import render_template
import random

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'apki_secret_key_yahan_likhein'

# Define a route and its handler
@app.route('/', methods=['GET'])
def home():
    # Agar session mein target number nahi hai, toh naya banao
    if 'target' not in session:
        session['target'] = random.randint(1, 100)
        session['attempts'] = 1
    
    return render_template('index.html')


@app.route('/contact')
def contact():               
    return render_template('contact.html')
@app.route('/about')
def about():            
    return render_template('about.html')

@app.route('/guess', methods=['POST', 'GET'])
def guess():

    # Console mein check karne ke liye
    print(f"Current Session Data: {session}") 
    
    target = session.get('target')
    print(f"Secret Target is: {target}")

    if request.method == 'POST':
        number_guess = request.form.get('guessNumber')

    
    if target is not None:
        number_guess = int(number_guess)
        attempts = session.get('attempts', 0)
        session['attempts'] = attempts + 1

        if number_guess < int(target):
            feedback = "Too low! Try again."
        elif number_guess > int(target):
            feedback = "Too high! Try again."
        else:
            feedback = f"Congratulations! You've guessed the number in {session['attempts']} attempts."
            session.pop('target', None)  # Game over, remove target from session
            session.pop('attempts', None)  # Reset attempts for new game

    return render_template('index.html', feedback=feedback, number_guess=number_guess, attempts=attempts)

@app.route('/reset')
def reset():
    # Session se game ka data saaf karna
    session.pop('target', None)
    session.pop('attempts', None)
    # Wapas home page par bhejna jahan naya number generate hoga
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
