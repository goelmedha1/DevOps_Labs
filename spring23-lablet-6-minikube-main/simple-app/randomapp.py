import random
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    # Increment the view count
    number = random.randint(0, 10)
    return f"You will get {number} random things.\n"

app.run(host="0.0.0.0" , port=80)