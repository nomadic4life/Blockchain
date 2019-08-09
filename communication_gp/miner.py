# Paste your version of miner.py from the clinet_mining_p
# folder here
import hashlib
import requests
from uuid import uuid4
import sys
import os.path


def get_id():
    if not os.path.exists(os.path.abspath('./my_id')):
        print('making new ID')
        f = open('./my_id', 'w')
        f.write(str(uuid4()).replace('-', ''))
        f.close()
    with open('./my_id', 'r') as f:
        content = f.readlines()
        return content[0]


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = f"http://localhost:{int(sys.argv[1])}"
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    uid = get_id()
    print("USER ID:", uid)
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof, "user_id": uid}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
