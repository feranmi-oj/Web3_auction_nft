// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/presets/ERC1155PresetMinterPauser.sol";

contract ArtworkNFT is ERC1155PresetMinterPauser {

    string public _name;
    string public _symbol;
    uint256 public artworkIDCounter;
    mapping(string => string) public namemap;
    mapping(string => uint256) public idmap;
    mapping(uint256 => string) public lookupmap;


    constructor() ERC1155PresetMinterPauser("https://ipfs.io/ipfs/") { //base URI
        
    }
    
    function addArtwork( string memory artworkID, uint256 initialSupply, string memory name_, string memory symbol_ ) external {
        require(hasRole(MINTER_ROLE, _msgSender()), "ArtworkNFT: must have minter role to mint");
        
        require(idmap[artworkID] == 0, "ArtworkNFT: This artwork already exists");
        
        _name = name_;
        _symbol = symbol_;
        artworkIDCounter = artworkIDCounter + 1;
        namemap[artworkID]= _name;
        idmap[artworkID] = artworkIDCounter;
        lookupmap[artworkIDCounter] = artworkID;

        _mint(msg.sender, artworkIDCounter, initialSupply, "");        
    }
    
    function uri(uint256 id) public view virtual override returns (string memory) {
        return string( abi.encodePacked( super.uri(id), lookupmap[id]));
    }
    
    function getAllTokens(address account) public view returns (uint256[] memory){
        uint256 numTokens = 0;
        for (uint i = 0; i <= artworkIDCounter; i++) {
            if ( balanceOf(account, i) > 0) {
                numTokens++;
            }
        }
        
        uint256[] memory ret = new uint256[](numTokens);
        uint256 counter = 0;
        for (uint i = 0; i <= artworkIDCounter; i++) {
            if ( balanceOf(account, i) > 0) {
                ret[counter] = i;
                counter++;
            }
        }
        
        return ret;
    }
}