# Flask Chat & File Transfer Application

This project is a real-time chat and file-sharing application built using Flask and Flask-SocketIO. Users can join chat rooms with a specific room code and share messages or files with other participants.

## Installation

### Requirements

To run this project, you need the following installed on your system:

- Python 3.x
- Flask
- Flask-SocketIO

### Installation Steps

1. Install the required dependencies:

   ```sh
   pip install flask flask-socketio eventlet werkzeug
Start the application:

sh
Copy
Edit
python app.py
Open the following address in your browser:

arduino
Copy
Edit
http://localhost:5000
Application Features
Creating & Joining Rooms
Users can create a new room or join an existing room using a room code.
A unique room code is generated for each room, allowing users to communicate within the same chat.
Real-Time Messaging
Flask-SocketIO enables real-time communication between users.
Messages are instantly delivered to all users in the room.
File Sharing
Users can share images, documents, or text files.
Files are encoded in base64 format and securely stored on the server.
Users receive a file link to access shared files.
User Connection & Disconnection
When a user joins, they are automatically added to the chat room.
When a user disconnects, a notification is sent to other users.
API Endpoints
/ (Home Page)
GET: Returns the user login page.
POST: Allows users to log in and redirects them to a chat room.
/room
GET: Redirects the user to their chat room.
/leave
POST: Allows the user to leave the current chat room.
/uploads/<filename>
GET: Allows users to retrieve uploaded files from the server.
Usage Scenarios
Scenario 1: User Creates a New Room
The user enters a username.
Clicks the "Create Room" button.
The system generates a random room number and unique code.
The user is redirected to the chat room.
Scenario 2: User Joins an Existing Room
The user enters a username and room number.
Clicks the "Join Room" button.
The user is connected to the existing chat room.
Scenario 3: User Sends a Message
The user types a message and clicks the "Send" button.
The message is instantly delivered to all room members.
Scenario 4: User Shares a File
The user selects and uploads a file.
The file is saved on the server, and a download link is shared in the chat room.
This application allows seamless real-time communication and file sharing among users in different rooms.
