//SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

contract Guarded {
    address constant public ANY = address(uint160(-1));
    bytes4 constant public ANY4 = 0xffffffff;

    // keccak256 hash of "guarded.owner" subtracted by 1
    bytes32 private constant _OWNER_SLOT = 0x94e6c49109b7c66b44d1c8e437511b1024df1040fa13894e8fcee32ac2a9affa;

    mapping (address => mapping (address => mapping (bytes4 => bool))) internal acl;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event Permit(address indexed src, address indexed dst, bytes4 indexed sig);
    event Forbid(address indexed src, address indexed dst, bytes4 indexed sig);

    modifier internalAuth {
         require(isAuthorized(msg.sender, address(this), msg.sig), "Unauthorized for function call");
        _;
    }

    constructor() {
        _setOwner(msg.sender);
        emit OwnershipTransferred(address(0), msg.sender);
    }

    function _setOwner(address owner) internal {
        assembly {
            sstore(_OWNER_SLOT, owner)
        }
    }

    function owner() public view returns (address _owner) {
        bytes32 slot = _OWNER_SLOT;
        assembly {
            _owner := sload(slot)
        }
    }

    function transferOwnership(address newOwner) public internalAuth {
        require(newOwner != address(0), "New owner is the zero address");
        emit OwnershipTransferred(owner(), newOwner);
        _setOwner(newOwner);
    }


    function permit(address src, address dst, bytes4 sig) public internalAuth {
        acl[src][dst][sig] = true;
        emit Permit(src, dst, sig);
    }

    function forbid(address src, address dst, bytes4 sig) public internalAuth {
        acl[src][dst][sig] = false;
        emit Forbid(src, dst, sig);
    }

    function canCall(address src, address dst, bytes4 sig) public view returns (bool) {

        return acl[src][dst][sig]
            || acl[src][dst][ANY4]
            || acl[src][ANY][sig]
            || acl[src][ANY][ANY4]
            || acl[ANY][dst][sig]
            || acl[ANY][dst][ANY4]
            || acl[ANY][ANY][sig]
            || acl[ANY][ANY][ANY4];
    }

    function isAuthorized(address src, address target, bytes4 sig) internal view returns (bool) {
        if (src == owner()) {
            return true;
        }
        return canCall(src, target, sig);
    }
}