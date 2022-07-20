from flask import Flask
from flask import render_template
from flask import make_response
from flask import redirect, url_for, request
app = Flask(__name__)

ADMIN_TOKEN = '@#V$RFv23WBTGNEEBXdfYNHdYTi*&695Hcdfw'
ADMIN_OTP = 95840392837495028193

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # TODO: implement login when actual accounts get added
    return render_template('failure.html')

@app.route('/guest_login',methods = ['POST','GET'])
def guest_login():
    resp = redirect(url_for('homepage'))
    resp.set_cookie('account_type','guest')

    return resp

@app.route('/home')
def homepage():
    if 'account_type' in request.cookies:
        if request.cookies.get('account_type') == 'admin':
            if request.cookies.get('admin_token') == ADMIN_TOKEN:
                return render_template('success.html')
            return redirect(url_for('otp_landing'))
        return render_template('homepage.html')
    return redirect(url_for('index'))

@app.route('/otp')
def otp_landing():
    if request.cookies.get('account_type') == 'admin':
        return render_template('oneTimePassowrd.html')
    return redirect(url_for('homepage'))

@app.route('/logout')
def logout():
    resp = redirect(url_for('index'))
    for cookie in request.cookies:
        resp.set_cookie(cookie, '')
    return resp

@app.route('/otp/authenticate', methods=['POST'])
def authenticate_otp():
    # throws error if user enters non-integer password
    # just wrap it in a try/catch for now
    try:
        if int(request.form.get('psw')) != ADMIN_OTP:
            resp = redirect(url_for('login'))
            resp.set_cookie('account_type','')
            return resp
    except:
        pass
    resp = redirect(url_for('homepage'))
    resp.set_cookie('admin_token',ADMIN_TOKEN)
    return resp

if __name__ == '__main__':
    app.run()
