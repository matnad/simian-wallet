//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

import "../../interfaces/IERC20Minimal.sol";
import "../../interfaces/ISnxFarm.sol";
import "../../interfaces/IUniswapTokenForToken.sol";

contract HarvestFarms {

    function stake(uint256[] memory amounts, address[] memory pools, address[] memory tokens) public {
        for(uint256 i = 0; i < amounts.length; i++) {
            IERC20Minimal token = IERC20Minimal(tokens[i]);
            if(token.allowance(address(this), pools[i]) < amounts[i]) {
                token.approve(pools[i], amounts[i]);
            }
            ISnxFarm(pools[i]).stake(amounts[i]);
        }
    }

    function getRewards(address[] memory farms) public {
        for(uint256 i = 0; i < farms.length; i++) {
            ISnxFarm(farms[i]).getReward();
        }
    }

    function getRewardsAs(address[] memory farms, address rewardToken, address convertTo) public {
        getRewards(farms);
        uint256 balance = IERC20Minimal(rewardToken).balanceOf(address(this));
        IUniswapTokenForToken sushiRouter = IUniswapTokenForToken(0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F);
        address [] memory path = new address[](2);
        path[0] = rewardToken;
        path[1] = convertTo;
        IERC20Minimal rewardERC = IERC20Minimal(rewardToken);
        if(rewardERC.allowance(address(this), address(sushiRouter)) < balance) {
            rewardERC.approve(address(sushiRouter), uint256(-1));
        }
        sushiRouter.swapExactTokensForTokens(balance, 0, path, address(this), block.timestamp);
    }

}
