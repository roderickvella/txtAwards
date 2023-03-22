// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";

abstract contract RestrictExternalAccess is Ownable{        
    address private _latestVersion;

    constructor(address latestVersionAdr){        
        _latestVersion =latestVersionAdr;
    }

    modifier onlyLatestVersion()  {
       require(msg.sender == _latestVersion,"call not made by latest address version");
        _;
    }

    function getAccessContractVersion() public virtual returns(address){
        return _latestVersion;
    }

    function upgradeAccessContractVersion(address _newVersion) public virtual onlyOwner {  
        _latestVersion = _newVersion;
    }    
}
