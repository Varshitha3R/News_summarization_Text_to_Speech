from flask import Flask, request, jsonify
from utils import scrape_and_analyze

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    company_name = data.get("company", "").strip()

    if not company_name:
        return jsonify({"error": "No company name provided"}), 400

    result = scrape_and_analyze(company_name)

    if "error" in result:
        return jsonify(result), 404

    # Debugging: Print JSON response to console
    print(result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
