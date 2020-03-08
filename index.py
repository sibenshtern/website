from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template("base.html", title=title)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


