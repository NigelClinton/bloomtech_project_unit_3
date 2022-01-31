from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.BIGINT, primary_key=True, nullable=False)
    name = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f'[<User: {self.name}>]'


class Tweet(db.Model):
    id = db.Column(db.BIGINT, primary_key=True, nullable=False)
    text = db.Column(db.Unicode(300), nullable=False)
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    vect = db.Column(db.PickleType, nullable=False)


    def __repr__(self):
        return f'[Tweet: {self.text}]'
