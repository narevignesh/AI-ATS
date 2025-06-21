from app import create_app
from app.extensions import mongo
from app.models.user_model import find_user_by_email, create_user

app = create_app()

def ensure_default_admin():
    admin_email = 'vigneshnaidu022@gmail.com'
    admin_password = 'vignesh123@MBU'
    admin_name = 'NARE VIGNESH'
    if not find_user_by_email(mongo, admin_email):
        create_user(mongo, admin_name, admin_email, admin_password, role='admin', is_verified=True)
        print('Default admin user created.')
    else:
        print('Default admin user already exists.')

if __name__ == '__main__':
    with app.app_context():
        ensure_default_admin()
    app.run(debug=True) 