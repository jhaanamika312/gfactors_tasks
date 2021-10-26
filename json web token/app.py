from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity


app = Flask(__name__)


app.config['SECRET_KEY'] = 'anamika'


def token_required(func):
    
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
       
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'

# Just to show you that a public route is available for everyone


@app.route('/public')
def public():
    return 'For Public'

# auth only if you copy your token and paste it after /auth?query=XXXXXYour TokenXXXXX
# Hit enter and you will get the message below.


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '

# Login page


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '312':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)



if __name__ == "__main__":
     app.run(debug=True)