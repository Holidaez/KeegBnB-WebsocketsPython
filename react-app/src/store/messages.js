const GET_MESSAGES = 'messages/getMessages'

const getMessages = (messages) => {
    return {
        type: GET_MESSAGES,
        messages
    }
}

export const getDMS = (userId, ownerId) => async (dispatch) => {
    const res = await fetch(`/api/messages/${userId}/${ownerId}`)
    if (res.ok){
        const messages = await res.json()
        dispatch(getMessages(messages))
        return messages
    }else throw new Error("Bad Request")
}

export default function messageReducer(state = {}, action){
    let newState = {}
    switch(action.type){
        case GET_MESSAGES:
            newState = {}
            console.log(action.messages)
            action.messages.forEach((message) => newState[message.id] = message)
            return newState
        default:
            return state
    }
}
