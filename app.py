from flask import Flask, session, request,redirect,render_template
import re

app = Flask(__name__)
app.secret_key = 'this is secret_key'

from views.page import page
from views.user import user

app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

@app.route('/')
def index():
    return redirect('/user/login')

@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    print(session.get('username'))
    if re.search(pat,request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    username = session.get('username')
    if username:
            return None
    return redirect('/user/login')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
