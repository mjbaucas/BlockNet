nodeId = "NoDe0001"

ledger = {
    "02567435285": "Dev00001",
    "14656980610": "Dev00002"
}

if __name__ == "__main__":    
    node_1 = Node(nodeId)
    node_1.add_to_ledger(ledger)

    ping_mess = json.dumps({"type": "ping", "pub_key": node_1.pub_key})
    ping_mess = node_1.encrypt(ping_mess, node_1.network_key)
    
    while(1):
        # Broad cast ping message
        
        # Try to read any message
        
        # Process message