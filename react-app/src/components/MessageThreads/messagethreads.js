import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import { getThreads } from "../../store/threads";


const MessageThreads = () => {
    const user = useSelector(state => state.session.user)
    const threads = useSelector(state => state.threads)
    const history = useHistory()
    const dispatch = useDispatch()
    //On Mount, fetch all of the threads from the backend and load them in.
    useEffect(() => {
        const userId = user.id
        const threads = dispatch(getThreads(userId))
        console.log(threads)
    },[])
    // Function to Create a dynamic redirect to the actual thread
    const redirectToThread = (e, user, thread) =>{
        e.preventDefault()
        console.log(thread, user)
        let path = `/directmessage/${user.id}/${thread.id}`
        history.push(path)
    }
    return (
        <div>
            {threads && Object.values(threads).map(thread => (
                <div>
                    <button onClick={(e) => redirectToThread(e,user,thread)}>{thread.username}</button>
                </div>
            ))}
        </div>
    )
}


export default MessageThreads
