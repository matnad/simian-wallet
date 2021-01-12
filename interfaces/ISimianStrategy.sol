//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

interface ISimianStrategy {
    function afterExecution(uint256 gasUsed) external returns(bytes32 response);
}