from typing import Tuple, List

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.logic import get_application_address
from algosdk import account, encoding

from pyteal import compileTeal, Mode

import account
import contracts
import util 

APPROVAL_PROGRAM = b""
CLEAR_STATE_PROGRAM = b""

def getContracts(client: AlgodClient) -> Tuple[bytes, bytes]:

    global APPROVAL_PROGRAM
    global CLEAR_STATE_PROGRAM

    if len(APPROVAL_PROGRAM) == 0:
        APPROVAL_PROGRAM = util.fullyCompileContract(client, contracts.approval_program())
        CLEAR_STATE_PROGRAM = util.fullyCompileContract(client, contracts.clear_state_program())

    return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM

def createIdentityApp(
    client: AlgodClient,
    sender: account.Account,
) -> int:

    approval, clear = getContracts(client)

    globalSchema = transaction.StateSchema(num_uints=7, num_byte_slices=2)
    localSchema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_args = [
        # add app args as needed
        # currently no app args needed on creation
    ]

    txn = transaction.ApplicationCreateTxn(
        sender=sender.getAddress(),
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=globalSchema,
        local_schema=localSchema,
        app_args=app_args,
        sp=client.suggested_params(),
    )

    signedTxn = txn.sign(sender.getPrivateKey())

    client.send_transaction(signedTxn)

    response = util.waitForTransaction(client, signedTxn.get_txid())
    assert response.applicationIndex is not None and response.applicationIndex > 0
    return response.applicationIndex
