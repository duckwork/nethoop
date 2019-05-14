from flask import Flask, make_response, render_template
from yaml import safe_load

app = Flask(__name__)

TITLE = "Writers of the Fediverse!"


@app.route("/")
def root():
    return render_template("index.html", title=TITLE, members=hoop_members())


@app.route("/feeds.xml")
def feeds_xml():
    response = make_response(
        render_template("feeds.xml", title=TITLE, members=hoop_members())
    )
    response.headers["Content-Type"] = "application/xml"
    return response


def hoop_members():
    with open("data/members.yaml") as f:
        members = safe_load(f)
    return members


if __name__ == "__main__":
    app.run()
