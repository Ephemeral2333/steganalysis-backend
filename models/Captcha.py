from exts import db


class Captcha(db.Model):
    __tablename__ = 'captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    captcha_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, captcha, captcha_time):
        self.email = email
        self.captcha = captcha
        self.captcha_time = captcha_time

    def __repr__(self):
        return f'<Captcha {self.email}>'
