from flask import Flask
from routes.search_route import search_bp
from routes.monitoring_route import monitoring_bp
from routes.decode_route import decode_bp
#from scheduler_job import start_scheduler
from config import API_PORT

app = Flask(__name__)

# register routes
app.register_blueprint(search_bp)
app.register_blueprint(monitoring_bp)
app.register_blueprint(decode_bp)

#start_scheduler()

@app.route("/")
def home():
    return "Twitter Search API Modular"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=API_PORT, debug=True, threaded=True)
