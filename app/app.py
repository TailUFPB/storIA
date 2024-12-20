from flask import Flask, render_template, request
from story import Story_generator
from utils import storia_logger

story_generator = Story_generator()

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    """
    Main page of the app, where the user can input the text, choose the length and temperature of the story
    This page also shows the generated story, if left empty, it generates a story from scratch
    The user can also access the social media and members pages
    """
    return render_template('index.html')

@app.route("/submit", methods = ["POST", "GET"])
def submit():
    """
    Params: text, length and temperature
    Returns: generated story
    """
    data = request.form
    input_text = data.get('text[]') # Default text not needed, it creates from scratch if empty
    size = int(data.get('length[]')) # Default size comes from the form
    temperature = float(data.get('temperature[]')) # Default temperature also comes from the form

    try:
        story = story_generator.generate_story(input_text, size, temperature)
        return render_template('index.html', suggestion_text=story), storia_logger.info(f"Story generation successful")
    
    except Exception as e:
        return render_template('index.html', suggestion_text=f"Error generating story:\n{e}"), storia_logger.error(f"Error generating story: {e}")

@app.route("/social")
def social():
    return render_template('social.html')

@app.route("/members")
def members():
    return render_template('members.html')

if __name__ == "__main__":
    app.run()