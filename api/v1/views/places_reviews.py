#!/usr/bin/python3
"""places.py"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_get(place_id):
    """retrieves Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=["DELETE", ["PUT", "GET"]],
                 strict_slashes=False)
def delete_or_get_rev(review_id):
    """deletes,gets, or puts a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.todict())
    if request.method == "DELETE":
        storage.delete(review)
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            reviews = request.json()
            ignores = ['id', 'created_at', 'updated_at', 'place_id']
            for key, value in reviews.items():
                if key not in ignores:
                    setattr(review, key, value)
            storage.save()
            return make_response(jsonify(review.to_dict()), 200)

    @app_views.route('/places/<place_id>/reviews', methods=['POST'],
                     strict_slashes=False)
    def review_post(place_id):
        """makes new review"""
        review = request.get_json()
        place = storage.get_json()
        if place is None:
            abort(404)
        if not review:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if "user_id" not in review.keys():
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if storage.get(User, review["user_id"]) is None:
            abort(404)
        if "text" not in review.keys():
            return make_response(jsonify({'error': 'Missing text'}), 400)
        new_review = Review(**review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
