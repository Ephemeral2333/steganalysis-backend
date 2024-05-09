from exts import db


class TestModel(db.Model):
    __tablename__ = 'test_model'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1 = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    state = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, u_id, name, precision, recall, f1, accuracy, created_time):
        self.u_id = u_id
        self.name = name
        self.precision = precision
        self.recall = recall
        self.f1 = f1
        self.accuracy = accuracy
        self.created_time = created_time
        self.state = 0

    def __repr__(self):
        return f'<TestModel {self.url}>'

    def assign(self, url, precision, recall, f1, accuracy):
        self.url = url
        self.precision = precision
        self.recall = recall
        self.f1 = f1
        self.accuracy = accuracy
        self.state = 1
        db.session.commit()
