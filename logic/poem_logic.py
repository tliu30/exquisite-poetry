from models.poem import Poem
from models.segment import Segment
from extensions import db
import uuid
import sqlalchemy as sa


def create_new_poem(text: str, num_segments: int) -> Segment:
    poem = Poem(uid=str(uuid.uuid4()), num_segments=num_segments)
    db.session.add(poem)

    segment = Segment(
        uid=str(uuid.uuid4()),
        poem_uid=poem.uid,
        previous_segment_uid=None,
        text=text,
    )
    db.session.add(segment)
    db.session.commit()

    return segment


def create_next_segment(cur_segment: Segment) -> Segment:
    segment = Segment(
        uid=str(uuid.uuid4()),
        poem_uid=cur_segment.poem_uid,
        previous_segment_uid=cur_segment.uid,
        text=None,
    )
    db.session.add(segment)
    db.session.commit()

    return segment


def get_segment(segment_uid: str) -> Segment | None:
    query = sa.select(Segment).where(Segment.uid == segment_uid)
    return db.session.scalars(query).one_or_none()


def update_segment(segment: Segment, text: str) -> Segment | None:
    segment.text = text
    db.session.add(segment)
    db.session.commit()
    db.session.refresh(segment)


def get_poem(poem_uid: str) -> Poem:
    query = sa.select(Poem).where(Poem.uid == poem_uid)
    return db.session.scalars(query).one()


def get_all_segments(poem_uid: str) -> list[Segment]:
    first_segment_query = sa.select(Segment).where(
        Segment.poem_uid == poem_uid, Segment.previous_segment_uid.is_(None)
    )
    first_segment = db.session.scalars(first_segment_query).one()

    segments = [first_segment]
    while True:
        next_segment_query = sa.select(Segment).where(
            Segment.previous_segment_uid == segments[-1].uid
        )
        next_segment = db.session.scalars(next_segment_query).one_or_none()

        if not next_segment:
            break

        segments.append(next_segment)

    return segments


def is_the_poem_full(poem_uid: str) -> bool:
    poem_record = get_poem(poem_uid)

    if not poem_record:
        return False

    n_segments = len(get_all_segments(poem_uid))

    return poem_record.num_segments <= n_segments


def is_poem_done(poem_uid: str) -> bool:
    poem_record = get_poem(poem_uid)

    if not poem_record:
        return False

    n_complete_segments = 0
    for record in get_all_segments(poem_uid):
        if record.text is not None:
            n_complete_segments += 1

    return poem_record.num_segments <= n_complete_segments
