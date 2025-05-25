from flask import Flask, request, jsonify
from src.trade_simulator import log_trade
from src.parser import parse_alert
from src.notifier import send_telegram_alert
from src.trade_filter import passes_filters
from src.data import get_recent_candles
from src.trade_simulator import simulate_trade
def create_app():
    app = Flask(__name__)
    @app.route("/webhook", methods=["POST"])
    def webhook():
        try:
            data = request.get_json(force=True)
            if not data:
                return jsonify({"status": "error", "message": "Empty JSON body"}), 400
        
            trade_info = parse_alert(data)

            if not trade_info:
                return jsonify({"status": "error", "message": "Missing or invalid fields in alert"}), 422
            candles_ltf = get_recent_candles(trade_info["symbol"], "m1")
            candles_htf = get_recent_candles(trade_info["symbol"], "1h")
            if not passes_filters(trade_info, candles_ltf, candles_htf):
                return jsonify({"status": "rejected", "message": "Trade filtered out"}), 200

            if not passes_filters(trade_info, candles_ltf, candles_htf):
                 return jsonify({"status": "rejected", "message": "Trade filtered out"}), 200
            if passes_filters(trade_info, candles_ltf, candles_htf):
                simulate_trade(trade_info)
            else:
                print("🚫 Trade rejected by filters.")
            log_trade(trade_info)
            send_telegram_alert(trade_info)
            print("Received alert: {data}")
        
        
            return jsonify({"status": "success", "message": "Trade logged"}), 200
        
            
        except Exception as e:
            return jsonify({"status": "error", "message":f"Server error: {str(e)}"}), 400
    return app