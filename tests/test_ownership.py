import brownie


def test_ownership(wallet, owner):
    assert wallet.owner() == owner


def test_transfer_ownership(wallet, owner, user):
    tx = wallet.transferOwnership(user, {'from': owner})
    assert "OwnershipTransferred" in tx.events
    assert tx.events["OwnershipTransferred"].values() == [owner, user]
    assert wallet.owner() == user


def test_transfer_to_zero_reverts(wallet, owner, zero_addr):
    with brownie.reverts("New owner is the zero address"):
        wallet.transferOwnership(zero_addr, {'from': owner})


def test_user_transfer_fails(wallet, user):
    with brownie.reverts("Unauthorized for function call"):
        wallet.transferOwnership(user, {'from': user})
