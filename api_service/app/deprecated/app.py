from flask import Flask, render_template, request
import utils
from test import *

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/submit", methods = ["POST", "GET"])
def submit():

    data = request.form


    print(data['text[]'])

    example = check_token(data['text[]'])

    input_len = len(example.split())
    size = data['length[]']# DEFINIDO PELO USUÁRIO DEFAULT 50
    
    output = query({"inputs": example,
                "parameters": {'repetition_penalty': float(1.2), 'num_beams':5,
                               'no_repeat_ngram_size':3, 'max_length':input_len + int(size)}})
    print(output[0].get('generated_text'))
    

    
    return render_template('index.html', suggestion_text=remove_token(output[0].get('generated_text')))

@app.route("/social")
def social():
    return render_template('social.html')

@app.route("/members")
def members():
    return render_template('members.html')




if __name__ == "__main__":
    app.run()