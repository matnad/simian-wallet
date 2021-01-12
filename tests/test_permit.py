import brownie


def test_owner_can_use_all(wallet, do_expensive, owner):
    data = do_expensive.burnGas.encode_input(1e6)
    wallet.execute(do_expensive, data, {'from': owner})

    data = do_expensive.burnGas2.encode_input(1e6)
    wallet.execute(do_expensive, data, {'from': owner})


def test_others_cant_use(wallet, do_expensive, user):
    data = do_expensive.burnGas.encode_input(1e6)
    with brownie.reverts("Unauthorized for function call"):
        wallet.execute(do_expensive, data, {'from': user})


def test_permit(wallet, do_expensive, owner, user):
    sig = do_expensive.signatures['burnGas']
    assert wallet.canCall(user, do_expensive, sig) is False
    tx = wallet.permit(user, do_expensive, sig, {'from': owner})
    assert "Permit" in tx.events
    assert tx.events["Permit"].values() == [user, do_expensive, sig]
    assert wallet.canCall(user, do_expensive, sig) is True


def test_permit_fails_for_other_sigs(wallet, do_expensive, owner, user):
    sig = do_expensive.signatures['burnGas']
    sig2 = do_expensive.signatures['burnGas2']
    wallet.permit(user, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user, do_expensive, sig2) is False


def test_permit_fails_for_other_targets(wallet, do_expensive, do_nothing, owner, user):
    sig = do_expensive.signatures['commonSig']
    wallet.permit(user, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user, do_nothing, sig) is False


def test_permit_fails_for_other_users(wallet, do_expensive, owner, user, user2):
    sig = do_expensive.signatures['commonSig']
    wallet.permit(user, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user2, do_expensive, sig) is False


def test_permit_all_sigs(wallet, do_expensive, owner, user):
    sig = do_expensive.signatures['burnGas']
    sig2 = do_expensive.signatures['burnGas2']
    wallet.permit(user, do_expensive, "0xffffffff", {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user, do_expensive, sig2) is True


def test_permit_all_targets(wallet, do_expensive, do_nothing, owner, user, all_addr):
    sig = do_expensive.signatures['commonSig']
    wallet.permit(user, all_addr, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user, do_nothing, sig) is True


def test_permit_all_users(wallet, do_expensive, owner, user, user2, all_addr):
    sig = do_expensive.signatures['commonSig']
    wallet.permit(all_addr, do_expensive, sig, {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user2, do_expensive, sig) is True


def test_permit_all(wallet, do_expensive, do_nothing, owner, user, user2, all_addr):
    sig = do_expensive.signatures['commonSig']
    sig2 = do_nothing.signatures['nothing']
    wallet.permit(all_addr, all_addr, "0xffffffff", {'from': owner})
    assert wallet.canCall(user, do_expensive, sig) is True
    assert wallet.canCall(user, do_nothing, sig) is True
    assert wallet.canCall(user, do_nothing, sig2) is True
    assert wallet.canCall(user2, do_expensive, sig) is True
    assert wallet.canCall(user2, do_nothing, sig) is True
    assert wallet.canCall(user2, do_nothing, sig2) is True


def test_permit_internal_call(wallet, owner, user):
    sig = wallet.signatures['transferOwnership']
    wallet.permit(user, wallet, sig, {'from': owner})
    assert wallet.canCall(user, wallet, sig) is True

    assert wallet.owner() == owner
    wallet.transferOwnership(user, {'from': user})


def test_permit_zero_sig_can_use_fallback(wallet, do_nothing, owner, user):
    sig = "0x00000000"
    wallet.permit(user, do_nothing, sig, {'from': owner})
    assert wallet.canCall(user, do_nothing, "") is True

    tx = wallet.execute(do_nothing, "", {'from': user})
    assert int(repr(tx.return_value[0]), 16) == 789


def test_permit_invalid_sig_can_use_fallback(wallet, do_nothing, owner, user):
    sig = "0x12345678"
    wallet.permit(user, do_nothing, sig, {'from': owner})
    assert wallet.canCall(user, do_nothing, sig) is True

    tx = wallet.execute(do_nothing, sig, {'from': user})
    assert int(repr(tx.return_value[0]), 16) == 789
