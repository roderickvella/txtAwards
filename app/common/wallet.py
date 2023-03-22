from base64 import encode,b64encode
from eth_account import Account
from eth_account.messages import encode_defunct
import secrets
import eth_keyfile
import common.environment
import common.contracts
from codecs import encode, decode
from web3 import Web3
from decimal import Decimal
import requests
from enum import Enum



local_account = None 

#connect to provider
w3 = Web3(Web3.HTTPProvider(common.environment.WEB3_HTTPProvider))

#Check Connection
is_connected_node=w3.isConnected()
print("Connected to HTTPProvider:",is_connected_node)

#set w3 in contracts
common.contracts.set_web3(w3)   

def create_wallet(password):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv   
    acct = Account.from_key(private_key)    
    encoded_private_key = decode(priv.encode(), "hex")
    json_output = eth_keyfile.create_keyfile_json(encoded_private_key,password.encode())

    #print ("SAVE BUT DO NOT SHARE THIS:", private_key)
    print("Address:", acct.address)
    return json_output

def unlock_wallet(json_keyfile,password):
    global local_account

    private_key = w3.eth.account.decrypt(json_keyfile, password)
    local_account=w3.eth.account.from_key(private_key)

    print("public address:",local_account.address)
    print("private key:",local_account.key)
    return True

def wallet_unlocked():
    return local_account is not None

def get_decoded_privatekey():    
    encoded = encode(local_account.key, "hex")
    decoded_private_key = encoded.decode()
    return "0x"+decoded_private_key

def get_address():
    return local_account.address

def get_checksum_address(address):
    return w3.toChecksumAddress(address)

def get_balance_address():
    if(local_account is not None):
        balance_wei = w3.eth.get_balance(local_account.address)
        return Decimal(w3.fromWei(balance_wei, 'ether'))
    return None


def get_chain_id():
    return w3.eth.chain_id

def get_gas_fees():
    return requests.get(common.environment.POLYGON_GAS_STATION).json()

def get_selected_gas_fee(gas_fees,gas_fee_priority):
    if(gas_fee_priority=="safe low"):
        print("safe low selected")
        max_fee_gas = gas_fees["safeLow"]["maxFee"]
        max_priority_fee_gas = gas_fees["safeLow"]["maxPriorityFee"]
    elif(gas_fee_priority=="standard"):
        print("standard selected")
        max_fee_gas = gas_fees["standard"]["maxFee"]
        max_priority_fee_gas = gas_fees["standard"]["maxPriorityFee"]
    elif(gas_fee_priority=="fast"):
        print("fast selected")
        max_fee_gas = gas_fees["fast"]["maxFee"]
        max_priority_fee_gas = gas_fees["fast"]["maxPriorityFee"]
    return {"max_fee_gas":max_fee_gas,"max_priority_fee_gas":max_priority_fee_gas,"estimatedBaseFee":gas_fees["estimatedBaseFee"]}

def build_transaction(gas_fee_priority,transaction_type,**kwargs):

    def create_txn(selected_gas,txn_type):
        if(txn_type==TransactionType.Deploy_Institution_Contract):
            txn = common.contracts.get_new_institution_txn()
        elif(txn_type==TransactionType.Publish_Award):
            data = kwargs.get('data', None)            
            txn = common.contracts.get_func_publish_award_txn(data["signed_data"],data["student_address"],data["award_title"],data["award_date"],data["institution_contract"])
                      
        #https://ethereum.stackexchange.com/questions/108049/how-does-estimation-of-gas-price-changes-after-implementation-of-eip-1559
        max_priority_fee = w3.toWei(selected_gas["max_priority_fee_gas"], 'gwei')
        max_fee = w3.toWei(selected_gas["max_fee_gas"], 'gwei')
        base_fee = w3.toWei(selected_gas["estimatedBaseFee"], 'gwei')

        #--make sure you have enough money to process transaction - this check is not yet implemented
        construct_txn = txn.buildTransaction({
            'from': local_account.address,
            'chainId':get_chain_id(),
            'nonce': w3.eth.getTransactionCount(local_account.address),            
            'maxPriorityFeePerGas':max_priority_fee,
            'maxFeePerGas':max_fee})
        
        gas = w3.eth.estimate_gas(construct_txn)
        construct_txn.update({'gas': gas})
       
        #the overall fee a transaction creator pays is calculated as: ( (base fee + priority fee) x units of gas used). 
        estimated_total_gas_fee = (base_fee + max_priority_fee)*gas
        estimated_total_gas_fee_eth = w3.fromWei(estimated_total_gas_fee,'ether')
        #print("Matic",estimated_total_gas_fee_eth)        
        return {"unsigned_txn":construct_txn,"total_gas_fee":estimated_total_gas_fee_eth}

    
    gas_fees = get_gas_fees()  
    selected_gas = get_selected_gas_fee(gas_fees,gas_fee_priority)

    tx_info = create_txn(selected_gas,transaction_type)
    return tx_info


def sign_sendtransaction(unsigned_txn):
    signed = local_account.signTransaction(unsigned_txn) 
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    return {"txn_hash":txn_hash,"hex_txn_hash":Web3.toHex(txn_hash)}

def get_transaction_receipt(txn_hash):
    tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)    
    #print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return tx_receipt

def sign_award(award):
    messageHash =  Web3.solidityKeccak(["string","uint256","uint256","uint256","address"], [award["award_title"],award["award_date"],award["nonce_award_student"],award["chain_id"],award["institution_contract"]])
    message = encode_defunct(hexstr=Web3.toHex(messageHash))
    signed_message = w3.eth.account.sign_message(message, private_key=local_account.key)
    return signed_message.signature

def get_transaction_title(transaction_type):
    if(transaction_type == common.wallet.TransactionType.Deploy_Institution_Contract):
        return "Create Contract"
    elif(transaction_type == common.wallet.TransactionType.Publish_Award):
        return "Publish Award"

def sign_message(msg):
    message = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(message, private_key=local_account.key)     
    return signed_message.signature.hex()

def verify_signed_message(message,address,signature_hex):
    message = encode_defunct(text=message)
    try:
        signature_bytes = bytes.fromhex(signature_hex[2:])
    except ValueError:
        return False
    recovered_address = w3.eth.account.recover_message(message, signature=signature_bytes)  
    # return true if valid
    return recovered_address == address

class TransactionType(Enum):
    Deploy_Institution_Contract = 1
    Publish_Award =2

#https://docs.polygon.technology/docs/develop/tools/polygon-gas-station/
#https://cryptomarketpool.com/get-gas-prices-from-the-eth-gas-station-and-web3-py-in-python/
#https://stackoverflow.com/questions/66007565/how-to-get-gas-amount-web3py
    


       

    

    




