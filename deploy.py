from solcx import compile_standard, install_solc
import json
from web3 import Web3
_solc_version = "0.6.0"
install_solc(_solc_version)
with open("./SimpleStorage.sol", "r") as file:
    simple_stprage_file = file.read()

    # Compile our solidity
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_stprage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=_solc_version,
    )
    print(compiled_sol)

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file) 
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]['abi']

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0x66A19bEc114A282ca7805B840046a1b326101Cb9"
    private_key = "0x9a8e001e8b5fd4ff7f61537540e934ae8fa7f313df23e5afa0f2f1117c46fbcd"

    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.getTransactionCount(my_address)
    print(nonce)    
    
    transaction = SimpleStorage.constructor().buildTransaction(
        {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
    simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)
    print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
    greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce + 1})

    signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(simple_storage.functions.retrieve().call())