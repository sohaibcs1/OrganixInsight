from flask import Flask, send_from_directory
import os
from flask_cors import CORS
# pip install flask-cors
app = Flask(__name__)

CORS(app)

@app.route('/images/<exp_dir>/<filename>')
def serve_image(exp_dir, filename):
    return send_from_directory(os.path.join('images', exp_dir), filename)

# @app.route('/results_cc/<filename>')
# def serve_cc_image(filename):
#     base = os.path.join(os.getcwd(), 'results_cc')
#     return send_from_directory(base, filename)

# Define your Flask routes, event handlers, and app configuration as needed.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6085)
