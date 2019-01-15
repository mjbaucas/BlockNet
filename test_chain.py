from chain_class import Chain
from block_class import Block

if __name__ == "__main__":
    chain = Chain()
    chain.gen_next_block("asdsad", [])
    chain.display_contents()