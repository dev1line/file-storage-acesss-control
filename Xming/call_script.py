import os
import requests
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()
default_path = "/mnt/d/Freelance/Upwork/file-storage-contracts/Xming/Storage/"
project_id = "2HCgCTXMPiHEQdclDGeIe7S7vp0"
project_secret = "4d3e66dfadd210f20535107cdeab7fa8"
endpoint = "https://ipfs.infura.io:5001"

install_solc("0.8.9")

w3 = Web3(
    Web3.HTTPProvider("http://127.0.0.1:7545")
)
chain_id = 1337
w3.eth.defaultAccount = os.getenv('ACCOUNT')
my_address = os.getenv('ACCOUNT')
private_key = os.getenv('PRIVATE_KEY')
# store file on ipfs
def store_file_ipfs(FILE_NAME):
    print("receiver", FILE_NAME)
    with open(FILE_NAME, 'rb') as file_content:
        files = {
            FILE_NAME: file_content
        }

        ### ADD FILE TO IPFS AND SAVE THE HASH ###
        response = requests.post(
            endpoint + '/api/v0/add',
            files=files,
            auth=(project_id, project_secret),
        )
        r = response.json()
        print("r", r)
        CID = r['Hash']
        # return hash function
    return CID


# retreive file from ipfs
def get_file_ipfs(CID, file_type):
    params = {
     'arg': CID
    }
    response = requests.post(
        endpoint + '/api/v0/cat',
        params=params,
        auth=(project_id, project_secret),
    )
    
    # write downloaded file from ipfs
    with open(default_path + CID + f'{file_type}'+ ".enc", 'wb') as f:
        f.write(response.content)
    # df = pd.read_csv(CID)    
    return f.name

def call_transaction(name, functionName, params):
    print("caller: ", my_address)
    nonce = w3.eth.getTransactionCount(my_address)
    print("nonce", nonce)
    with open(f"contract.json", "r") as read_file:
        dumper = read_file.read()

    instance_address = json.loads(dumper)[f"{name}"]
    print("instance_address", instance_address)
    with open(f"{name}_abi.txt", "r") as file:
        abi = file.read()
    instance = w3.eth.contract(address=instance_address, abi=abi)
    tx = ""
    data = None
    if params is None: 
        tx = instance.functions[f"{functionName}"]().buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "verify":
        data = instance.functions[f"{functionName}"](params[0], params[1]).call()
    elif functionName == "getCurrentId":
        data = instance.functions[f"{functionName}"]().call()
    elif functionName == "getMyFiles":
        data = instance.functions[f"{functionName}"]().call()  
    elif functionName == "getAuthorizedUsersOf":
        data = instance.functions[f"{functionName}"](params[0]).call()  
    elif functionName == "getFile":
        data = instance.functions[f"{functionName}"](params[0]).call()  
    elif functionName == "createFile" :
        tx = instance.functions[f"{functionName}"](params[0], params[1], params[2], params[3], params[4]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "updateFile":
        print(params[0])
        print(params[1])
        tx = instance.functions[f"{functionName}"](params[0], params[1]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "deleteFile":
        tx = instance.functions[f"{functionName}"](params[0]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "deleteFile":
        tx = instance.functions[f"{functionName}"](params[0]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "addAuthorizedUser":
        tx = instance.functions[f"{functionName}"](params[0], params[1]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "removeAuthorizedUser":
        tx = instance.functions[f"{functionName}"](params[0], params[1]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    elif functionName == "setFileStorage":
        tx = instance.functions[f"{functionName}"](params[0]).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
    
    if tx:
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
        print("sign message...")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! ")
    return tx, data

# whitelist = ["0x48416B1fb7653019BAF244044134C1821d0519C0", "0xc1DcFCB34d21259088924565A6342513Ba987948", "0x29365F5865cEDcee38DcF4CB6A97F806bFd195f1"]

# params = ["fileType", "fileName", "fileLink", whitelist, bytes(f"private_metadata", 'utf-8')]

# tx, data = call_transaction("AccessControl", "createFile", params)
# print(tx, data)

# params = [1]
# tx, data = call_transaction("AccessControl", "getFile", params)
# print(tx, data)



# with open(f"contract.json", "r") as read_file:
#     dumper = read_file.read()

# instance_address = json.loads(dumper)["accessControl"]

# with open("AccessControl_abi.txt", "r") as file:
#     abi = file.read()
# instance = w3.eth.contract(address=instance_address, abi=abi)

# tx = instance.functions.createFile("fileType", "fileName", "fileLink", whitelist, bytes(f"private_metadata", 'utf-8')).buildTransaction(
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
# data_1 = instance.functions.getFile(1).call()

# print(data_1)
# nonce += 1
# tx = instance.functions.updateFile(1, ["fileType", "fileName", "fileLink", bytes(f"updated_private_metadata", 'utf-8'), my_address]).buildTransaction(
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

# # data = instance.functions.getRootHash(1).call()

# data_2 = instance.functions.getFile(1).call()
# tx, data = call_transaction("AccessControl", "getMyFiles", [])
# print(tx, data)