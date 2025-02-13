from config.db import db

class TagItemModel(db.Model):
    __tablename__ = "tag_items"

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    items_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)