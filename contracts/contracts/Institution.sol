// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
// import "hardhat/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

import "./StorageAwards.sol";

contract Institution is Ownable {
    string public version = "0.1";
   
    StorageAwards private storageAwards;
    mapping(address => uint) private nonceAwardSign; //avoid signature replay attacks

    constructor(bool createStorage)  { 
        if(createStorage){
            //if storage does not exist yet, then create a new instance
            storageAwards = new StorageAwards(address(this)); 
        }                           
    }
 
    function getStorageAwards () public view returns(StorageAwards){
        return storageAwards;
    }

    //should be called by the old institution contract to update the owner to the upgraded institution contract
    function upgradeStorageAwardsOwner(address _newVersion) external onlyOwner{        
        storageAwards.upgradeAccessContractVersion(_newVersion);
    }

    //this should be called only if storage does not exist yet for this contract
    function setStorageAwards(address storageAddress) external onlyOwner{
        storageAwards = StorageAwards(storageAddress);
    }        

    function getNonceAwardSign(address studentAddress) public view returns(uint){
        return nonceAwardSign[studentAddress];
    }

    function addAwardSignedByStudent(bytes memory signature, address studentAddress,string memory awardTitle, uint awardDate) external onlyOwner{
    
        bytes32 hash_data = keccak256(abi.encodePacked(awardTitle,awardDate,nonceAwardSign[studentAddress],block.chainid, address(this)));
        bytes32 digest = ECDSA.toEthSignedMessageHash(hash_data);       

        address recoveredSigner = ECDSA.recover(digest, signature);
    
        require(recoveredSigner == studentAddress,"Address extracted from sig does not match");

        //increase nonce signature
        nonceAwardSign[studentAddress]++;      

        //proceed and store award
        storageAwards.addStudentAward(studentAddress, awardTitle, awardDate);
            
    }

    function removeAward(address studentAddress, uint index) external onlyOwner{
        //remove award
        storageAwards.removeStudentAward(studentAddress,index);
    }

    function removeStudentData(address studentAddress)external onlyOwner{
        //remove awards assigned to student and also the student's address - applies for upcoming calls
        storageAwards.removeStudentData(studentAddress);
    }

}