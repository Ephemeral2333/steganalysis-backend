from exts import db


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result = db.Column(db.Integer, nullable=False)
    u_result = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    image_show = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    # 添加外键关联
    user = db.relationship('User', backref=db.backref('history', lazy=True))

    def __init__(self, user_id, result, image, image_show, created_time):
        self.user_id = user_id
        self.result = result
        self.u_result = result
        self.image = image
        self.image_show = image_show
        self.created_time = created_time

    def __repr__(self):
        return f'<History {self.email}>'
