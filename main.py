from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    token_info = None
    if request.method == 'POST':
        contract_address = request.form.get('contract_address')
        if contract_address:
            etherscan_api_key = os.environ.get('3Z1M8G2HXSBPXBCSA5FSZ1A6AMN43IERPB')
            etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={etherscan_api_key}"
            response = requests.get(etherscan_url)
            token_info = response.json()
    return render_template('index.html', token_info=token_info)

if __name__ == '__main__':
    app.run(debug=True)
