//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

contract DoMalicious {
    address test;

    function set() public {
        test = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    }

    function transferOwnership(address newOwner) public {

    }
}