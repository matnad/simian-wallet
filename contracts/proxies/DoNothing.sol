//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

contract DoNothing {
    function nothing(uint256 burn) public {
    }

    function nothing2(uint256 burn) public {
    }

    function commonSig() public {

    }

    fallback(bytes calldata) external returns (bytes memory) {
        bytes memory ret = new bytes(32);
        assembly { mstore(add(ret, 32), 789) }
        return ret;
    }
}