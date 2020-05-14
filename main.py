from flask import Flask, flash, render_template, request, session
from flask_bootstrap import Bootstrap
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

# generate random secret key so flash can run
app.config['SECRET_KEY'] = os.urandom(24)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/words', methods=['GET','POST'])
def words():
    # check if GET or POST:
    if request.method == 'POST':
        wordInfo = request.form
        inputWord = wordInfo['inputWord']
        buttonValue = wordInfo['submit-button']
        print(inputWord, buttonValue)
        if buttonValue == 'add':
            flash('Word Added.', 'success')
            # add word to database
        elif buttonValue == 'delete':
            flash('Word Deleted.', 'success')
            # delete word from database
        else:
            flash('Something went wrong. Your word was not added.', 'danger')

        #create variable that holds database entries and pass to html page
        return render_template('words.html')
    #create variable that holds database entries and pass to html page
    return render_template('words.html')

if __name__ == '__main__':
    app.run(debug=True)
