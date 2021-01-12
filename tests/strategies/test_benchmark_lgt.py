BURN_GAS = 4000000


def test_expensive_eoa(do_expensive, owner):
    bal = owner.balance()
    tx = do_expensive.burnGas(BURN_GAS, {'from': owner})
    account_paid = bal - owner.balance()
    assert 0 < account_paid
    print(f"Tx Gas Used: {tx.gas_used}")
    print(f"Total ETH spent: {account_paid.to('ether')}")


def test_expensive_wallet(wallet, do_expensive, owner, zero_addr):
    balw = wallet.balance()
    bala = owner.balance()
    data = do_expensive.burnGas.encode_input(BURN_GAS)
    tx = wallet.execute(do_expensive, zero_addr, data, {'from': owner})
    wallet_paid = balw - wallet.balance()
    account_paid = bala - owner.balance()
    assert tx.return_value[0] is not None
    assert account_paid == tx.gas_used * tx.gas_price  # acc1 only pays gas
    print(f"Tx Gas Used: {tx.gas_used}")
    print(f"Total ETH spent: {(wallet_paid + account_paid).to('ether')}")


def test_expensive_lgt(wallet, lgt_strategy, do_expensive, owner):
    balw = wallet.balance()
    bala = owner.balance()
    data = do_expensive.burnGas.encode_input(BURN_GAS)
    tx = wallet.execute(do_expensive, lgt_strategy, data, {'from': owner})
    wallet_paid = balw - wallet.balance()
    account_paid = bala - owner.balance()
    assert tx.return_value[0] is not None
    tokens_used = int(repr(tx.return_value[1]), 16)
    assert tokens_used > 0
    assert 0 < wallet_paid
    assert account_paid == tx.gas_used * tx.gas_price  # acc1 only pays gas
    print(f"LGT bought and used: {tokens_used}")
    print(f"Tx Gas Used: {tx.gas_used}")
    print(f"Total ETH spent: {(wallet_paid + account_paid).to('ether')}")

