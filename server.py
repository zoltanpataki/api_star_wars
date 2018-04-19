from flask import Flask, render_template, redirect, request, session, url_for
import common
app = Flask(__name__)
table_header = ['Name', 'Diameter', 'Climate', 'Terrain', 'Surface water percentage', 'Population', 'Residents']
app.secret_key = 'ducimucijuci'


@app.route('/')
def index():
    return render_template('form.html', table_header=table_header)


@app.route('/registration')
def registration_or_login():
    state = 'Registration'
    return render_template('login.html', state=state)


@app.route('/save-registration', methods=['POST'])
def user_regist():
    error_message = ""
    username = request.form['username']
    password = request.form['password']
    hashed_password = common.hash_password(password)
    all_users = common.user_select()
    for user in all_users:
        if username == user['username']:
            error_message = "Sorry, but this username is taken! :("
            state = "Registration"
            return render_template('login.html', error_message=error_message, state=state)
    common.add_user(username, hashed_password)
    return redirect('/')


@app.route('/login')
def login():
    state = 'Login'
    return render_template('login.html', state=state)


@app.route('/valid-login', methods=['POST'])
def login_validation():
    error_message = ""
    login_username = request.form['username']
    login_password = request.form['password']
    hashed_password = common.hash_password(login_password)
    user = common.get_user(login_username, hashed_password)
    if len(user) == 0:
        error_message = "Oooppsss, that's a wrong username or password!"
        state = "Login"
        return render_template('login.html', error_message=error_message, state=state)
    else:
        session['username'] = login_username
        session['user_id'] = user[0]['id']
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect('/')


def main():
    app.run(
        debug=True,
        port=5000
    )

if __name__ == '__main__':
    main()