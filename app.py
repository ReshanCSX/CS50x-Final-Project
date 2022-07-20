from flask import Flask, redirect, render_template, request

#app configuration
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def default():

    return render_template("index.html")