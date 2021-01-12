//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

import "./Guarded.sol";

contract SimianWallet is Guarded {
    bytes4 private constant STRATEGY_SIG = bytes4(0xc893a971);

    // keccak256 hash of "simianwallet.defaultstrategy" subtracted by 1
    bytes32 private constant _DEFAULT_STRATEGY_SLOT = 0x0678490ae7ad248de7d58e178f19fc83f13bf124b843300bd4cc6396c8d61e59;

    function _execute(address target, address strategy, bytes memory data)
        internal
        returns (bytes memory callResponse, bytes memory strategyResponse)
    {
        uint256 initialGas = gasleft();
        require(target != address(0), "Target address required");
        bytes4 sig;
        if (data.length >= 4) {
            sig =
                data[0] |
                (bytes4(data[1]) >> 8) |
                (bytes4(data[2]) >> 16) |
                (bytes4(data[3]) >> 24);
        }
        require(isAuthorized(msg.sender, target, sig), "Unauthorized for function call");
//        assembly {
//            let succeeded := delegatecall(sub(gas(), 5000), target, add(data, 0x20), mload(data), 0, 0)
//            let size := returndatasize()
//
//            callResponse := mload(0x40)
//            mstore(0x40, add(callResponse, and(add(add(size, 0x20), 0x1f), not(0x1f))))
//            mstore(callResponse, size)
//            returndatacopy(add(callResponse, 0x20), 0, size)
//
//            switch iszero(succeeded)
//            case 1 {
//                // throw if delegatecall failed
//                revert(add(callResponse, 0x20), size)
//        }

        (bool success, bytes memory callResponse) = target.delegatecall(data);
        if(!success) {
            assembly {
                let ptr := mload(0x40)
                let size := returndatasize()
                returndatacopy(ptr, 0, size)
                revert(ptr, size)
            }
        }
//        bytes memory strategyResponse = new bytes(32);
//        assembly { mstore(add(strategyResponse, 32), sub(initialGas, gas())) }
        if (strategy != address(0) && isAuthorized(msg.sender, strategy, STRATEGY_SIG)) {
            uint256 gasUsed = initialGas - gasleft();
            data = abi.encodeWithSelector(STRATEGY_SIG, gasUsed);
            (, bytes memory strategyResponse) = strategy.delegatecall(data);
        }

        return (callResponse, strategyResponse);
    }

    function execute(address target, address strategy, bytes memory data)
        external
        payable
        returns (bytes memory callResponse, bytes memory strategyResponse)
    {
        return _execute(target, strategy, data);
    }

    function execute(address target, bytes memory data)
        external
        payable
        returns (bytes memory callResponse, bytes memory strategyResponse)
    {
        return _execute(target, defaultStrategy(), data);
    }

    receive() external payable {
    }

    function setDefaultStrategy(address strategy) public internalAuth {
        assembly {
            sstore(_DEFAULT_STRATEGY_SLOT, strategy)
        }
    }

    function defaultStrategy() public view returns (address _defaultStrategy) {
        bytes32 slot = _DEFAULT_STRATEGY_SLOT;
        assembly {
            _defaultStrategy := sload(slot)
        }
    }
}