import os
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_socketio import join_room, leave_room, send, SocketIO
from werkzeug.utils import secure_filename
import random
from string import ascii_uppercase
import base64

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "pdf", "docx", "txt"}

socketio = SocketIO(app)

# Dictionary to store room_number -> unique_code mappings
room_code_map = {}

def generate_unique_code(room_number):
    """Generate a unique code for a given room number and store the mapping."""
    if room_number in room_code_map:
        return room_code_map[room_number]  # Return existing unique code
    
    unique_code = "".join(random.choices(ascii_uppercase, k=6))  # Generate 6-character code
    room_code_map[room_number] = unique_code  # Store the mapping
    return unique_code


@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        room_number = request.form.get("code")  # Use this as room number
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=room_number, name=name)

        if join and not room_number:
            return render_template("home.html", error="Please enter a room code.", code=room_number, name=name)

        if create:
            room_number = str(random.randint(1, 9999))  # Generate a numeric room ID

        unique_code = generate_unique_code(room_number)  # Get unique code for the room

        session["room"] = unique_code  # Store the unique code in session
        session["name"] = name
        session["room_number"] = room_number  # Keep track of numeric room ID

        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room", methods=["GET"])
def room():
    """Display the room page with unique code and room number."""
    room = session.get("room")
    name = session.get("name")
    room_number = session.get("room_number")  # Get numeric room ID

    if not room or not name:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, room_number=room_number)


@socketio.on("message")
def message(data):
    """Handle incoming chat messages."""
    room = session.get("room")
    if not room:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["message"],
        "is_file": data.get("is_file", False)
    }

    send(content, to=room)
    print(f"{session.get('name')} said: {data['message']}")

@app.route("/leave", methods=["POST"])
def leave():
    """Allow a user to leave the chat room."""
    room = session.get("room")
    name = session.get("name")

    if room and name:
        leave_room(room)  
        send({"name": name, "message": "has left the room"}, to=room)
        print(f"{name} has left the room {room}")

    session.clear()  
    return redirect(url_for("home"))

@socketio.on("send_file")
def handle_file(data):
    """Handle file uploads."""
    room = session.get("room")
    if not room:
        return
    
    filename = secure_filename(data["filename"])
    file_data = base64.b64decode(data["file_data"])

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, "wb") as file:
        file.write(file_data)

    file_url = url_for('uploaded_file', filename=filename)
    
    socketio.emit("message", {
        "name": session.get("name"),
        "message": file_url,
        "is_file": True
    }, room=room)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on("connect")
def connect(auth):
    """Handle new user connections."""
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """Handle user disconnections."""
    room = session.get("room")
    name = session.get("name")

    if room and name:
        leave_room(room)
        send({"name": name, "message": "has left the room"}, to=room)
        print(f"{name} has left the room {room}")

    session.clear()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
