from extensions import db
from sqlalchemy.orm import Mapped, mapped_column


class Poem(db.Model):
    uid: Mapped[str] = mapped_column(primary_key=True)
    num_segments: Mapped[int]
