from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Token Info Finder API is live!"

@app.route('/fetch', methods=['POST'])
def fetch_token_info():
    data = request.get_json()
    contract_address = data.get('contract_address')
    
    if not contract_address:
        return jsonify({'error': 'Contract address missing'}), 400

    # Get API Key from environment variable
    etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')
    
    if not etherscan_api_key:
        return jsonify({'error': 'API key not set'}), 500
    
    etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={etherscan_api_key}"
    
    response = requests.get(etherscan_url)
    token_info = response.json()

    return jsonify(token_info)

if __name__ == '__main__':
    app.run(debug=True)