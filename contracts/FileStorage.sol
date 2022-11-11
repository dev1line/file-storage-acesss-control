// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/CountersUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/structs/EnumerableSetUpgradeable.sol";
import "./IFileStorage.sol";

/**
 *  @title  Dev File Storage Contract
 *
 *  @author Stephen Sang
 *
 *  @notice This smart contract is contract to store metadata of files
 */
contract FileStorage is OwnableUpgradeable {
    using CountersUpgradeable for CountersUpgradeable.Counter;
    using EnumerableSetUpgradeable for EnumerableSetUpgradeable.UintSet;
    using EnumerableSetUpgradeable for EnumerableSetUpgradeable.AddressSet;

    CountersUpgradeable.Counter private _fileId;

    mapping(uint256 => IFileStorage.File) private _files;
    mapping(uint256 => EnumerableSetUpgradeable.AddressSet) private _fileIdToWhitelist;
    mapping(address => EnumerableSetUpgradeable.UintSet) private _fileOfOwner;

    modifier validFileId(uint256 _fileID) {
        require(_fileID > 0 && _fileID <= _fileId.current(), "ID: Invalid file ID");
        _;
    }

    /**
     *  @notice Initialize new logic contract.
     */
    function initialize(address user) public initializer {
        OwnableUpgradeable.__Ownable_init();
        OwnableUpgradeable.transferOwnership(user);
    }

    /**
     * @dev Create new metadata
     * @param _fileType type of file uploaded
     * @param _fileName name of file uploaded
     * @param _fileLink IPFS link
     * @param _whiteList array of authorized address
     * @param _privateMetadata extra private metadata
     * @param _privateCreator address pf caller
     */
    function createMetadata(
        string memory _fileType,
        string memory _fileName,
        string memory _fileLink,
        address[] memory _whiteList,
        bytes memory _privateMetadata,
        address _privateCreator
    ) external onlyOwner returns (uint256) {
        _fileId.increment();
        _files[_fileId.current()] = IFileStorage.File({
            id: _fileId.current(),
            fileType: _fileType,
            fileName: _fileName,
            fileLink: _fileLink,
            privateMetadata: _privateMetadata,
            privateCreator: _privateCreator
        });
        // Add authorized to whitelist
        for (uint256 i = 0; i < _whiteList.length; i++) {
            _fileIdToWhitelist[_fileId.current()].add(_whiteList[i]);
        }
        // Update owner of File
        _fileOfOwner[_privateCreator].add(_fileId.current());

        return _fileId.current();
    }

    /**
     * @dev Read metadata from file ID
     * @param _fileID ID of file uploaded
     */
    function readMetadata(uint256 _fileID)
        external
        view
        onlyOwner
        validFileId(_fileID)
        returns (IFileStorage.File memory)
    {
        return _files[_fileID];
    }

    /**
     * @dev Update metadata from file ID
     * @param _fileID ID of file uploaded
     * @param _newFile struct of new file
     */
    function updateMetadata(uint256 _fileID, IFileStorage.File memory _newFile)
        external
        onlyOwner
        validFileId(_fileID)
    {
        _files[_fileID] = _newFile;
    }

    /**
     * @dev Delete metadata from file ID
     * @param _fileID ID of file uploaded
     */
    function deleteMetadata(uint256 _fileID, address _user) external onlyOwner validFileId(_fileID) {
        delete _files[_fileID];
        _fileOfOwner[_user].remove(_fileID);
    }

    /**
     * @dev Add Authorized User
     * @param _fileID file ID
     * @param _user address of user
     */
    function addAuthorizedUser(uint256 _fileID, address _user) external onlyOwner validFileId(_fileID) {
        _fileIdToWhitelist[_fileID].add(_user);
    }

    /**
     * @dev Remove Authorized User
     * @param _fileID file ID
     * @param _user address of user
     */
    function removeAuthorizedUser(uint256 _fileID, address _user) external onlyOwner validFileId(_fileID) {
        _fileIdToWhitelist[_fileID].remove(_user);
    }

    /**
     * @dev Returns true if an address (leaf)
     * @param _fileID file ID
     * @param _caller address of caller
     */
    function verify(uint256 _fileID, address _caller) public view returns (bool) {
        return _files[_fileID].privateCreator == _caller || _fileIdToWhitelist[_fileID].contains(_caller);
    }

    /**
     * @dev Get all file of owner
     * @param _caller address of caller
     */
    function getMyFiles(address _caller) external view onlyOwner returns (IFileStorage.File[] memory) {
        IFileStorage.File[] memory allFiles = new IFileStorage.File[](_fileOfOwner[_caller].length());
        for (uint256 i = 0; i < _fileOfOwner[_caller].length(); i++) {
            allFiles[i] = _files[_fileOfOwner[_caller].at(i)];
        }
        return allFiles;
    }

    /**
     * @dev Get current ID of file
     */
    function getCurrentId() external view returns (uint256) {
        return _fileId.current();
    }
}
