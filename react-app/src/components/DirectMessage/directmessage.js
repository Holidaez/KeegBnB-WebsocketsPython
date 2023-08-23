import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { io } from 'socket.io-client';
import { getDMS } from "../../store/messages";
let socket;

const Chat = () => {
    const [chatInput, setChatInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [incommingMessage, setIncommingMessage] = useState(null)
    const user = useSelector(state => state.session.user)
    const dms = useSelector(state => state.messages)

    const { userId, ownerId } = useParams()
    const dispatch = useDispatch()

    //! Async Logger Function
    useEffect(() => {
        console.log("message effect", messages)
    },[messages])

    //! This is a fire trick in react
    useEffect(() => {
        if(incommingMessage){
            setMessages([...messages, incommingMessage])
            setIncommingMessage(null)
        }
    },[incommingMessage])

    useEffect(() => {
        // open socket connection
        // create websocket
        socket = io();
        console.log("connected to dms socket")
        async function retrieveMessages() {
            const msgsFromBackend = await dispatch(getDMS(userId, ownerId))
            setMessages(msgsFromBackend)
        }
        retrieveMessages()
        socket.emit("chat", { user: user.username, msg: "has connected!", recipient_id: ownerId, sender_id: userId })
        socket.on("chat", (chat) => {
            setIncommingMessage(chat)
        })

        return (() => {
            socket.emit("chat", { user: user.username, msg: "has disconnected!", recipient_id: ownerId, sender_id: userId })
            console.log("disconnected")
            socket.disconnect()
        })
    }, [])

    const updateChatInput = (e) => {
        setChatInput(e.target.value)
    };
    // When we send a chat, we tell our socket in the backend what we're sending so that it can do work.
    const sendChat = (e) => {
        e.preventDefault()
        // setisSending(true)
        socket.emit("chat", { user: user.username, msg: chatInput, recipient_id: ownerId, sender_id: userId });
        // setisSending(false)
        setChatInput("")
    }

    return (user && (
        <div>
            <div>
                {dms && messages.length > 0 && messages.map((message, ind) => (
                    <div key={ind}>{`${message.sender?.username || message.user}: ${message.msg}`}</div>
                ))}
            </div>
            <form onSubmit={sendChat}>
                <input
                    value={chatInput}
                    onChange={updateChatInput}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    )
    )
};


export default Chat;
