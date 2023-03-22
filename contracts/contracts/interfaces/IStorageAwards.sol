// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

interface IStorageAwards{
    function addStudentAward(address studentAdr, string calldata awardTitle, uint awardDate) external;
    function removeStudentAward(address studentAdr,uint index) external;
    function removeStudentData(address studentAdr) external;   
}