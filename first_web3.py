from flask import Flask, make_response, request
from web3 import Web3
import json

app = Flask(__name__)

ganache_url = 'http://localhost:7545'
w3 = Web3(Web3.HTTPProvider(ganache_url))
with open('build/contracts/TestCoin.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    abi = config["abi"]
address = "0x251B1C5f3Ce171e1C48D4D76196498772b82190f"
contract = w3.eth.contract(address=address, abi=abi)
accounts = w3.eth.accounts
admin = accounts[0]
receiver = accounts[1]


def wei_to_ether(wei):
    return w3.fromWei(wei, 'ether')


@app.route('/', methods=['GET'])
def index_accounts():
    accounts = w3.eth.accounts
    return_accounts = []
    for acc in accounts:
        return_accounts.append({
            'address': acc,
            'balance': contract.functions.balanceOf(acc).call()
        })
    content = {
        'Token name': contract.functions.name().call(),
        'Symbol': contract.functions.symbol().call(),
        'Contract Address': contract.address,
        'accounts': return_accounts
    }
    return make_response(content)


@app.route('/transfer', methods=['GET'])
def transfer():
    from_index = int(request.args.get('from', 0))
    to_index = int(request.args.get('to', 1))
    amount = int(request.args.get('amount', 10))
    try:
        from_address = accounts[from_index]
        to_address = accounts[to_index]
        tx_hash = contract.functions.transfer(to_address, amount).transact({'from': from_address})
        w3.eth.waitForTransactionReceipt(tx_hash)
        return 'Transfered {} from account[{}] to accounts[{}]'.format(amount, from_index, to_index)
    except Exception as e:
        app.logger.warning(e)
        return "Transfer Frailed"


if __name__ == "__main__":
    app.run()
