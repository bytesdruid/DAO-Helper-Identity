from time import time, sleep

import pytest

from algosdk import account, encoding
from algosdk.logic import get_application_address

import operations
import util
import testing.setup
import testing.resources

def test_creation():
    client = testing.setup.getAlgodClient()
    creator = testing.resources.getTemporaryAccount(client)

    appID = operations.createIdentityApp(
        client=client,
        sender=creator,
    )

    print(appID)

test_creation()