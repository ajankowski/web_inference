from flask import Flask

app = Flask(__name__)

@app.route('/')
def hallo():
    return 'Hallo World'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

