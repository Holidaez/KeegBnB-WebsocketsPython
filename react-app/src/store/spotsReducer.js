
const GET_SPOTS = 'spots/getSpots'

const GET_A_SPOT = 'spots/getASpot'

const getSpots = (spots) => {
    return {
        type: GET_SPOTS,
        spots
    }
}

const getASpot = (spot) => {
    return {
        type: GET_A_SPOT,
        spot
    }
}

export const getAllSpots = () => async (dispatch) => {
    const response = await fetch('/api/spots/')
    if (response.ok){
        const spots = await response.json()
        dispatch(getSpots(spots))
        
    }else throw new Error("Bad Request")
}

export const findASpot = (spotId) => async (dispatch) => {
    const res = await fetch(`/api/spots/${spotId}`)
    if (res.ok) {
        const spot = await res.json()
        dispatch(getASpot(spot))
    }else throw new Error("Invalid Spot Id")
}
export default function spotsReducer(state = {}, action) {
    let newState = {}
    switch (action.type){
        case GET_SPOTS:
            newState = {}
            action.spots.forEach((spot) => newState[spot.id] = spot)
            return newState
        case GET_A_SPOT:
            newState = {...action.spot}
            return newState
        default:
            return state
    }
}
