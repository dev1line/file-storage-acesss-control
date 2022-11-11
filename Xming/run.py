import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc


project_id = "2HCgCTXMPiHEQdclDGeIe7S7vp0"
project_secret = "4d3e66dfadd210f20535107cdeab7fa8"
endpoint = "https://ipfs.infura.io:5001"

install_solc("0.8.9")

w3 = Web3(
    Web3.HTTPProvider("http://127.0.0.1:7545")
)
chain_id = 1337

my_address = "0x24c620Ac3DCc320C889e2EAd3817a24E6282CaF6"
private_key = "5a574cb5135b242bd3ccd9da5fe3ace820c0aa1f37dc8b8ca6a7bb264d3917d1"
nonce = w3.eth.getTransactionCount(my_address)

def call_transaction(name, instance_address, functionName, params, nonce):
    with open(f"{name}_abi.txt", "r") as file:
        abi = file.read()
    instance = w3.eth.contract(address=instance_address, abi=abi)
    if params is None: 
        tx = instance.functions[f"{functionName}"]().buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce + 1,
            }
        )
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
        print("sign message...")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! ")
    elif params is tuple:
        tx = instance.functions[f"{functionName}"](params).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce + 1,
            }
        )
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
        print("sign message...")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! ")
    else:
        tx = instance.functions[f"{functionName}"](params).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce + 1,
            }
        )
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
        print("sign message...")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! ")

elems = ["0x48416B1fb7653019BAF244044134C1821d0519C0", "0xc1DcFCB34d21259088924565A6342513Ba987948", "0x29365F5865cEDcee38DcF4CB6A97F806bFd195f1"]

params = ("fileType", "fileName", "fileLink", elems, bytes(f"{my_address}", 'utf-8'))

# call_transaction("AccessControl", "0x32175A78bc40301da1c2373Cf66E6c75E0C2d4Ba", "createFile", params, nonce)
instance_address = "0xb7eB562B39391010ca892ebCE1D9Bb29232ACe81"

with open("AccessControl_abi.txt", "r") as file:
    abi = file.read()
instance = w3.eth.contract(address=instance_address, abi=abi)

# tx = instance.functions.createFile("fileType", "fileName", "fileLink", mtree.getRootHash(), mtree.getRootHash()).buildTransaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce,
#     }
# )
# # Sign the transaction
# signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
# print("sign message...")
# # Send it!
# tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# # Wait for the transaction to be mined, and get the transaction receipt
# print("Waiting for transaction to finish (mined)...")
# w3.eth.wait_for_transaction_receipt(tx_hash_)
# print("Done! ")
tx = instance.functions.updateFile(1, ["fileType", "fileName", "fileLink", mtree.getRootHash(), mtree.getRootHash(), my_address]).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
print("sign message...")
# Send it!
tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish (mined)...")
w3.eth.wait_for_transaction_receipt(tx_hash_)
print("Done! ")

data = instance.functions.getRootHash(1).call()

data_2 = instance.functions.getFile(1).call()

print(data)