// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "./IFileStorage.sol";

/**
 *  @title  Dev Access Control Contract
 *
 *  @author Stephen Sang
 *
 *  @notice This smart contract is contract to control metadata access of files
 */
contract AccessControl is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    /**
     * @notice storage of metadata.
     */
    IFileStorage public fileStorage;

    event SetFileStorage(address indexed newFileStorage);
    event CreateFile(uint256 indexed _fileID);
    event UpdateFile(uint256 indexed _fileID);
    event DeleteFile(uint256 indexed _fileID);
    event AddAuthorizedUser(uint256 indexed _fileID, address indexed _user);
    event RemoveAuthorizedUser(uint256 indexed _fileID, address indexed _user);

    modifier onlyCreator(uint256 _fileID, address creator) {
        require(fileStorage.readMetadata(_fileID).privateCreator == creator, "Ownable: Invalid creator");
        _;
    }

    /**
     * @notice Initialize new logic contract.
     */
    function initialize() public initializer {
        OwnableUpgradeable.__Ownable_init();
    }

    /**
     * @dev Set new storage contract address
     * @param _newFileStorage storage address
     */
    function setFileStorage(IFileStorage _newFileStorage) external onlyOwner {
        fileStorage = _newFileStorage;

        emit SetFileStorage(address(_newFileStorage));
    }

    /**
     * @dev Create new File
     * @param _fileType type of file uploaded
     * @param _fileName name of file uploaded
     * @param _fileLink IPFS link
     * @param _whiteList array of authorized address
     * @param _privateMetadata extra private metadata
     */
    function createFile(
        string memory _fileType,
        string memory _fileName,
        string memory _fileLink,
        address[] memory _whiteList,
        bytes memory _privateMetadata
    ) external nonReentrant {
        uint256 fileID = fileStorage.createMetadata(
            _fileType,
            _fileName,
            _fileLink,
            _whiteList,
            _privateMetadata,
            _msgSender()
        );

        emit CreateFile(fileID);
    }

    /**
     * @dev Get File from file ID
     * @param _fileID ID of file uploaded
     */
    function getFile(uint256 _fileID) external view returns (IFileStorage.File memory) {
        require(fileStorage.verify(_fileID, _msgSender()), "Error: UnAuthorized Users");
        return fileStorage.readMetadata(_fileID);
    }

    /**
     * @dev Update File from file ID
     * @param _fileID ID of file uploaded
     * @param _file struct of file
     */
    function updateFile(uint256 _fileID, IFileStorage.File memory _file) external onlyCreator(_fileID, _msgSender()) {
        require(_file.privateCreator == _msgSender(), "Error: Field not allow to change");
        require(_fileID == _file.id, "Error: Can not update file ID");
        fileStorage.updateMetadata(_fileID, _file);

        emit UpdateFile(_fileID);
    }

    /**
     * @dev Delete File from file ID
     * @param _fileID ID of file uploaded
     */
    function deleteFile(uint256 _fileID) external onlyCreator(_fileID, _msgSender()) {
        fileStorage.deleteMetadata(_fileID, _msgSender());

        emit DeleteFile(_fileID);
    }

    /**
     * @dev Add Authorized User
     * @param _fileID file ID
     * @param _user address of user
     */
    function addAuthorizedUser(uint256 _fileID, address _user) external onlyCreator(_fileID, _msgSender()) {
        fileStorage.addAuthorizedUser(_fileID, _user);

        emit AddAuthorizedUser(_fileID, _user);
    }

    /**
     * @dev  Remove Authorized User
     * @param _fileID file ID
     * @param _user address of user
     */
    function removeAuthorizedUser(uint256 _fileID, address _user) external onlyCreator(_fileID, _msgSender()) {
        fileStorage.removeAuthorizedUser(_fileID, _user);

        emit RemoveAuthorizedUser(_fileID, _user);
    }

    /**
     * @dev  Get all Files of caller
     */
    function getMyFiles() external view returns (IFileStorage.File[] memory) {
        return fileStorage.getMyFiles(_msgSender());
    }
}
