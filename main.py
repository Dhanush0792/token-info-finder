from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ETHERSCAN_API_KEY = "3Z1M8G2HXSBPXBCSA5FSZ1A6AMN43IERPB"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/fetch", response_class=HTMLResponse)
async def fetch_token_info(request: Request, address: str = Form(...)):
    etherscan_url = f"https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={address}&apikey={ETHERSCAN_API_KEY}"
    etherscan_res = requests.get(etherscan_url).json()

    coingecko_url = f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{address}"
    coingecko_res = requests.get(coingecko_url)

    result = {}
    
    if etherscan_res['status'] == '1':
        result['etherscan'] = etherscan_res['result']
    else:
        result['etherscan'] = {"error": "Token info not found on Etherscan"}

    if coingecko_res.status_code == 200:
        result['coingecko'] = coingecko_res.json()
    else:
        result['coingecko'] = {"error": "Token not found on CoinGecko"}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})
