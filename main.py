from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Index route working!"

@app.route('/fetch', methods=['POST'])
def fetch_token_info():
    print("Received POST request on /fetch")
    data = request.get_json()
    contract_address = data.get('contract_address')
    print(f"Contract Address: {contract_address}")

    if not contract_address:
        return jsonify({'error': 'Contract address missing'}), 400

    # **HARD CODED API KEY FOR LOCAL TEST**
    etherscan_api_key = '3Z1M8G2HXSBPXBCSA5FSZ1A6AMN43IERPB'
    
    etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={etherscan_api_key}"
    print(f"Calling Etherscan API: {etherscan_url}")
    
    response = requests.get(etherscan_url)
    token_info = response.json()

    return jsonify(token_info)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
