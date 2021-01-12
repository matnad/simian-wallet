

def test_forbid(wallet, do_expensive, owner, user):
    sig = do_expensive.signatures['burnGas']
    tx = wallet.forbid(user, do_expensive, sig, {'from': owner})
    assert "Forbid" in tx.events
    assert tx.events["Forbid"].values() == [user, do_expensive, sig]
    assert wallet.canCall(user, do_expensive, sig) is False


def test_forbid_after_permit(wallet, do_expensive, owner, user):
    sig = do_expensive.signatures['burnGas']
    wallet.permit(user, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    wallet.forbid(user, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is False

