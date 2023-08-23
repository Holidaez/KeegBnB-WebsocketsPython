from app.models import db, SpotImage, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a SpotImage user, you can add other spot_images here if you want
def seed_spot_images():
    demo = SpotImage(
        spot_id=1,
        url="https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?cs=srgb&dl=pexels-binyamin-mellish-186077.jpg&fm=jpg",
        preview_image=True

    )
    marnie = SpotImage(
        spot_id=1,
        url="https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?cs=srgb&dl=pexels-binyamin-mellish-186077.jpg&fm=jpg",
        preview_image=False

    )
    bobbie = SpotImage(
        spot_id=2,
        url="https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?cs=srgb&dl=pexels-binyamin-mellish-186077.jpg&fm=jpg",
        preview_image=True

    )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the spot_images table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_spot_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.spot_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM spot_images"))

    db.session.commit()
