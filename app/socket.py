from flask_socketio import SocketIO, emit
import os
from app.models import DirectMessage,db, Like
from app.forms import message_form
# socketio = SocketIO()

#! Needs to be changed for RENDER
if os.environ.get("FLASK_ENV") == "production":
    origins = []
else:
    origins = "*"

# create your SocketIO instance
socketio = SocketIO(cors_allowed_origins=origins)


# handle chat messages
@socketio.on("chat")
def handle_chat(data):
    if data['msg'] != "has connected!" or data['msg'] != 'has disconnected!':
        dm = DirectMessage(
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message=data['msg'],
            sent_at='hi'
        )
        db.session.add(dm)
        db.session.commit()
    emit("chat", data, broadcast=True)


# handle likes
@socketio.on('like')
def handle_like(data):
    if data != "User connected!":
        like = Like(
          user_id = data['user_id'],
          review_id = data['review_id']
        )
        db.session.add(like)
        db.session.commit()
    emit('like', data, broadcast=True)

# handle unlikes
@socketio.on('unlike')
def handle_like(data):
    if data != "User connected!":
        target_like = Like.query.get(data['id'])
        db.session.delete(target_like)
        db.session.commit()
    emit('like', data, broadcast=True)
