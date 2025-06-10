from BookingSystem import create_app
from flask_login import logout_user

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    logout_user()

# only run webserver if this file is run

