import hashlib
import time


class MerkleTree:
    def __init__(self, forMerkle_hash):
        self.forMerkle_hash = forMerkle_hash
        self.tree = self.construct_merkle_tree()

    def construct_merkle_tree(self):
     if not self.forMerkle_hash:
            return hashlib.sha256(b"").hexdigest()

        # Create a list of transaction hashes
     forMerkle_hash = self.forMerkle_hash

        # Build the Merkle tree
     while len(forMerkle_hash) > 1:
            hashes = []
            for i in range(0, len(forMerkle_hash), 2):
                left_hash = forMerkle_hash[i]
                right_hash = forMerkle_hash[i + 1] if i + 1 < len(forMerkle_hash) else left_hash
                combined_hash = hashlib.sha256((left_hash + right_hash).encode('utf-8')).hexdigest()
                hashes.append(combined_hash)
            forMerkle_hash = hashes

     return forMerkle_hash




class Transaction_Structure:
    def __init__(self, sender, recipient, coins,message):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.coins = coins
        self.merkl_path =self.calc_hash_transaction()
        
    def calc_hash_transaction(self):
       data = (
            str(self.sender) +
            str(self.recipient) +
            str(self.message) +str(self.coins)
        )
       return hashlib.sha256(data.encode()).hexdigest()

    def to_string(self):
        return f"**{self.sender} send to {self.recipient}**\ncoins: {self.coins}\nMessage: {self.message}\nHash:{self.merkl_path}"
    
    

class Block_Structure:
    def __init__(self, index, previous_hash, timestamp,data, transactions,merkle_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.transactions = transactions
        self.hash = self.calc_hash()
        self.merkle_hash = merkle_hash
        
    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()
    

class Blockchain:
    def __init__(self):
        self.chain = [self.default_genesis_block()]
        self.transactions_list = []


    def default_genesis_block(self):
        return Block_Structure(1, "0", int(time.time()), "Genesis Block","0",0)

    def getPreviousBlock(self):
        return self.chain[-1]
    
    def update_list_transactions(self, transaction):
        self.transactions_list.append(transaction)

    def addTransaction(self):
        previous_block = self.getPreviousBlock()
        index = previous_block.index
        if index != 1:   
            print(f"index--->{index}")
            if  index > len(self.chain):
                print("#Invalid block index for adding transaction")
                return False  
            
            data = previous_block.data
            timestamp = int(time.time())
            new_transactions = self.transactions_list.copy()
            # print(new_transactions[0].merkl_path)
            # print(new_transactions.merkl_path)
            transaction_paths = []
            for i in range(0,len(new_transactions)):
              print(f"inarray path-->{new_transactions[i].merkl_path}")
              transaction_paths.append(new_transactions[i].merkl_path)
            merkle_path = MerkleTree(f"{transaction_paths}")
            print(f"merkle_path-->{merkle_path.tree}")
            new_block = Block_Structure(index, previous_block.previous_hash, timestamp,data, new_transactions,merkle_path.tree)
            self.chain[-1] = new_block
            return True
        elif index == 1:
            return 'genesis'
        else:
            return False
        
    
    def checkBlocks_valid(self):
     if len(self.chain)>1:
        for i in range(1, len(self.chain)):
            blockNext = self.chain[i]
            blockBefore = self.chain[i - 1]

            if blockNext.hash != blockNext.calc_hash():
                return False
            if blockNext.previous_hash != blockBefore.hash:
                return False
            return True
     else:
            return "genesis"
         
        
    def add_block(self, data):
        self.transactions_list = []
        previous_block = self.getPreviousBlock()
        new_index = previous_block.index + 1
        new_timestamp = int(time.time())
        new_hash = previous_block.hash
        new_block = Block_Structure(new_index, new_hash, new_timestamp, data,"0",'0')
        self.chain.append(new_block)
        return True
    


def callforTransactionStructure(sender, resepient, coins , message): # Create a new transaction
    new_transaction = Transaction_Structure(f"{sender}", f"{resepient}",int(coins),f"{message}")
    return new_transaction
    

