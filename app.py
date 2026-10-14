from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():

    # Get JSON data sent by the client
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Check that title exists
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Get the title
    title = data["title"]

    # Validate that title is a string
    if not isinstance(title, str):
        return jsonify({"error": "Title must be a string"}), 400

    # Remove unnecessary spaces
    title = title.strip()

    # Make sure title isn't empty
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    # Generate a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create the new Event object
    new_event = Event(new_id, title)

    # Add the event to our in-memory list
    events.append(new_event)

    # Return the newly created event
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):

    # Get JSON data sent by the client
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Check that title exists
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Validate that title is a string
    if not isinstance(data["title"], str):
        return jsonify({"error": "Title must be a string"}), 400

    # Remove unnecessary spaces
    title = data["title"].strip()

    # Make sure title isn't empty
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    # Find the event
    for event in events:

        if event.id == event_id:

            # Update the title
            event.title = title

            # Return the updated event
            return jsonify(event.to_dict()), 200

    # Event wasn't found
    return jsonify({
        "error": f"Event with id {event_id} not found"
    }), 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({
        "error": f"Event with id {event_id} not found"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)