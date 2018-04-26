from . import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(250))  
    email = db.Column(db.String(80))
    location = db.Column(db.String(255))
    biography = db.Column(db.Text)
    proPhoto = db.Column(db.String(80))
    joined_on = db.Column(db.DateTime)
    
    def __init__(self,firstname,lastname,username,password,email,location,biography,proPhoto,joined_on):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email
        self.location = location
        self.biography = biography
        self.proPhoto = proPhoto
        self.joined_on = joined_on
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.userName)
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    photo = db.Column(db.String(80))
    caption = db.Column(db.Text)
    created_on = db.Column(db.DateTime)
    
    def __init__(self,userID,photo,caption,created_on):
        self.userID = userID
        self.photo  = photo
        self.caption = caption
        self.created_on = created_on

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    postID = db.Column(db.Integer)
    
    def __init__(self,userID,postID):
        self.userID = userID
        self.postID = postID
    
class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    followerID = db.Column(db.Integer)
    
    def __init__(self,userID,followerID):
        self.userID = userID
        self.followerID = followerID
    