from tkinter import *
from tkinter import ttk
from Cryptography.hybrid_encryption import *
from getpass import getuser
from tkinter.filedialog import askopenfilename
from ttkthemes import themed_tk as tk
import os
import requests
import json
from web3 import Web3
from solcx import compile_standard, install_solc
import pickle
import pandas as pd

import matplotlib
matplotlib.use('Agg')

ganache_url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))

# check the latest block number
print(web3.eth.blockNumber)

project_id = "2HCgCTXMPiHEQdclDGeIe7S7vp0"
project_secret = "4d3e66dfadd210f20535107cdeab7fa8"
endpoint = "https://ipfs.infura.io:5001"

install_solc("0.8.9")

w3 = Web3(
    Web3.HTTPProvider("http://127.0.0.1:7545")
)
chain_id = 1337

my_address = "0x786cbFf099CcAd1401Ab8aE582272CdfCc6d0f85"
private_key = "e6fd8ffe050909b736d3c52e10d167965055eee56f791801d584d6f5454277f7"
nonce = w3.eth.getTransactionCount(my_address)
# store file on ipfs
def store_file_ipfs(FILE_NAME):
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
        print(r)
        CID = r['Hash']
        # return hash function
    return CID


# retreive file from ipfs
def get_file_ipfs(CID):
    params = {
     'arg': CID
    }
    response = requests.post(
        endpoint + '/api/v0/cat',
        params=params,
        auth=(project_id, project_secret),
    )
   
    # write downloaded file from ipfs
    with open(CID + '.csv.enc', 'wb') as f:
        f.write(response.content)
    # df = pd.read_csv(CID)    
    # return df


# deploy smart contract to blockchain
def deploy_contract(name, params, nonce):
    with open(f'x{name}.sol', 'w', encoding='utf-16', errors='ignore') as outFIle:
        with open(f'{name}.sol', 'r', encoding='utf-16', errors='ignore') as infile:
            lines = infile.read().replace("// SPDX-License-Identifier: MIT", "")
            outFIle.write(lines)
    os.replace(f'x{name}.sol', f'{name}.sol')

    with open(f"{name}.sol", "r", encoding='utf-16', errors='ignore') as file:
        file_storage_file = file.read()

    # Solidity source code
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {f"{name}.sol": {"content": file_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [
                            "abi",
                            "metadata",
                            "evm.bytecode",
                            "evm.bytecode.sourceMap",
                        ]
                    }
                }
            },
        },
        solc_version="0.8.9",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"][f"{name}.sol"][f"{name}"]["evm"][
        "bytecode"
    ]["object"]

    # get abi
    abi = json.loads(
        compiled_sol["contracts"][f"{name}.sol"][f"{name}"]["metadata"]
    )["output"]["abi"]
    print(f"abi: {abi}")

    instance_sc = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Submit the transaction that deploys the contract
    transaction = instance_sc.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish (mined)...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
    print(type(params))
    instance = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    call_transaction(instance, "initialize", params, nonce)
    return tx_receipt.contractAddress, tx_hash, abi, nonce + 1


