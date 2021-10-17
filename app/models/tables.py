from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Collumn(db.Integer, primary_key=True)
    username = db.Collumn(db.String(80), unique=True)
    password = db.Collumn(db.String(20))
    name = db.Collumn(db.String())
    email = db.Collumn(db.String(20), unique=True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Collumn(db.Integer, primary_key=True)
    content = db.Collumn(db.Text)
    user_id = db.Collumn(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return "<Post %r>" % self.id


class Follow(db.Model):
    __tablename__ = "follow"

    id = db.Collumn(db.Integer, primary_key=True)
    user_id = db.Collumn(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Collumn(db.Integer, db.ForeignKey('users.id'))

    user = db.relatioship('User', foreign_keys=user_id)
    follower = db.relatioship('User', foreign_keys=user_id)
