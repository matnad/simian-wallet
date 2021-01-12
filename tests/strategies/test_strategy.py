def test_strategy_from_owner(wallet, do_nothing, empty_strategy, owner):
    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, empty_strategy, data, {'from': owner})
    strategy_value = int(repr(tx.return_value[1]), 16)
    assert strategy_value == 666


def test_user_cant_use_strategy(wallet, do_nothing, empty_strategy, owner, user):
    sig = do_nothing.signatures['nothing']
    wallet.permit(user, do_nothing, sig, {'from': owner})

    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, empty_strategy, data, {'from': user})
    strategy_value = tx.return_value[1]
    assert strategy_value == "0x"


def test_permit_user_strategy(wallet, do_nothing, empty_strategy, owner, user, strategy_sig):
    sig = do_nothing.signatures['nothing']
    wallet.permit(user, do_nothing, sig, {'from': owner})
    wallet.permit(user, empty_strategy, strategy_sig, {'from': owner})

    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, empty_strategy, data, {'from': user})
    strategy_value = int(repr(tx.return_value[1]), 16)
    assert strategy_value == 666


def test_permit_user_all_strategies(
        wallet, empty_strategy, empty_strategy2, owner, user, all_addr, strategy_sig
):
    assert wallet.canCall(user, empty_strategy, strategy_sig) is False
    assert wallet.canCall(user, empty_strategy2, strategy_sig) is False
    wallet.permit(user, all_addr, strategy_sig, {'from': owner})
    assert wallet.canCall(user, empty_strategy, strategy_sig) is True
    assert wallet.canCall(user, empty_strategy2, strategy_sig) is True
