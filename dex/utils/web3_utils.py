from web3 import Web3
import json

from GraduationProject.settings import  web3, erc1155


def print_contract_address():
    print(erc1155.address)


def create_mint(data):
    data['is_nf'] = data['is_nf'].lower() == 'true'
    usr_addr = data['usr_addr']
    quantity = data['quantity']

    try:
        tx_hash = erc1155.functions.create(json.dumps(data), data['is_nf']).transact()
        log_to_process = web3.eth.waitForTransactionReceipt(tx_hash)['logs'][1]
        processed_log = erc1155.events.URI().processLog(log_to_process)

        if data['is_nf']:
            tx_hash = erc1155.functions.mintNonFungible(processed_log.args._id, [Web3.toChecksumAddress(usr_addr)]).transact()
        else:
            tx_hash = erc1155.functions.mintFungible(processed_log.args._id, [Web3.toChecksumAddress(usr_addr)], [quantity]).transact()

        log_to_process = web3.eth.waitForTransactionReceipt(tx_hash)['logs'][0]
        processed_log = erc1155.events.TransferSingle().processLog(log_to_process)
        print(processed_log.args._id)
        return processed_log.args._id
    except Exception as e:
        print(e)
        return None


def balanceOf(usr_addr, id):
    try:
        balance = erc1155.functions.balanceOf(usr_addr, id).call()
        return balance
    except Exception as e:
        print(e)
        return None


def getTokenIdsByAddr(usr_addr):
    try:
        ids = erc1155.functions.ownedBy(Web3.toChecksumAddress(usr_addr)).call()
        return ids
    except Exception as e:
        print(e)
        return None


def balanceOfBatchSingleAddr(usr_addr, ids):
    try:
        ids = erc1155.functions.balanceOfBatchSingleOwner(Web3.toChecksumAddress(usr_addr), ids).call()
        return ids
    except Exception as e:
        print(e)
        return None


def sendETHtoUser(usr_addr, val):
    try:
        return erc1155.functions.sendETHtoUser(Web3.toChecksumAddress(usr_addr), web3.toWei(val, 'ether')).transact()
    except Exception as e:
        print(e)
        return None


def safeTransferFrom(from_usr_addr, to_usr_addr, token_id, quantity, data="0x01"):
    print()
    try:
        if token_id == "1":
            quantity = Web3.toWei(quantity, "ether")
        return erc1155.functions.safeTransferFrom(Web3.toChecksumAddress(from_usr_addr), Web3.toChecksumAddress(to_usr_addr), int(token_id), int(quantity), data).transact()
    except Exception as e:
        print(e)
        return None