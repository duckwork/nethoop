from flask import Flask, render_template
from yaml import safe_load

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html', members=hoop_members())


def hoop_members():
    with open('data/members.yaml') as f:
        members = safe_load(f)
    return members


if __name__ == '__main__':
    app.run()
