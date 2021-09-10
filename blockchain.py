# https://medium.com/coinmonks/python-tutorial-build-a-blockchain-713c706f6531

import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = [] #an empty list that we’ll add blocks to. Quite literally our ‘block-chain’
        self.pending_transactions = [] #when users send our coins to each other, their transactions will sit in this array until we approve & add them to a new block
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.",
                       proof=100) #this is a method that we’ll define soon, and we’ll use it to add each block to the chain

    # Create a new block listing key/value pairs of block information in a JSON object.
    # Reset the list of pending transactions & append the newest block to the chain.
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1, #Take the length of our blockchain and add 1 to it
            'timestamp': time(),
            'transactions': self.pending_transactions, #any transactions that are sitting in the ‘pending’ list will be included in our new block
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]), #a hashed version of the most recent approved block.
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    # Search the blockchain for the most recent block.
    @property
    def last_block(self):
        return self.chain[-1]

    # Add a transaction with relevant info to the 'blockpool' - list of pending tx's.

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    # receive one block. Turn it into a string, turn that into Unicode (for hashing). Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

# Azionamento della classe
blockchain = Blockchain()

t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)
t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
blockchain.new_block(6789)

print("Genesis block: ", blockchain.chain)
