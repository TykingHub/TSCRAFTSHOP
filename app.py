from flask import Flask, request, jsonify, send_from_directory
import os
import json
import secrets
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "purchases.json"


def load_purchases():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_purchases(purchases):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(purchases, file, indent=4, ensure_ascii=False)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/purchase", methods=["POST"])
def create_purchase():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Datos inválidos."
        }), 400

    minecraft = data.get("minecraft", "").strip()
    discord = data.get("discord", "").strip()
    kit = data.get("kit", "").strip()
    payment = data.get("payment", "").strip()

    if not minecraft or not discord or not kit:
        return jsonify({
            "success": False,
            "error": "Faltan datos."
        }), 400

    purchases = load_purchases()

    purchase_id = secrets.token_hex(6).upper()

    purchase = {
        "id": purchase_id,
        "minecraft": minecraft,
        "discord": discord,
        "kit": kit,
        "payment": payment,
        "status": "pending",
        "key": None,
        "created_at": datetime.utcnow().isoformat()
    }

    purchases.append(purchase)

    save_purchases(purchases)

    return jsonify({
        "success": True,
        "purchase_id": purchase_id,
        "message": "Compra registrada correctamente."
    })


@app.route("/api/purchase/<purchase_id>", methods=["GET"])
def get_purchase(purchase_id):

    purchases = load_purchases()

    for purchase in purchases:

        if purchase["id"] == purchase_id:

            return jsonify({
                "success": True,
                "purchase": purchase
            })

    return jsonify({
        "success": False,
        "error": "Compra no encontrada."
    }), 404


@app.route("/api/health")
def health():

    return jsonify({
        "success": True,
        "server": "TSCRAFTSHOP",
        "status": "online"
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
  )
