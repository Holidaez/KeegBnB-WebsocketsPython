import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import { Redirect, useParams, useHistory } from "react-router-dom";
import { getAllSpots, findASpot } from '../../store/spotsReducer'
import { Link } from 'react-router-dom'
import './GetASpot.css'
import LikeAReview from '../LikeAReview/LikeAReview';

export default function CurrentSpotDetails() {
    const { spotId } = useParams()
    const history = useHistory()
    const dispatch = useDispatch()
    const spots = useSelector(state => state.spots)
    const user = useSelector(state => state.session.user)

    useEffect(() => {
        dispatch(findASpot(spotId))
    }, [])
    let spotReviews;
    if (spots && spots.reviews) {
        let reviewNumber = 1
        spotReviews = spots.reviews.map((review) => {
            return (
                <li key={review.id} className="user-reviews">
                    <div className={`review${reviewNumber++}`}>
                        <div className="review-name-stars">
                            <p className="user-name">{review.user.username}: </p>
                            <p className="star-paragraph"><i className="fa-solid fa-star star-icon"></i>{review.stars}</p>
                        </div>

                        <p className="actual-review"> {review.review}</p>
                        <p>
                            {user && user.id === review.user.id && (
                                <Link to={`/review/delete/${spotId}/${review.id}`} className="delete-review-link">Delete Review</Link>
                            )}
                        </p>
                            <LikeAReview review={review} spotId={spotId}/>
                        
                    </div>
                </li>
            )
        })

    }

    let image;
    if (spots && spots.images) {
        image = spots.images.map((img) => {
            return (
                <img src={img} alt="image Not Found" className="detail-image"></img>
            )
        })
    }

    let unique;
    if (spots && spots.reviews && user) {
        let test = spots.reviews
        unique = test.filter(review => review.id === user.id)
    }

    let owner;
    if (spots){
        owner = spots.owner
    }
    //Function to dynamically redirect to a thread
    function redirectToMessage(e, user, owner){
        e.preventDefault()
        console.log(user, owner)
        let path = `/directmessage/${user.id}/${owner.id}`
        history.push(path)
    }

    return (
        <div className="spot-details-container">
            <button onClick={(e)=> redirectToMessage(e, user, owner)}>Message Host</button>
            <div className="header-div">

                <h1 className="spot-name">{spots.name}</h1>
                <div className="button-div">
                    {spots.owner && user && user.id === spots.owner.id && (
                        <p className="owner-options">
                            {spots.owner && user && user.id === spots.owner.id && (
                                <Link to={`/delete/${spots.id}`} className="link">Delete Spot</Link>
                            )}
                        </p>
                    )}
                    {spots.owner && user && user.id === spots.owner.id && (
                        <p className="owner-options">
                            {spots.owner && user && user.id === spots.owner.id && (
                                <Link to={`/update/${spots.id}`} className="link">Edit</Link>
                            )}
                        </p>
                    )}
                </div>

            </div>

            <div className="img-container">
                {image}
            </div>
            {spots.owner && (
                <h2 className="detail-block">{`Owned By: ${spots.owner.username}`}</h2>
            )}
            <div className="detail-block">

                <h3 className="city-state">{`${spots.city}, ${spots.state}`}</h3>
                <p className="address">Address: {spots.address}</p>
                <p className="price">${spots.price} per night</p>

                <h3 className="description-container-spot-details">About This Place:</h3>
                <p className="description">{spots.description}</p>

                {spots.rating !== "NaN" && (
                    <h3 className="spot-rating">Rating:  <i className="fa-solid fa-star"></i> {spots.rating}</h3>
                )}

                {spots.rating === "NaN" && (
                    <p className="spot-rating-no-review">No Reviews</p>
                )}
            </div>
            {spots.reviews && (
                <ul className="review-list">
                    {spotReviews}
                </ul>
            )}
            <div className="review-button-container">
                <p className="review-button">
                    {(!spots.reviews || (spots.owner && user && user.id !== spots.owner.id && spots.reviews && unique.length < 1)) && (
                        <Link to={`/create/review/${spots.id}`} className="link">Leave Your Review</Link>
                    )}
                </p>
            </div>
        </div>
    )

}
