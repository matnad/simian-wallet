def test_no_default_no_strategy(wallet, do_nothing, zero_addr, owner):
    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, zero_addr, data, {'from': owner})
    strategy_value = tx.return_value[1]
    assert strategy_value == "0x"


def test_no_default_with_strategy(wallet, do_nothing, empty_strategy, owner):
    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, empty_strategy, data, {'from': owner})
    strategy_value = tx.return_value[1]
    assert int(repr(strategy_value), 16) == 666


def test_set_default_strategy(wallet, empty_strategy, zero_addr, owner):
    assert wallet.defaultStrategy() == zero_addr
    wallet.setDefaultStrategy(empty_strategy, {'from': owner})
    assert wallet.defaultStrategy() == empty_strategy


def test_default_strategy(wallet, do_nothing, empty_strategy, owner):
    wallet.setDefaultStrategy(empty_strategy, {'from': owner})
    data = do_nothing.nothing.encode_input(0)
    # omit strategy field to use default strategy
    tx = wallet.execute(do_nothing, data, {'from': owner})
    strategy_value = tx.return_value[1]
    assert int(repr(strategy_value), 16) == 666


def test_overwrite_default_strategy(wallet, do_nothing, empty_strategy, empty_strategy2, owner):
    wallet.setDefaultStrategy(empty_strategy, {'from': owner})
    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, empty_strategy2, data, {'from': owner})
    strategy_value = tx.return_value[1]
    assert int(repr(strategy_value), 16) == 1337


def test_default_strategy_requires_permit(wallet, owner, user, do_nothing, empty_strategy):
    wallet.setDefaultStrategy(empty_strategy, {'from': owner})
    sig = do_nothing.signatures['nothing']
    wallet.permit(user, do_nothing, sig, {'from': owner})

    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, data, {'from': user})
    strategy_value = tx.return_value[1]
    assert strategy_value == "0x"


def test_permit_default_strategy(wallet, owner, user, do_nothing, empty_strategy, strategy_sig):
    wallet.setDefaultStrategy(empty_strategy, {'from': owner})
    sig = do_nothing.signatures['nothing']
    wallet.permit(user, do_nothing, sig, {'from': owner})
    wallet.permit(user, empty_strategy, strategy_sig, {'from': owner})

    data = do_nothing.nothing.encode_input(0)
    tx = wallet.execute(do_nothing, data, {'from': user})
    strategy_value = tx.return_value[1]
    assert int(repr(strategy_value), 16) == 666
