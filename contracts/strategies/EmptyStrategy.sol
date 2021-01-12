//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

import "../../interfaces/ISimianStrategy.sol";

contract EmptyStrategy is ISimianStrategy {

    function afterExecution(uint256 gasUsed)
        external
        override
        returns (bytes32 response)
    {
        response = bytes32(uint(666));
    }

}