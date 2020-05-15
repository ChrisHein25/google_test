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
DATABASE = './database.db'

def addWord(word):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM words WHERE word=?;", (word,))
    existingCount = cur.fetchone()[0]
    if existingCount == 0:
        print(existingCount)
        cur.execute("INSERT INTO words(word) VALUES(?);", (word,))
        con.commit()
        con.close()
        return True
    else:
        return False

def deleteWord(word):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM words;")
    initialCount = cur.fetchone()[0]
    cur.execute("DELETE FROM words WHERE word=?;", (word,))
    con.commit()
    cur.execute("SELECT COUNT(*) FROM words;")
    finalCount = cur.fetchone()[0]
    con.close()
    if initialCount == finalCount:
        return False
    else:
        return True

def deleteAll():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM words;")
    cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME = 'words';")
    con.commit()
    con.close()

def printWords(): # prints entire table to command line
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM words;")
    words = cur.fetchall()
    con.close()
    print(words)
    return

def getWordTable():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM words;")
    wordTable = cur.fetchall()
    con.close()
    return wordTable


##### Browser Routing #####

@app.route('/')
def index():
    title = 'index'
    return render_template('index.html', title=title)

@app.route('/notbuilt')
def notbuilt():
    title = 'notbuilt'
    return render_template('notbuilt.html', title=title)

@app.route('/words', methods=['GET','POST'])
def words():
    title = 'words'
    # check if GET or POST:
    if request.method == 'POST':
        wordInfo = request.form
        inputWord = wordInfo['inputWord']
        inputWord = str(inputWord).strip(" ").lower().replace(" ", "") # clean up input word
        buttonValue = wordInfo['submit-button']
        #print(inputWord, buttonValue)
        if buttonValue == 'add':
            # add word to database
            if len(inputWord) > 0:
                if addWord(inputWord):
                    flash('Word added.', 'success')
                else:
                    flash('Please enter a valid word.', 'danger')
            else:
                flash('Please enter a valid word.', 'danger')
        elif buttonValue == 'delete':
            # delete word from database
            if deleteWord(inputWord):
                flash('Word deleted.', 'success')
            else:
                flash('Please enter a valid word or make sure the table has a value.', 'danger')
        elif buttonValue == 'delete_all':
            # display warning message??
            deleteAll()
            flash('All entries deleted.','success')
        else:
            flash('Something went wrong. Your word was not added.', 'danger')
        wordTable = getWordTable() # table in list
        return render_template('words.html', wordTable = wordTable, title=title)
    wordTable = getWordTable() # table in list
    return render_template('words.html', wordTable = wordTable, title=title)

if __name__ == '__main__':
    app.run(debug=True)