def upload_hash(simple_storage, file_hash, _nonce):
    print(f"nonce deploy:{_nonce}")
    add_hash_transaciton = simple_storage.functions.set(file_hash).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": _nonce + 1,
        }
    )

    signed_greeting_txn = w3.eth.account.sign_transaction(
        add_hash_transaciton, private_key=private_key
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print("Hash uploaded to smart contract")


def get_hash(simple_storage):
    stored_hash = simple_storage.functions.get().call()
    print(f"Stored hash value retrieved from smart contract: {stored_hash}")
    return stored_hash

def message(name, button, mgs_label):
    """This function displayed the massage, return by either Encryption or Decryption"""
    
    
    button['state'] = DISABLED  # make button state disable
    if button["text"] == "Encryption":
        mgs = encryption(name)
        mgs_label.config(text=mgs)

    if button["text"] == "Decryption":
        mgs = decryption(name)
        mgs_label.config(text=mgs)

    if button["text"] == "Upload":       
        file_hash = store_file_ipfs(name)
        # file_hash = "QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr"
        # nonce = w3.eth.getTransactionCount(my_address)
        global nonce
        print(f"nonce:{nonce}")
        mgs = upload_hash(simple_storage, file_hash, nonce)
        print(f"Uploaded to IPFS with hash:{file_hash}")
        nonce = nonce + 1
        mgs_label.config(text=mgs)

    if button["text"] == "Download":
        downloaded_hash = get_hash(simple_storage)
        print(f"Download hash:{downloaded_hash}")
        mgs = get_file_ipfs(downloaded_hash)
        mgs_label.config(text=mgs)


def open_file():
    """
    This function open the file dialog box for choosing the file.
    And then making two buttons : encrypt_button, decrypt_button
    """
    
    username = getuser()
    initialdirectory = "C:/Users/{}".format(username)
    name = askopenfilename(initialdir=initialdirectory,
                           filetypes=[("All Files", "*.*")],
                           title="Choose a file."
                           )
    if name:
        file_name = get_file_name(name, extension=True)
        label.config(text=file_name)
        separator2 = ttk.Separator(root, orient='horizontal')
        separator2.place(relx=0, rely=0.38, relwidth=1, relheight=1)
        mgs_label = ttk.Label(root)
        mgs_label.place(x=0, y=150)
        encrypt_button = ttk.Button(root, text="Encryption", command=lambda: message( name, encrypt_button, mgs_label))
        decrypt_button = ttk.Button(root, text="Decryption", command=lambda: message( name, decrypt_button, mgs_label))
        upload_button = ttk.Button(root, text="Upload", command=lambda: message( name, upload_button, mgs_label))
        download_button = ttk.Button(root, text="Download", command=lambda: message( name, download_button, mgs_label))
        encrypt_button.place(x=110, y=80)
        decrypt_button.place(x=210, y=80)
        upload_button.place(x=110, y=120)
        download_button.place(x=210, y=120)

def call_transaction(instance, functionName, params, nonce):
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
        print("Initialize Contract!")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! Initialize contract")
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
        print("Initialize Contract!")
        # Send it!
        tx_hash_ = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish (mined)...")
        w3.eth.wait_for_transaction_receipt(tx_hash_)
        print("Done! Initialize contract")

root = tk.ThemedTk()
root.get_themes()
root.set_theme("clearlooks")

contract_addr, tx_hash, abi_fs, nonce_fs = deploy_contract("FileStorage", my_address, nonce)
nonce += 2
simple_storage = w3.eth.contract(address=contract_addr, abi=abi_fs)
contract_addr_ac, tx_hash_ac, abi_ac, nonce_ac = deploy_contract("AccessControl", None, nonce)
nonce += 1
file_storage_ac = w3.eth.contract(address=contract_addr_ac, abi=abi_ac)
call_transaction(file_storage_ac, "setFileStorage", contract_addr, nonce)
nonce += 1
# icon = PhotoImage(file="images/icon.png")  
# # icon for the window
# icon_sl = root.iconphoto(False, icon)
# icon_sl.pack()
app_width = 400  # window width
app_height = 200  # window height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Evaluating X and Y coordinate such that, window always comes into the center.
x = int((screen_width / 2) - (app_width / 2))
y = int((screen_height / 2) - (app_height / 2))
root.geometry(f"{app_width}x{app_height}+{x}+{y}")
root.resizable(0, 0)  # Window size constant
title = root.title("File Storage")
title_label = ttk.Label(root, text="Welcome to File Storage Application", font=("Helvetica ", 16))
title_label.pack()
separator1 = ttk.Separator(root, orient='horizontal')
separator1.place(relx=0, rely=0.20, relwidth=1, relheight=1)
chose_file_button = ttk.Button(root, text="Chose File", command=open_file).pack()
label = ttk.Label(root, text="No chosen file")  # Label to display the name of selected file.
label.pack()

root.mainloop()
