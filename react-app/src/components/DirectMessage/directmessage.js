import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { io } from 'socket.io-client';
import { getDMS } from "../../store/messages";
let socket;

const Chat = () => {
    const [chatInput, setChatInput] = useState("");
    /*
        Need 2 slices of localized state in order to control the messages displayed to the user.
        Slice #1 (messages) is the array of messages we're going to render out to the user.
        Slice #2 (incommingMessage) stores the information recieved from the socket listener and is utlilized by a second useEffect to update the messages slice of state with new (not stale) state
        Without Slice #2 the messages do not update properly on render because the socket listener is stuck with old state for messages when pushed onto the stack. (this is a "common" issue in react)
    */
    const [messages, setMessages] = useState([]);
    const [incommingMessage, setIncommingMessage] = useState(null)

    // Common Selectors
    const user = useSelector(state => state.session.user)
    const dms = useSelector(state => state.messages)

    const { userId, ownerId } = useParams()
    const dispatch = useDispatch()

    //! Async Logger Function that logs out our messages every time it changes feel free to comment out.
    useEffect(() => {
        console.log("message effect", messages)
    },[messages])

    //! This is a fire trick in react (reference comments on Slice #2)
    // This useEffect ensures that we are using the most up-to-date messages solving our issue with the initial render, making use of both slices of state to update our messages array.
    useEffect(() => {
        //! This if statement ensures that we will not get an infinite loop because we are setting Incomming messages to null breaking the useEffect firing cycle.
        // We have incomingMessage in the dependency array because we need this useEffect to fire each time a new chat is recieved from the socket
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
        //! Async helper function to retrieve the messages from the backend, it must be async so that the remainder of our useEffect waits to run.
        async function retrieveMessages() {
            const msgsFromBackend = await dispatch(getDMS(userId, ownerId))
            setMessages(msgsFromBackend)
        }
        // Invokes our helper function
        retrieveMessages()

        // This tells all users in the chat that x user has connected, our listener in the backend filters this message out so that it does not get saved to the db
        socket.emit("chat", { user: user.username, msg: "has connected!", recipient_id: ownerId, sender_id: userId })
        //! Whenever our socket recieves an emission of "chat" this function fires, setting our incommming message to the value of chat (an object)
        socket.on("chat", (chat) => {
            //! Causes our useEffect to run setting messages to all of the old messages as well as the newly recieved message
            setIncommingMessage(chat)
        })
        //! Only runs when the componentn unmounts or this useEffect fires again (which never happens)
        return (() => {
            // Emits a chat that states that x user has disconnected, our listener in the backend filters this message out so it is not saved in the DB (will flood the message thread)
            socket.emit("chat", { user: user.username, msg: "has disconnected!", recipient_id: ownerId, sender_id: userId })
            console.log("disconnected")
            // Disconnects the use from the socket pool
            socket.disconnect()
        })
    }, [])

    const updateChatInput = (e) => {
        setChatInput(e.target.value)
    };
    // When we send a chat, we tell our socket in the backend what we're sending so that it can do work.
    const sendChat = (e) => {
        e.preventDefault()
        socket.emit("chat", { user: user.username, msg: chatInput, recipient_id: ownerId, sender_id: userId });
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
