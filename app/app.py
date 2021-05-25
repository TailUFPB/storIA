from flask import Flask, render_template, request
import utils

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()