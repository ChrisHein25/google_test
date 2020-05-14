from flask import Flask, flash, render_template, request, session
from flask_bootstrap import Bootstrap
import yaml

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

if __name__ == '__main__':
    app.run(debug=True)
