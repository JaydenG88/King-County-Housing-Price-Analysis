from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from housing_data_API.routes.routes import housing_bp
from werkzeug.middleware.proxy_fix import ProxyFix

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "100 per hour"]
)

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
limiter.init_app(app)
app.register_blueprint(housing_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run()
    