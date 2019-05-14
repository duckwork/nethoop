from flask import Flask
from yaml import safe_load

app = Flask(__name__)


@app.route('/')
def root():
    ret = ("Nethoop v. 0.0.1" "Members: " + hoop_members())
    return ret


def hoop_members():
    with open('data/members.yaml') as f:
        members = safe_load(f)
    return members


if __name__ == '__main__':
    app.run()
