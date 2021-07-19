from flask import Flask, render_template, request
import utils

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/submit", methods = ["POST", "GET"])
def submit():

    config = request.form
    print('antes')

    features = utils.preprocess(config)

    print(features)

    
    return render_template('index.html', suggestion_text='texto sugerido.....')

@app.route("/social")
def social():
    return render_template('social.html')

@app.route("/members")
def members():
    return render_template('members.html')




if __name__ == "__main__":
    app.run()