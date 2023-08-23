from app.models import db, Review, environment, SCHEMA, Like
from sqlalchemy.sql import text


def seed_likes():
    seed1 = Like(
        user_id = 1,
        review_id = 1,
    )
    seed2 = Like(
        user_id = 2,
        review_id = 1,
    )
    seed3 = Like(
        user_id = 3,
        review_id = 1,
    )
    seed_lst = [seed1,seed2,seed3]

    for seed in seed_lst:
        db.session.add(seed)
    db.session.commit()

# Uses a raw SQL query to TRUNCATE or DELETE the reviews table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_likes():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.likes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM likes"))

    db.session.commit()
