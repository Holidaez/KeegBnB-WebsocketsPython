
const SEND_THREADS = 'messages/threads'

const saveThreads = (threads) => {
    return {
        type: SEND_THREADS,
        threads
    }
}

export const getThreads = (userId) => async (dispatch) => {
    console.log(userId)
    const res = await fetch(`/api/messages/threads/${userId}`)
    if (res.ok){
        const threads = await res.json()
        dispatch(saveThreads(threads))
    }else throw new Error("Bad Request")
}


export default function threadsReducer(state = {}, action){
    let newState = {}
    switch(action.type){
        case SEND_THREADS:
            newState = {}
            action.threads.forEach((thread) => newState[thread.id] = thread)
            return newState
        default:
            return state
    }
}
