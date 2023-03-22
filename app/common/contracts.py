import json
from os import path


basepath = path.dirname(__file__)
build_contracts_path = "contracts/artifacts/contracts"
w3 = None

def set_web3(web3):
    global w3
    w3=web3

####### institution #######

def load_institution_interface_file():
    filepath = path.abspath(path.join(basepath, "..", "..", build_contracts_path+"/Institution.sol/Institution.json"))
    f = open(filepath)        
    data = json.load(f)
    f.close()    
    return data

def institution_contract(**kwargs):
    address = kwargs.get('address', None)
    contract_interface = load_institution_interface_file()    
    contract = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bytecode'],address=address)
    return contract


def get_new_institution_txn():
    contract = institution_contract()
    construct_txn = contract.constructor(True) #true -> create new storage       
    return construct_txn

def get_func_publish_award_txn(signature,student_address,award_title,award_date,contract_address):
    contract = institution_contract(address=contract_address)
    construct_txn = contract.functions.addAwardSignedByStudent(signature,student_address,award_title,award_date)
    return construct_txn

def get_nonce_award_student(contract_address,student_address):
    contract = institution_contract(address=contract_address)
    return contract.functions.getNonceAwardSign(student_address).call()

def get_storage_address(contract_address):
    contract = institution_contract(address=contract_address)
    return contract.functions.getStorageAwards().call()
 
####### storage #######

def load_storage_interface_file():
    filepath = path.abspath(path.join(basepath, "..", "..", build_contracts_path+"/StorageAwards.sol/StorageAwards.json"))
    f = open(filepath)        
    data = json.load(f)
    f.close()    
    return data

def storage_contract(**kwargs):
    address = kwargs.get('address', None)
    contract_interface = load_storage_interface_file()    
    contract = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bytecode'],address=address)
    return contract

def get_student_awards(contract_address,student_address):
    contract = storage_contract(address=contract_address)
    return contract.functions.getStudentAwards(student_address).call()

def get_all_students(contract_address):
    contract = storage_contract(address=contract_address)
    return contract.functions.getAllStudents().call()
    