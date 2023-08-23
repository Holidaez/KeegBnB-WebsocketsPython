from flask import Blueprint, jsonify, session, request
from app.models import User, db, Spot
from .auth_routes import validation_errors_to_error_messages
from app.forms import SpotForm
from flask_login import current_user, login_user, logout_user, login_required

spot_routes = Blueprint('spot', __name__)



@spot_routes.route('/')
def get_all_spots():
    """Get All Spots"""
    spots_list = Spot.query.all()
    return_list = []
    default_img = "https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?cs=srgb&dl=pexels-binyamin-mellish-186077.jpg&fm=jpg"
    for spot in spots_list:
        #Turn spots into dictionaries
        spot_dict = spot.to_dict()
        #Initialize the rating
        rating = 0
        #Get all associated reviews and their rating
        spot_reviews = spot.reviews
        for review in spot_reviews:
            rating += review.stars
        #Setting the rating in the spot
        if len(spot_reviews):
            spot_dict['rating'] = rating / len(spot_reviews)
        else:
            spot_dict['rating'] = rating
        #Get all spot images
        spot_images = spot.spot_images
        #Iterate through the images if there is a preview image set the url
        if len(spot_images):
            for image in spot_images:
                if image.preview_image == True:
                    spot_dict['preview_image'] = image.url
        #If a preview image was not set upload a preview image
        if not len(spot_images):
            spot_dict['preview_image'] = default_img

        #Get and Attach the Owner of the Spot
        owner = spot.owner
        spot_dict['owner'] = owner.to_dict()
        return_list.append(spot_dict)
    return return_list

@spot_routes.route('/<id>')
def get_selected_spot(id):
    """Get A selected spot by id"""
    selected_spot = Spot.query.get(id)
    #Turn spots into dictionaries
    spot_dict = selected_spot.to_dict()
    #Initialize the rating
    rating = 0
    #Get all associated reviews and their rating
    spot_reviews = selected_spot.reviews
    review_list = []
    review_image_list = []
    for review in spot_reviews:
        rating += review.stars
        review_image = review.review_images
        #Iterate through the review images
        for rev_image in review_image:
            review_image_list.append(rev_image.url)
        #turn the review into a dictionary
        final_review = review.to_dict()
        #add the image list
        final_review['images'] = review_image_list
        #! Attach the review creator to the review
        rev_user = review.user
        #! Add the user to the review
        final_review['user'] = rev_user.to_dict()

        #get the likes for this review
        rev_likes = [like.to_dict() for like in review.likes]
        final_review['likes'] = rev_likes
        #append the reivews to the spot
        review_list.append(final_review)


    #Setting the rating in the spot
    if len(spot_reviews):
        spot_dict['rating'] = rating / len(spot_reviews)
    else:
        spot_dict['rating'] = rating
    #Get all Images on the spot
    spot_images = selected_spot.spot_images
    #Initialize the image list
    image_list = []
    #For each Image add the url to the image list
    for image in spot_images:
        image_list.append(image.url)
    #Get and Attach the owner to the return object
    spot_owner = selected_spot.owner
    spot_dict['owner'] = spot_owner.to_dict()
    spot_dict['reviews'] = review_list
    spot_dict['images'] = image_list
    return spot_dict

@spot_routes.route('/create', methods=["POST"])
@login_required
def create_a_spot():
    form = SpotForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        new_spot = Spot(
            owner_id=form.data['owner_id'],
            name=form.data['name'],
            lat=form.data['lat'],
            lng=form.data['lng'],
            state=form.data['state'],
            country=form.data['country'],
            city=form.data['city'],
            address=form.data['address'],
            description=form.data['description'],
            price=form.data['price']
            )
        db.session.add(new_spot)
        db.session.commit()
    return {'errors': validation_errors_to_error_message(form.errors)},401

@spot_routes.route('/edit/<id>', methods=["PUT"])
@login_required
def update_your_spot(id):
    form = SongForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        spot_to_edit = Spot.query.get(id)
        spot_to_edit['name'] = form.data['name']
        spot_to_edit['lat'] = form.data['lat']
        spot_to_edit['lng'] = form.data['lng']
        spot_to_edit['state'] = form.data['state']
        spot_to_edit['country'] = form.data['country']
        spot_to_edit['city'] = form.data['city']
        spot_to_edit['address'] = form.data['address']
        spot_to_edit['description'] = form.data['description']
        spot_to_edit['price'] = form.data['price']
        db.session.commit()
        returning_value = spot_to_edit.to_dict()
        return returning_value
    return {'errors': validation_errors_to_error_messages(form.errors)},401

@spot_routes.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_your_spot(id):
    to_delete = Spot.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    return {"Message": "Spot Deleted Successfully"}
