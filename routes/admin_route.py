from flask import Blueprint, request, jsonify
from services.stats_service import (
    bussiness_stats as bussiness,
    products_stats as products,
    tags_stats as tags,
    users_stats as users,
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/stats", methods=["GET"])
def stats():
    bussiness_stats = bussiness()
    users_stats = users()
    products_stats = products()
    tags_stats = tags()
    return jsonify(
        {
            "bussiness": bussiness_stats,
            "users": users_stats,
            "products": products_stats,
            "tags": tags_stats,
        }
    )
