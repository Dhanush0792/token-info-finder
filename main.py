from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Existing form-based route
@app.route('/', methods=['GET', 'POST'])
def index():
    token_info = None
    if request.method == 'POST':
        contract_address = request.form.get('contract_address')
        if contract_address:
            etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')  # safer key name
            etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={etherscan_api_key}"
            response = requests.get(etherscan_url)
            token_info = response.json()
    return render_template('index.html', token_info=token_info)

# NEW: API route for JSON POST requests
@app.route('/fetch', methods=['POST'])
def fetch_token_info():
    data = request.get_json()
    contract_address = data.get('contract_address')

    if not contract_address:
        return jsonify({'error': 'Contract address missing'}), 400

    etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')
    etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={etherscan_api_key}"
    response = requests.get(etherscan_url)
    token_info = response.json()

    return jsonify(token_info)

if __name__ == '__main__':
    app.run(debug=True)
