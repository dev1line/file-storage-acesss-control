// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

interface IFileStorage {
    struct File {
        uint256 id;
        string fileType;
        string fileName;
        string fileLink;
        bytes privateMetadata;
        address privateCreator;
    }

    function createMetadata(
        string memory _fileType,
        string memory _fileName,
        string memory _fileLink,
        address[] memory _whiteList,
        bytes memory _privateMetadata,
        address _privateCreator
    ) external returns (uint256);

    function readMetadata(uint256 _fileID) external view returns (File memory);

    function updateMetadata(uint256 _fileID, File memory _newFile) external;

    function deleteMetadata(uint256 _fileID, address _user) external;

    function addAuthorizedUser(uint256 _fileID, address _user) external;

    function removeAuthorizedUser(uint256 _fileID, address _user) external;

    function verify(uint256 _fileID, address _caller) external view returns (bool);

    function getMyFiles(address _caller) external view returns (File[] memory);

    function getAuthorizedUsersOf(uint256 _fileID) external view returns (address[] memory);

    function getCurrentId() external view returns (uint256);
}
