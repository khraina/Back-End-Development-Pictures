from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Find a picture by its ID in the data list"""
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200

    return jsonify({"message": "picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Extract picture data from request and append to data list"""
    new_picture = request.get_json()

    # Check if the picture with the given ID already exists
    for picture in data:
        if picture.get("id") == new_picture.get("id"):
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # If it doesn't exist, append it to the data list
    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture in the data list with incoming request data"""
    updated_data = request.get_json()

    # Find the picture by ID
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            # Update the entry in the list
            data[index] = updated_data
            return jsonify(data[index]), 201

    # If the ID was not found in the loop
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture from the data list by its ID"""
    for picture in data:
        if picture.get("id") == id:
            data.remove(picture)
            # Return an empty body with 204 status
            return "", 204

    # If the picture does not exist, return 404
    return jsonify({"message": "picture not found"}), 404