import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import { getAllSpots } from '../../store/spotsReducer'
import { Link } from 'react-router-dom'
import './GetAllSpots.css'
import '../../index.css'


export default function SpotGetter() {
    const dispatch = useDispatch()
    const spots = useSelector(state => state.spots)
    useEffect(() => {
        dispatch(getAllSpots())
    }, [])

    const spotItems = Object.values(spots).map((spotItem) => {
        // console.log(spotItem)
        const rating = spotItem.rating !== "NaN" ? (
            <h4 className='spot-rating-get-spots'><i className="fa-solid fa-star">
            </i>{spotItem.rating}</h4>
        ) : (
            <p className='no-reviews'>No Reviews</p>
        )

        return (
            <li key={spotItem.id} className='spot-list-item'>
                <Link to={`/selectedSpot/${spotItem.id}`} className="link-get-spots">
                <img src={spotItem.preview_image} alt="image not found" className='image'></img>
                </Link>
                <div className='city-state-rating-div'>
                    <h3>{`${spotItem.city}, ${spotItem.state}`}</h3>
                    {rating}
                </div>

                <p className='spot-price'>${spotItem.price} night</p>
            </li>
        )
    })

return (
    <div className='home-page-container'>
        <ul className='spot-list'>
            {spotItems}
        </ul>
    </div>
)
}
