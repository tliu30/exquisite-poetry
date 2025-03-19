from extensions import db
from sqlalchemy.orm import Mapped, mapped_column


class Segment(db.Model):
    uid: Mapped[str] = mapped_column(primary_key=True)
    poem_uid: Mapped[str]
    previous_segment_uid: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)

    @property
    def incomplete(self):
        return self.text is None
