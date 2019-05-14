from flask import Flask

nethoop = Flask(__name__)

@nethoop.route('/')
def root():
    return "Nethoop v. 0.0.1"

if __name__ == '__main__':
    nethoop.run()
