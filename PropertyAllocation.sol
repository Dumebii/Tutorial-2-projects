//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract propertyTransfer {
    address public DA;
    uint256 public totalNoOfProperties;

    function PropertyTransfer() public {
        DA=msg.sender;
    }
    modifier onlyOwner() {
        require(msg.sender==DA);
        _;
    }
    struct Property {
        string name;
        bool isSold;
    }
    mapping(address => mapping(uint256 => Property)) public propertiesOwner;
    mapping(address => uint256) individualCountOfPropertyOwner;

    event PropertyAllocated(address indexed _verifiedOwner, uint256 indexed _totalNoOfPropertyCurrently, string _msg);
    event PropertyTransferred(address indexed _from, address);
    
    function getPropertyCOuntOfANyAddress(address _onwerAddress) public returns(uint256) {
        uint count=0;
        for(uint i=0; i<individualCountOfPropertyOwner[_onwerAddress]; i++) {
            //if(propertyTransfer [_onwerAddress][i].isSold!=true)
            //count++;
        }
        return count;
    }
    function allotProperty(address _verifiedOwner, string memory _propertyName)onlyOwner public
    {
        propertiesOwner[_verifiedOwner][individualCountOfPropertyOwner[_verifiedOwner]++].name = _propertyName;
        totalNoOfProperties++;
       emit  PropertyAllocated(_verifiedOwner, individualCountOfPropertyOwner[_verifiedOwner], _propertyName);

    }
    function isOwner(address _checkOwnerAddress, string memory _propertyName) public returns(uint) {
        uint i;
        bool flag;
        for(i=0;i<individualCountOfPropertyOwner[_checkOwnerAddress]; i++)
        {
            if(propertiesOwner[_checkOwnerAddress][i].isSold=true) {
                break;
            }
            if(flag==true) {
                break;
            }
        }
        if(flag==true) {
            return i;   
        }
        else{
            return 999999999;
        }
    }
    function transferProperty(address _to, string memory _propertyName) public returns(bool, uint) {
        uint256 checkOwner= isOwner(msg.sender, _propertyName);
        bool flag;
        if(checkOwner!= 999999999 && propertiesOwner[msg.sender][checkOwner].isSold ==false) {
            propertiesOwner[msg.sender][checkOwner].isSold = true;
            propertiesOwner[msg.sender][checkOwner].name = "Sold";
            propertiesOwner[_to][individualCountOfPropertyOwner[_to]++].name = _propertyName;
            flag = true;
           emit PropertyTransferred(msg.sender, _to);
        }
        else{
            flag=false;
            emit PropertyTransferred(msg.sender, _to);
        }
        return (flag, checkOwner);
    }

}
 