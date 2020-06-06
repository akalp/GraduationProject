from GraduationProject.db_connector import connect
import threading
from dex.utils import web3_utils

conn = connect()
cur = conn.cursor()

# cur.execute("create view sell as select * from dex_sellorder s, (select o.id,usr_addr,value,timestamp,obj_id,quantity,contract_id from dex_order o, dex_token t where t.id=o.obj_id) k where s.order_ptr_id=k.id order by timestamp desc;")
# cur.execute("create view buy as select * from dex_buyorder b, (select o.id,usr_addr,value,timestamp,obj_id,quantity,contract_id from dex_order o, dex_token t where t.id=o.obj_id) k where b.order_ptr_id=k.id order by timestamp desc;")

def match():
    threading.Timer(10.0, match).start()
    matched_orders = []
    print("-----------------------------------------------------\nsell view")
    cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'sell';")
    row1 = cur.fetchall()
    print(row1)
    cur.execute("SELECT * FROM sell;")
    row = cur.fetchall()
    for row in row:
        print(row)

    print("\nbuy view")
    cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'buy';")
    row1 = cur.fetchall()
    print(row1)
    cur.execute("SELECT * FROM buy;")
    row = cur.fetchall()
    for row in row:
        print(row)

    print("\nmatches")
    cur.execute("select buy.usr_addr as buyer,buy.value as buy_val,buy.quantity as buy_q,sell.usr_addr as seller,sell.value as sell_val,sell.quantity as sell_q,buy.contract_id, buy.order_ptr_id as buy_id, sell.order_ptr_id as sell_id from sell, buy where sell.contract_id=buy.contract_id and (cast(sell.value as integer)/sell.quantity)<=(cast(buy.value as integer)/buy.quantity);")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if len(row) != 0 and row[7] not in matched_orders or row[8] not in matched_orders:
            if row[5]-row[2] > 0:
                web3_utils.safeTransferFrom(row[3], row[0], row[6], row[2])
                web3_utils.safeTransferFrom(row[0], row[3], "1", row[1])
                matched_orders.append(row[7])
                cur.execute("UPDATE dex_order SET quantity={}, value={} WHERE id={};".format(row[5]-row[2], float(row[4]) - float(row[1]), row[8]))
                cur.execute("DELETE FROM dex_buyorder WHERE dex_buyorder.order_ptr_id={};".format(row[7]))
                cur.execute("DELETE FROM dex_order WHERE dex_order.id={};".format(row[7]))
            elif row[5]-row[2] == 0:
                web3_utils.safeTransferFrom(row[3], row[0], row[6], row[2])
                web3_utils.safeTransferFrom(row[0], row[3], "1", row[1])
                matched_orders.append(row[7])
                matched_orders.append(row[8])
                cur.execute("DELETE FROM dex_buyorder WHERE dex_buyorder.order_ptr_id={};".format(row[7]))
                cur.execute("DELETE FROM dex_sellorder WHERE dex_sellorder.order_ptr_id={};".format(row[8]))
                cur.execute("DELETE FROM dex_order WHERE dex_order.id={};".format(row[7]))
                cur.execute("DELETE FROM dex_order WHERE dex_order.id={};".format(row[8]))
            else:
                web3_utils.safeTransferFrom(row[3], row[0], row[6], row[5])
                web3_utils.safeTransferFrom(row[0], row[3], "1", float(row[4]))
                matched_orders.append(row[8])
                cur.execute("UPDATE dex_order SET quantity={}, value={} WHERE id={};".format(row[2]-row[5], float(row[1]) - float(row[4]), row[7]))
                cur.execute("DELETE FROM dex_sellorder WHERE dex_sellorder.order_ptr_id={};".format(row[8]))
                cur.execute("DELETE FROM dex_order WHERE dex_order.id={};".format(row[8]))
            conn.commit()


match()
