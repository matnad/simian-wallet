from brownie import web3

"""
The simian wallet has no storage variables in the static slots
starting form 0. All storage variables are stored at a specific location.
This allows a target of the delegatecall to use storage variables without
interfering with the core functionality. 
"""


def test_empty_storage(wallet, zero_addr):
    assert wallet.defaultStrategy() == zero_addr
    # Assert that the first 2 storage slots are empty (no storage variables)
    for i in range(20):
        slot_value = web3.eth.getStorageAt(str(wallet.address), i).hex()
        assert int(slot_value, 16) == 0


def test_override(wallet, do_malicious, owner):
    """ Override the first storage slot with a delegate call """
    sig = do_malicious.signatures["set"]
    wallet.execute(do_malicious, sig, {'from': owner})
    assert web3.eth.getStorageAt(str(wallet.address), 0).hex() == \
           "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()
