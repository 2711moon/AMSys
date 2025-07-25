from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def init_extensions(app):
    csrf.init_app(app)
