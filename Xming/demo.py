import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc

ganache_url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))

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
# check the latest block number
print(web3.eth.blockNumber, nonce)

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

    with open(f"{name}_abi.txt", "w") as file:
        # file.write(string(abi))
        json.dump(abi, file)
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
    call_transaction(instance, "initialize", params, nonce, False)
    return tx_receipt.contractAddress, tx_hash, abi, nonce + 1

def call_transaction(instance, functionName, params, nonce, call):
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
    elif call:
        data = instance.functions[f"{functionName}"]().call()

        print("Call:", data)
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
contract_addr_ac, tx_hash_ac, abi_ac, nonce_ac = deploy_contract("AccessControl", None, nonce)
nonce += 2
file_storage_ac = w3.eth.contract(address=contract_addr_ac, abi=abi_ac)

contract_addr, tx_hash, abi_fs, nonce_fs = deploy_contract("FileStorage", contract_addr_ac, nonce)
nonce += 1
simple_storage = w3.eth.contract(address=contract_addr, abi=abi_fs)
call_transaction(file_storage_ac, "setFileStorage", contract_addr, nonce, False)
nonce += 1
call_transaction(simple_storage, "owner", contract_addr, nonce, True)
nonce += 1