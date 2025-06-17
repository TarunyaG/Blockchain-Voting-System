# blockchain.py
import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data={'message': 'Genesis Block'}, previous_hash='0')

    def create_block(self, data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'data': data,
            'previous_hash': previous_hash,
            'hash': self.hash_block(data, previous_hash)
        }
        self.chain.append(block)
        return block

    def hash_block(self, data, previous_hash):
        encoded_block = json.dumps({'data': data, 'previous_hash': previous_hash}, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_previous_block()
        previous_hash = previous_block['hash']
        new_block = self.create_block(data, previous_hash)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            if current_block['hash'] != self.hash_block(current_block['data'], current_block['previous_hash']):
                return False
        return True
