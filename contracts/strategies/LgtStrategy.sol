//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

import "../../interfaces/ISimianStrategy.sol";
import "../../interfaces/ILGT.sol";

contract LgtStrategy is ISimianStrategy {

    function afterExecution(uint256 gasUsed)
        public
        override
        returns (bytes32 response)
    {
        ILGT lgt = ILGT(0x000000000000C1CB11D5c062901F32D06248CE48);
        uint256 optimalTokens = (gasUsed + 60000) / 41300;
        if (optimalTokens > 0) {
            uint256 buyCost = lgt.getEthToTokenOutputPrice(optimalTokens);
            if (buyCost < ((18145 * optimalTokens) - 24000) * tx.gasprice) {
                if (address(this).balance >= buyCost) {
                    lgt.buyAndFree22457070633{value : buyCost}(optimalTokens);
                } else if(address(this).balance > 0) {
                    lgt.buyMaxAndFree{value : address(this).balance}(block.timestamp);
                }
            }
        }
        response = bytes32(gasUsed);
    }
}