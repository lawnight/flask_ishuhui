from ishuhui.extensions.flasksqlalchemy import db
import ishuhui.data


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True, unique=True) # 废弃
    title = db.Column(db.String(256), nullable=False)
    comic_id = db.Column(db.Integer, nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False) # 第几章
    front_cover = db.Column(db.String(256), nullable=True)
    refresh_time = db.Column(db.DateTime, nullable=True)
    images = db.Column(db.Text, nullable=True)

    def comic(self):
        return ishuhui.data.get_comic(self.comic_id)
