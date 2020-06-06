from urllib import request


from GraduationProject.db_connector import connect
import threading
from GraduationProject.settings import web3, erc1155
import json

conn = connect()
cur = conn.cursor()


def run():
    threading.Timer(10.0, run).start()
    print("thread start")
    contract_tokens = dict()
    for event in uri.get_all_entries():
        value = json.loads(event.args._value)
        if type(value['is_nf']) == str:
            continue
        id = event.args._id if not bool(value["is_nf"]) else event.args._id+1
        contract_tokens.update({(id,): value})

    cur.execute("SELECT contract_id FROM dex_token;")
    tokens = cur.fetchall()

    for id, value in contract_tokens.items():
        if (str(id[0]),) not in tokens:
            print(id[0])
            img = "token/default_token.jpg"
            if "img" in value.keys():
                img = "../media/token/{}.{}".format(id[0], value["img"].split(".")[-1])
                request.urlretrieve(value["img"], img)
            try:
                print("insert id:", id[0])
                name = value["name"]
                if "data" in value:
                    name += " "+value["data"]
                cur.execute("INSERT INTO dex_token (name, img, game_id, is_nf, contract_id) VALUES ('{}','{}','{}','{}','{}');".format(value["name"], img, value["game"], bool(value["is_nf"]), str(id[0])))
                conn.commit()
            except:
                print("hatalı veri id: ", id[0])
                continue
    print("thread end")


uri = erc1155.events.URI.createFilter(fromBlock=web3.eth.blockNumber-10, toBlock='latest')
run()