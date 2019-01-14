import datetime
from block_class import Block
from transaction_class import Transaction


class Chain:
	def __init__():
		self.chain = [gen_genesis_block()]
		

	def gen_next_block(prev_block, private_key, transactions):
		index = prev_block.index + 1
		timestamp = datetime.datetime.now()
		data = transactions
		hashed_block = prev_block.gen_hashed_block()
		return Block(index, timestamp, data, hashed_block, private_key)


def gen_genesis_block():
    transaction = [Transaction('genesis', None, None)]
    return Block(0, datetime.datetime.now(), transaction, "0", "0")

