//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;
pragma experimental ABIEncoderV2;

contract DoTest {

    struct Test {
        uint256 b;
        address c;
    }

    function getStruct() public returns (Test memory r) {
        r = Test(1514, 0xDB3F9dc103bc5ecA8148e0466A9A0416b1F250E4);
    }

    function getLongBytesArray() public returns (bytes memory r) {
        r = bytes("This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. This is a very long string. ");
    }

    function getShortString() public returns (string memory r) {
        r = "ok";
    }

    function getUint256Array() public returns (uint256[3] memory r) {
        r = [uint256(22), 33, 44];
    }

    function getUint256() public returns (uint256 r) {
        r = 1234567890;
    }

    function getUint64() public returns (uint64 r) {
        r = 8888;
    }

    function getAddress() public returns (address r) {
        r = 0xDB3F9dc103bc5ecA8148e0466A9A0416b1F250E4;
    }

    function getBool() public returns (bool r) {
        r = true;
    }

    function getBytes32() public returns (bytes32 r) {
        r = bytes32("hello world");
    }
}