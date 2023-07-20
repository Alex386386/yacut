from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), unique=True, nullable=False)
    short = db.Column(db.String(128), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Вот он — новый метод:
    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_to_url', short_url=self.short,
                               _external=True),
        )
