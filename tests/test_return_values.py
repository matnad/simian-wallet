from brownie import web3
from hexbytes import HexBytes
import pytest


def parse_string(hex_obj: HexBytes) -> str:
    hex_str = str(hex_obj.hex())
    # chunk = web3.toInt(hexstr=hex_str[:64])
    len = web3.toInt(hexstr=hex_str[64:128])
    data = hex_str[128:128 + len * 2]
    return web3.toText(hexstr=data)


def split_hex_32bytes(hex_obj: HexBytes) -> list:
    hex_str = str(hex_obj.hex())
    return [hex_str[i:i + 64] for i in range(0, len(hex_str), 64)]


def test_long_bytes_array_string(wallet, do_test, owner):
    sig = do_test.signatures["getLongBytesArray"]
    tx = wallet.execute(do_test, sig, {'from': owner})
    expected = "This is a very long string. " * 12
    assert parse_string(tx.return_value[0]) == expected


def test_short_string(wallet, do_test, owner):
    sig = do_test.signatures["getShortString"]
    tx = wallet.execute(do_test, sig, {'from': owner})
    expected = "ok"
    assert parse_string(tx.return_value[0]) == expected


def test_uint_array(wallet, do_test, owner):
    sig = do_test.signatures["getUint256Array"]
    tx = wallet.execute(do_test, sig, {'from': owner})
    values = split_hex_32bytes(tx.return_value[0])
    expected = [22, 33, 44]
    for a, b, in zip(values, expected):
        assert int(a, 16) == b


def test_struct(wallet, do_test, owner):
    sig = do_test.signatures["getStruct"]
    tx = wallet.execute(do_test, sig, {'from': owner})
    values = split_hex_32bytes(tx.return_value[0])
    expected = [1514, "db3f9dc103bc5eca8148e0466a9a0416b1f250e4"]
    assert int(values[0], 16) == expected[0]
    assert values[1] == expected[1].rjust(64, '0')


@pytest.mark.parametrize("fn_exp", [
    ("getUint256", f"{1234567890:#0{66}x}"),
    ("getUint64", f"{8888:#0{66}x}"),
    ("getAddress", f"0xdb3f9dc103bc5eca8148e0466a9a0416b1f250e4"),
    ("getBool", f"{1:#0{66}x}"),
    ("getBytes32", web3.toHex(text="hello world").ljust(66, '0')),
])
def test_simple_return_values(wallet, do_test, owner, fn_exp):
    sig = do_test.signatures[fn_exp[0]]
    tx = wallet.execute(do_test, sig, {'from': owner})
    assert tx.return_value[0] == fn_exp[1]
