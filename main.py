from flask import Flask, g, flash, render_template, request, session
from flask_bootstrap import Bootstrap
import yaml
import os
import sqlite3
#import dbfunc

app = Flask(__name__)
Bootstrap(app)

# generate random secret key so flash can run
app.config['SECRET_KEY'] = os.urandom(24)

# SQL Database Functions
DATABASE = 'database.db'

def addWord(word):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO words(word) VALUES(?)", (word,))
    con.commit()
    con.close()

def deleteWord(word):
    # NEED TO ADD TRY EXCEPT BLOCK W BOOL LOGIC
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM words WHERE word=?", (word,))
    con.commit()
    con.close()

def printWords(): # prints entire table to command line
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM words")
    words = cur.fetchall()
    con.close()
    print(words)
    return

def getWordTable():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM words")
    wordTable = cur.fetchall()
    con.close()
    return wordTable


##### Browser Routing #####

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
        #print(inputWord, buttonValue)
        if buttonValue == 'add':
            # add word to database
            addWord(str(inputWord))
            flash('Word Added.', 'success')
        elif buttonValue == 'delete':
            # delete word from database
            deleteWord(str(inputWord))
            flash('Word Deleted.', 'success')
        else:
            flash('Something went wrong. Your word was not added.', 'danger')
        wordTable = getWordTable() # table in list
        return render_template('words.html', wordTable = wordTable)
    wordTable = getWordTable() # table in list
    return render_template('words.html', wordTable = wordTable)

if __name__ == '__main__':
    app.run(debug=True)
