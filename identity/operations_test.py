from time import time, sleep

import pytest

from algosdk import account, encoding
from algosdk.logic import get_application_address

from .operations import createIdentityApp
from .util import getBalances, getAppGlobalState, getLastBlockTimestamp
from .testing.setup import getAlgodClient
from .testing.resources import getTemporaryAccount, optInToAsset, createDummyAsset

def test_creation():
    client = getAlgodClient()

    