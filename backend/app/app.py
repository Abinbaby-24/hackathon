from flask import Flask, jsonify
from flask_cors import CORS


def create_app():

    app = Flask(__name__)

    # Allow React frontend to communicate with Flask
    CORS(app)

    # -----------------------------
    # Register routes
    # -----------------------------

    from app.routes.auth import auth_bp
    from app.routes.scan import scan_bp
    from app.routes.inspection import inspection_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        scan_bp
    )

    app.register_blueprint(
        inspection_bp
    )

    app.register_blueprint(
        reports_bp
    )

    # -----------------------------
    # Health check
    # -----------------------------

    @app.route("/health", methods=["GET"])
    def health():

        return jsonify({
            "status": "ok",
            "message": "Backend is running"
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )