from flask import Blueprint, jsonify, session, request
from app.models import User, db, DirectMessage
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_, and_

message_routes = Blueprint('message', __name__)


#! Get All Messages Route
@message_routes.route('/<sender_id>/<recipient_id>')
def get_all_dms(sender_id, recipient_id):
    #Query all dms from the database between 2 users where the id's line up
    dms = DirectMessage.query.filter(DirectMessage.sender_id == int(sender_id), DirectMessage.recipient_id == int(recipient_id)).all()
    #Query the Reverse ids from the database so that you get all messages between 2 users.
    dms2 = DirectMessage.query.filter(DirectMessage.sender_id == int(recipient_id), DirectMessage.recipient_id == int(sender_id)).all()
    #Append the 2 lists of messages together
    for d in dms2:
        dms.append(d)
    #Initialize the Message list im going to send to the frontend
    dm_list = []
    #"List Comprehension for dms"
    for dm in dms:
        #Query the User that send the message and make it a dictionary
        sender = User.query.get(dm.sender_id)
        sender_dict = sender.to_dict()
        #Query the User that recieved the message and make it a dictionary
        recipient = User.query.get(dm.recipient_id)
        recipient_dict = recipient.to_dict()
        #Turn the Message itself to a dictionary
        dm_dict = dm.to_dict()
        #Create new Key:Value pairs inside of the dictionary for the sender and recipient
        dm_dict['sender'] = sender_dict
        dm_dict['recipient'] = recipient_dict
        #Append the dictionary to our return list
        dm_list.append(dm_dict)
    return dm_list

#! Get all Message Threads Route
@message_routes.route('/threads/<id>')
def get_all_threads(id):
    #Query all Direct Messages where the user was the sender or the recipient
    threads = DirectMessage.query.filter(or_(DirectMessage.sender_id == int(id), DirectMessage.recipient_id == int(id))).all()
    #Initialize our user list
    userlist = []
    #Iterate through our threads
    for thread in threads:
        #Query the recipient User
        recieved_from = User.query.get(thread.sender_id)
        #Query the sending User
        sent_to = User.query.get(thread.recipient_id)
        #Check to see if the User is in the User List, If it is not add it to the User List
        if recieved_from not in userlist:
            userlist.append(recieved_from)
        if sent_to not in userlist:
            userlist.append(sent_to)
    #initialize our list to be returned to the frontend
    user_threads = []
    #Turn all of our users into Dictionaries to be send back (We don't care about the messages right now just who we have sent messages to)
    for user in userlist:
        user_threads.append(user.to_dict())
    return user_threads
