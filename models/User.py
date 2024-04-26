from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, join_date):
        self.email = email
        self.join_date = join_date

    def __repr__(self):
        return f'<User {self.email}>'
