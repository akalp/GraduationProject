from web3 import Web3, HTTPProvider
import json
import os

from GraduationProject.settings import BASE_DIR, web3, erc1155


def print_contract_address():
    print(erc1155.address)


def create_mint(data):
    is_nf = data['is_nf'].lower() == 'true'
    usr_addr = data['usr_addr']
    quantity = data['quantity']

    try:
        tx_hash = erc1155.functions.create(json.dumps(data), is_nf).transact()
        log_to_process = web3.eth.waitForTransactionReceipt(tx_hash)['logs'][1]
        processed_log = erc1155.events.URI().processLog(log_to_process)

        if is_nf:
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
        ids = erc1155.functions.balanceOfBatchSingleOwner(usr_addr, ids).call()
        return ids
    except Exception as e:
        print(e)
        return None