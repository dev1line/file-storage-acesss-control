const { expect } = require("chai");
const { upgrades, ethers } = require("hardhat");
const { formatBytes32String } = ethers.utils;
const { BN } = require("./utils");
describe("AccessControl", () => {
    beforeEach(async () => {
        const accounts = await ethers.getSigners();
        owner = accounts[0];
        user1 = accounts[1];
        user2 = accounts[2];
        user3 = accounts[3];
        user4 = accounts[4];
        user_notWhitelisted = accounts[5];

        FileStorage = await ethers.getContractFactory("FileStorage");
        AccessControl = await ethers.getContractFactory("AccessControl");

        accessControl = await upgrades.deployProxy(AccessControl, []);
        await accessControl.deployed();

        fileStorage = await upgrades.deployProxy(FileStorage, [accessControl.address]);
        await fileStorage.deployed();

        // initial fileStorage
        await accessControl.setFileStorage(fileStorage.address);
    });

    describe("Deployment", async () => {
        it("Should returns owner of contract equal msg.sender", async () => {
            const owner_address = await fileStorage.owner();
            expect(accessControl.address).to.equal(owner_address);
        });

        it("Should change transfer ownership success", async () => {
            await accessControl.transferOwnership(user1.address);
            const owner_address = await accessControl.owner();
            expect(user1.address).to.equal(owner_address);
        });
    });

    describe("setFileStorage function", async () => {
        it("Should revert when caller is not owner", async () => {
            await expect(accessControl.connect(user1).setFileStorage(user_notWhitelisted.address)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );

            expect(await fileStorage.getCurrentId()).to.equal(0);
        });

        it("Should set fileStorage success", async () => {
            await accessControl.setFileStorage(user_notWhitelisted.address);

            expect(await accessControl.fileStorage()).to.equal(user_notWhitelisted.address);
        });
    });

    describe("createFile function", async () => {
        it("Should create metadata success", async () => {
            await accessControl
                .connect(user1)
                .createFile(
                    "file_type",
                    "file_name",
                    "file_link",
                    [user1.address, user2.address, user3.address],
                    formatBytes32String("private_metadata")
                );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const metadata = await accessControl.connect(user1).getFile(1);

            expect(metadata[0]).to.equal(BN(1));
            expect(metadata[1]).to.equal("file_type");
            expect(metadata[2]).to.equal("file_name");
            expect(metadata[3]).to.equal("file_link");
        });
    });

    describe("getFile function", async () => {
        it("Should revert when caller is not authorized users", async () => {
            await accessControl
                .connect(user1)
                .createFile(
                    "file_type",
                    "file_name",
                    "file_link",
                    [user1.address, user2.address, user3.address],
                    formatBytes32String("private_metadata")
                );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(accessControl.connect(user_notWhitelisted).getFile(1)).to.be.revertedWith(
                "Error: UnAuthorized Users"
            );
        });

        it("Should get metadata success", async () => {
            await accessControl
                .connect(user1)
                .createFile(
                    "file_type",
                    "file_name",
                    "file_link",
                    [user1.address, user2.address, user3.address],
                    formatBytes32String("private_metadata")
                );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const metadata = await accessControl.connect(user1).getFile(1);
            expect(metadata[0]).to.equal(BN(1));
            expect(metadata[1]).to.equal("file_type");
            expect(metadata[2]).to.equal("file_name");
            expect(metadata[3]).to.equal("file_link");
        });
    });

    describe("updateFile function", async () => {
        it("Should revert when caller is not creator", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);
            const update_data = [
                1,
                "update_file_type",
                "update_file_name",
                "update_file_link",
                formatBytes32String("private_metadata"),
                owner.address,
            ];

            await expect(accessControl.connect(user1).updateFile(1, update_data)).to.be.revertedWith(
                "Ownable: Invalid creator"
            );
        });

        it("Should revert when change private_creator field", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);
            const update_data = [
                1,
                "update_file_type",
                "update_file_name",
                "update_file_link",
                formatBytes32String("private_metadata"),
                user_notWhitelisted.address,
            ];
            await expect(accessControl.updateFile(1, update_data)).to.be.revertedWith(
                "Error: Field not allow to change"
            );
        });

        it("Should update metadata success", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const update_data = [
                1,
                "update_file_type",
                "update_file_name",
                "update_file_link",
                formatBytes32String("private_metadata"),
                owner.address,
            ];
            await accessControl.updateFile(1, update_data);
            const metadata = await accessControl.connect(user1).getFile(1);
            expect(metadata[0]).to.equal(BN(1));
            expect(metadata[1]).to.equal("update_file_type");
            expect(metadata[2]).to.equal("update_file_name");
            expect(metadata[3]).to.equal("update_file_link");
        });
    });

    describe("deleteFile function", async () => {
        it("Should revert when caller is not creator", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(accessControl.connect(user1).deleteFile(1)).to.be.revertedWith("Ownable: Invalid creator");
        });

        it("Should delete metadata success", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const metadata = await accessControl.deleteFile(1);
            expect(metadata[0]).to.equal(undefined);
            expect(metadata[1]).to.equal(undefined);
            expect(metadata[2]).to.equal(undefined);
        });
    });

    describe("addAuthorizedUser function", async () => {
        it("Should revert when caller is not owner", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(accessControl.connect(user2).addAuthorizedUser(1, user4.address)).to.be.revertedWith(
                "Ownable: Invalid creator"
            );
        });

        it("Should add Authorized User success", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await accessControl.addAuthorizedUser(1, user4.address);
            const metadata = await accessControl.connect(user4).getFile(1);
            expect(metadata[0]).to.equal(BN(1));
            expect(metadata[1]).to.equal("file_type");
            expect(metadata[2]).to.equal("file_name");
            expect(metadata[3]).to.equal("file_link");
        });
    });

    describe("removeAuthorizedUser function", async () => {
        it("Should revert when caller is not owner", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(accessControl.connect(user2).removeAuthorizedUser(1, user1.address)).to.be.revertedWith(
                "Ownable: Invalid creator"
            );
        });

        it("Should remove Authorized User success", async () => {
            await accessControl.createFile(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata")
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await accessControl.removeAuthorizedUser(1, user1.address);

            await expect(accessControl.connect(user1).getFile(1)).to.be.revertedWith("Error: UnAuthorized Users");
        });
    });
});
