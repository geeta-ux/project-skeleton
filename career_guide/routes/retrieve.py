# career_guide/routes/retrieve.py
from flask import Blueprint, jsonify, request
from career_guide.services.retrieve import retrieve_career_kb

retrieve_bp = Blueprint("retrieve", __name__)

@retrieve_bp.route("/api/retrieve_kb", methods=["POST"])
def retrieve_kb():
    try:
        data = request.get_json() or {}
        query = data.get("query", "")
        results = retrieve_career_kb(query)
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
