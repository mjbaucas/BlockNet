import hashlib
import json

from node_class import Node, Device

from block_utils import gen_genesis_block, gen_next_block
from chain_utils import search_by_private_key
from key_cipher import AESCipher

node_private_key = "NoDe0001"

ledger = {
    "02567435285": "Dev00001",
    "14656980610": "Dev00002"
}

if __name__ == "__main__":    
    # node.blockchain.append(gen_genesis_block())
    # prev_block = node.blockchain[0]

    node_1 = Node("NoDe0001")
    node_1.add_to_ledger(ledger)
    device_1 = Device("Dev00001", "02567435285")
    device_2 = Device("Dev00002", "14656980610")
    device_3 = Device("Dev00003", "23654350610")

    # D1 creates a requests of access to N1
    d1_mess = json.dumps({"type": "access", "res_energy": 5, "rssi": -69})
    d1_mess = device_1.encrypt(d1_mess, None)
    d1_mess = device_1.dig_sign(d1_mess)

    # D1 sends request to N1
    node_1.process_message(d1_mess)
    
    # D2 creates a requests of access to N1
    d2_mess = json.dumps({"type": "access", "res_energy": 5, "rssi": -69})
    d2_mess = device_2.encrypt(d2_mess, None)
    d2_mess = device_2.dig_sign(d2_mess)
    
    # D2 sends request to N1
    node_1.process_message(d2_mess)
    
    # D1 requests to send data to D2
    d1_to_d2_mess = json.dumps({"type": "send_data", "destination": "14656980610", "rssi": -69})
    d1_to_d2_mess = device_1.encrypt(d1_to_d2_mess, None)
    d1_to_d2_mess = device_1.dig_sign(d1_to_d2_mess)
    node_1.process_message(d1_to_d2_mess)

    # D3 creates requests of access to N1
    d3_mess = json.dumps({"type": "access", "res_energy": 5, "rssi": -69})
    d3_mess = device_3.encrypt(d3_mess, None)
    d3_mess = device_3.dig_sign(d3_mess)

    # D3 sends request to N1
    node_1.process_message(d3_mess)