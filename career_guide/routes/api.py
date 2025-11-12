# career_guide/routes/api.py
from flask import Blueprint, request, jsonify
from career_guide.services.retrieve import retrieve_career_kb

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/retrieve_kb", methods=["POST"])
def retrieve_kb():
    """
    API endpoint to retrieve career knowledge base entries.
    Tries semantic search first, falls back to keyword search.
    """
    try:
        data = request.get_json(silent=True) or {}
        query = data.get("query", "").strip()
        top_k = data.get("top_k", 5)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Use hybrid retrieval
        results = retrieve_career_kb(query, top_k)

        return jsonify({
            "query": query,
            "count": len(results),
            "results": results
        }), 200

    except Exception as e:
        print("❌ API /retrieve_kb error:", e)
        return jsonify({"error": "Internal server error"}), 500
