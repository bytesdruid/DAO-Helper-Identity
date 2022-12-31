# Previously funded account is used to fund new account
# My address: BSTDOSCCPYN3AZNRGBX3VO4XBEAH2TKCGKYZPMYIIRNYAFHJZGNASJMOEI
# My private key: cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg==
# My passphrase: comfort anxiety nuclear citizen below airport leisure smooth public major rose worth mother stamp tribe bitter medal cotton wink wealth like wagon aware abandon witness

import json
import base64
import contracts
from util import *
from typing import Tuple, List
from algosdk import *
from algosdk.future.transaction import *
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
from algosdk.v2client.algod import AlgodClient
from algosdk.logic import get_application_address


pk_1 = "cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg=="
sk_1 = mnemonic.to_private_key("comfort anxiety nuclear citizen below airport leisure smooth public major rose worth mother stamp tribe bitter medal cotton wink wealth like wagon aware abandon witness")

ALGOD_ADDRESS = "https://testnet-api.algonode.network"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

def getAlgodClient() -> AlgodClient:
    return AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

APPROVAL_PROGRAM = b""
CLEAR_STATE_PROGRAM = b""

def getContracts(client: AlgodClient) -> Tuple[bytes, bytes]:

    global APPROVAL_PROGRAM
    global CLEAR_STATE_PROGRAM

    if len(APPROVAL_PROGRAM) == 0:
        APPROVAL_PROGRAM = fullyCompileContract(client, contracts.approval_program())
        CLEAR_STATE_PROGRAM = fullyCompileContract(client, contracts.clear_state_program())

    return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM

def createIdentityApp(
    client,
    sender_addr,
    sender_pk
) -> int:

    approval, clear = getContracts(client)

    globalSchema = transaction.StateSchema(num_uints=1, num_byte_slices=11)
    localSchema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_args = [
        # encodes the sender address as the soulbound address
        encoding.decode_address(sender_addr),
    ]

    txn = transaction.ApplicationCreateTxn(
        sender=sender_addr,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=globalSchema,
        local_schema=localSchema,
        app_args=app_args,
        sp=client.suggested_params(),
    )

    signedTxn = txn.sign(sender_pk)

    client.send_transaction(signedTxn)

    response = waitForTransaction(client, signedTxn.get_txid())
    assert response.applicationIndex is not None and response.applicationIndex > 0
    return response.applicationIndex

#### ACCOUNT GENERATION ####

# creates an account and prints info
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    new_my_address = format(address)
    new_my_private_key = format(private_key)
    new_my_passphrase = format(mnemonic.from_private_key(private_key))
    return[new_my_address, new_my_private_key, new_my_passphrase]

# funds new account
def fund_new_acct(private_key, my_address, new_acct_addr):
    algod_address = "https://testnet-api.algonode.network"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    # build transaction
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = new_acct_addr
    note = "Hello World".encode()
    # one algo or 1000000 micro algos
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

###################
#### APP CALLS ####
###################
# CALLING THE FUNCTIONS #
### This function creates the first new account
new_address, new_private_key, new_passphrase = generate_algorand_keypair()
print("New account address: {}".format(new_address))
print("New private key: {}".format(new_private_key))
print("New passphrase: {}".format(new_passphrase))
### This function funds the new account with a previously funded testnet account
fund_new_acct("cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg==", "BSTDOSCCPYN3AZNRGBX3VO4XBEAH2TKCGKYZPMYIIRNYAFHJZGNASJMOEI", new_address)

AlgodClient = getAlgodClient()
app = createIdentityApp(
    client=AlgodClient,
    sender_addr=new_address,
    sender_pk=new_private_key,
)
print(app)





