//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

contract Dummy {
}

contract DoExpensive {

    function burnGas(uint256 burn) public returns (uint256 burned){
        uint256 start = gasleft();
        assert(start > burn + 200);
        uint256 end = start - burn;
        uint c;
        while (gasleft() > end + 24000) {
            new Dummy();
        }
        while(gasleft() > end) {
            c++;
        }
        burned = start - gasleft();
    }

    function burnGas2(uint256 burn) public returns (uint256 burned){
        return burnGas(burn);
    }

    function commonSig() public {

    }

}