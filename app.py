from flask import Flask, request
from yaml import safe_load

nethoop = Flask(__name__)

@nethoop.route('/')
def root():
    ret = "Nethoop v. 0.0.1"
          "Members: "+hoop_members('data/members.yaml')
    return ret

def hoop_members(fname):
    return yaml.safe_load(fname)

if __name__ == '__main__':
    nethoop.run()
