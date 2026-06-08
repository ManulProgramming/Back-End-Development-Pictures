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
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################

def get_picture_by_id_method(id):
    if data:
        tmp_data=[d for d in data if d.get("id",-1)==id]
        if tmp_data:
            return tmp_data[0], 200
        else:
            return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res=get_picture_by_id_method(id)
    return jsonify(res[0]), res[1]


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture=request.json
    if picture:
        status=get_picture_by_id_method(picture.get("id",-1))
        if status[1]!=200:
            data.append(picture)
            return jsonify(picture), 201
        elif status[1]==200:
            return {"Message": f"picture with id {picture.get('id',-1)} already present"}, 302
    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture=request.json
    if picture:
        og=get_picture_by_id_method(picture.get("id",-1))
        if og[1]==200:
            data.remove(og[0])
            data.append(picture)
            return jsonify(picture), 200
        elif og[1]==404:
            return og[0], 404
        
    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    og=get_picture_by_id_method(id)
    if og[1]==200:
        data.remove(og[0])
        return "", 204
    elif og[1]==404:
        return og[0], 404
        
    return {"message": "Internal server error"}, 500
