from app.models import db, Review, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo Review, you can add other reviews here if you want
def seed_reviews():
    demo = Review(
        spot_id=1,
        user_id=2,
        review="OMG ITS SO HIGH TECH YASSSSSS",
        stars=5
    )
    marnie = Review(
        spot_id=1,
        user_id=2,
        review="Batman is so cool",
        stars=4
    )
    bobbie = Review(
        spot_id=1,
        user_id=2,
        review="I Got to meet robin =D",
        stars=3
    )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the reviews table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
