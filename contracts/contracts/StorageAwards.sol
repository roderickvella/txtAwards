// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
import "./abstracts/RestrictExternalAccess.sol";
import "./interfaces/IStorageAwards.sol";

/**
 * @dev Contract can store multiple awards per student. Student is identified by
 * a unique identifer (the public address of the student).  
 * 
 * Add/delete functions can be called externally by an authorised contract (caller contract). 
 * 
 * This contract has the feature to update the caller's contract address. This allows future updates 
 * on the caller's contract without loosing stored awards.
 * 
*/
contract StorageAwards is IStorageAwards,RestrictExternalAccess{
    using EnumerableSet for EnumerableSet.AddressSet;
    
    EnumerableSet.AddressSet private _setStudents;

    constructor(address latestContractVersion) RestrictExternalAccess(latestContractVersion) {}
  
    
    struct StudentAwards{
        Award[] awards;
    }
    
    struct Award{
        string title;
        uint date;
    }
      
    mapping(address => StudentAwards) awardsStorage;
  
    
    
    function containsStudent(address studentAdr) public view returns (bool) {
        return _setStudents.contains(studentAdr);
    }
    
    function addStudent(address studentAdr) private {
         _setStudents.add(studentAdr);
    }

    function removeStudent(address studentAdr) private {
        require(studentAdr != address(0));
        _setStudents.remove(studentAdr);
    }

    function numberOfStudents() public view returns (uint256) {
        return _setStudents.length();
    }

    function getStudentAt(uint256 index) public view returns (address) {
        return _setStudents.at(index);
    }

    //should be called from client side due to gas max 
    function getAllStudents() public view returns (address[] memory) {
        return _setStudents.values();
    }
    
    
    function addStudentAward(address studentAdr, string calldata awardTitle, uint awardDate) onlyLatestVersion external override{
        require(studentAdr != address(0));
        
        addStudent(studentAdr);
       
        StudentAwards storage studentAwards= awardsStorage[studentAdr];
        studentAwards.awards.push(Award({title:awardTitle, date:awardDate}));
    }
    
    function removeStudentAward(address studentAdr,uint index) onlyLatestVersion external override{
        Award[] storage awardArray = awardsStorage[studentAdr].awards;
        awardArray[index] = awardArray[awardArray.length - 1];
        awardArray.pop();
    }

    //deletes completely the student with assigned awards
    function removeStudentData(address studentAdr) onlyLatestVersion external override{
        uint count = getStudentAwardsCount(studentAdr);
        for(uint i=0; i<count; i++){
            Award[] storage awardArray = awardsStorage[studentAdr].awards;
            awardArray[0] = awardArray[awardArray.length - 1];
            awardArray.pop();
        }
        removeStudent(studentAdr);
    }
    
    function getStudentAward(address studentAdr, uint index) public view returns(Award memory){
        return awardsStorage[studentAdr].awards[index];
    }
    
    //should be called from client side due to gas max 
    function getStudentAwards(address studentAdr) public view returns(Award[] memory) {
        return awardsStorage[studentAdr].awards;
    }
    
    function getStudentAwardsCount(address studentAdr) public view returns(uint){
        return awardsStorage[studentAdr].awards.length;
    }
    
}