pragma solidity 0.7.6;

interface ISnxFarm {
    function getReward() external;
    function stake(uint256 amount) external;
}