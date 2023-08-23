import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { io } from 'socket.io-client';
import { getDMS } from "../../store/messages";
import { findASpot } from "../../store/spotsReducer";
let socket;

const LikeAReview = ({review}) => {
    console.log(review)
    const { spotId } = useParams()
    const [chatInput, setChatInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [isSending, setisSending]= useState(false)
    const user = useSelector(state => state.session.user)
    const dms = useSelector(state => state.messages)
    let messageList;
    if(dms){
        messageList = Object.values(dms)
    }
    const {userId, ownerId} = useParams()
    const dispatch = useDispatch()
    useEffect(() => {
        // open socket connection
        // create websocket
        socket = io();
        console.log("connected to review socket")
        socket.on("like", (like) => {
            dispatch(findASpot(spotId))
        })
        // when component unmounts, disconnect
        return (() => {
            console.log("disconnected from review socket")
            socket.disconnect()
        })
    }, [])

    const updateChatInput = (e) => {
        setChatInput(e.target.value)
    };
    // When we send a chat, we tell our socket in the backend what we're sending so that it can do work.
    const likeReview = (e) => {
        e.preventDefault()
        socket.emit("like", { user_id: user.id, review_id:review.id  });
    }
    const unlikeReview = (e) => {
        e.preventDefault()
        let needed_like = review.likes.filter(like => like.user === user.id)
        socket.emit("unlike", {"id":needed_like[0].id});
    }

   return(
    <>
        <p>Likes: {review.likes.length}</p>
        <div>
        {review && !review.likes.filter(like => like.user === user.id).length && (
                <button onClick={(e) => likeReview(e)}>Like</button>
            )}

        </div>
        {review && review.likes.filter(like => like.user === user.id).length && (
            <button onClick={(e) => unlikeReview(e)}>UnLike</button>
        )}
    </>
   )
};


export default LikeAReview;
