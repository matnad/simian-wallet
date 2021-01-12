import brownie


def test_no_target_fails(wallet, owner, zero_addr):
    with brownie.reverts("Target address required"):
        wallet.execute(zero_addr, "", {'from': owner})
