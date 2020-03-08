from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/<string:title>')
@app.route('/index/<string:title>')
def index(title):
    return render_template("base.html", title=title)


@app.route('/list_prof/<list_type>')
def show_professions_list(list_type):
    return render_template("professions_list.html", list_type=list_type,
                           title="Список профессий")


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


