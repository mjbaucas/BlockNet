def search_by_private_key(chain,private_key):
    results = []
    for node in chain:
        if node.validate_private_key(private_key):
            results.append(node)
            node.disp_block_info()
    return results