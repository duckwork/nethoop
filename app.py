from flask import Flask, make_response, render_template
from yaml import safe_load

app = Flask(__name__)

VARS = {"title": "Writers of the Fediverse!", "version": "0.0.3"}


@app.route("/")
def root():
    return render_template("index.html", members=hoop_members(), **VARS)


@app.route("/feeds.xml")
def feeds_xml():
    response = make_response(
        render_template("feeds.xml", members=hoop_members(), **VARS)
    )
    response.headers["Content-Type"] = "application/xml"
    return response


def hoop_members():
    with open("data/members.yaml") as f:
        members = safe_load(f)
    return members


if __name__ == "__main__":
    app.run()
