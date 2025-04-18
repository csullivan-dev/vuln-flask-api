from app.extensions import db
from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.now().date())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)