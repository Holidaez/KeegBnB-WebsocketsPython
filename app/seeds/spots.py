from app.models import db, Spot, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other spots here if you want
def seed_spots():
    demo = Spot(
        name='The BatCave',
        lat='33.453',
        lng='32.568',
        state='Illinois',
        country='United States',
        city='Chicago',
        address= '1234 Wayne Str',
        description='A luxurious multiBillion Estate',
        price='464.78',
        owner_id=1,
    )
    marnie = Spot(
        owner_id=2,
        address='2222 Titan Ave',
        city='New York City',
        state='New York',
        country='Unite States',
        lat='90',
        lng='90.2',
        name='Titan`s Tower',
        description='Headquarters for the teen titans',
        price='222.22'
    )
    bobbie = Spot(
        owner_id=3,
        address='8889 Jordan St',
        city='Atlanta',
        state='Georgia',
        country='United States',
        lat='68.23',
        lng='23.31',
        name='Jordan`s club',
        description='All of the Jordans ever',
        price='672.90'
    )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the spots table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_spots():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.spots RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM spots"))

    db.session.commit()
