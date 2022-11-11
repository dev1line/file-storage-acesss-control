const { expect } = require("chai");
const { upgrades, ethers } = require("hardhat");
const { formatBytes32String } = ethers.utils;

describe("FileStorage", () => {
    beforeEach(async () => {
        const accounts = await ethers.getSigners();
        owner = accounts[0];
        user1 = accounts[1];
        user2 = accounts[2];
        user3 = accounts[3];
        user4 = accounts[4];
        user_notWhitelisted = accounts[5];

        FileStorage = await ethers.getContractFactory("FileStorage");
        fileStorage = await upgrades.deployProxy(FileStorage, [owner.address]);
        await fileStorage.deployed();
    });

    describe("Deployment", async () => {
        it("Should returns owner of contract equal msg.sender", async () => {
            const owner_address = await fileStorage.owner();
            expect(owner.address).to.equal(owner_address);
        });

        it("Should change transfer ownership success", async () => {
            await fileStorage.transferOwnership(user1.address);
            const owner_address = await fileStorage.owner();
            expect(user1.address).to.equal(owner_address);
        });
    });

    describe("createMetadata function", async () => {
        it("Should revert when caller is not owner", async () => {
            await expect(
                fileStorage
                    .connect(user1)
                    .createMetadata(
                        "file_type",
                        "file_name",
                        "file_link",
                        [user1.address, user2.address, user3.address],
                        formatBytes32String("private_metadata"),
                        user1.address
                    )
            ).to.be.revertedWith("Ownable: caller is not the owner");

            expect(await fileStorage.getCurrentId()).to.equal(0);
        });

        it("Should create metadata success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);
        });
    });

    describe("readMetadata function", async () => {
        it("Should revert when caller is not owner", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(fileStorage.connect(user1).readMetadata(1)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );
        });

        it("Should revert when invalid ID", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(fileStorage.readMetadata(0)).to.be.revertedWith("ID: Invalid file ID");

            await expect(fileStorage.readMetadata(2)).to.be.revertedWith("ID: Invalid file ID");
        });

        it("Should read metadata success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const metadata = await fileStorage.readMetadata(1);
            expect(metadata[0]).to.equal("file_type");
            expect(metadata[1]).to.equal("file_name");
            expect(metadata[2]).to.equal("file_link");
        });
    });

    describe("updateMetadata function", async () => {
        it("Should revert when caller is not owner", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);
            const update_data = [
                "update_file_type",
                "update_file_name",
                "update_file_link",
                formatBytes32String("private_metadata"),
                user1.address,
            ];
            await expect(fileStorage.connect(user1).updateMetadata(1, update_data)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );
        });

        it("Should update metadata success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const update_data = [
                "update_file_type",
                "update_file_name",
                "update_file_link",
                formatBytes32String("private_metadata"),
                user1.address,
            ];
            await fileStorage.updateMetadata(1, update_data);
            const metadata = await fileStorage.readMetadata(1);
            expect(metadata[0]).to.equal("update_file_type");
            expect(metadata[1]).to.equal("update_file_name");
            expect(metadata[2]).to.equal("update_file_link");
        });
    });

    describe("deleteMetadata function", async () => {
        it("Should revert when caller is not owner", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(fileStorage.connect(user1).deleteMetadata(1)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );
        });

        it("Should delete metadata success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            const metadata = await fileStorage.deleteMetadata(1);
            expect(metadata[0]).to.equal(undefined);
            expect(metadata[1]).to.equal(undefined);
            expect(metadata[2]).to.equal(undefined);
        });
    });

    describe("addAuthorizedUser function", async () => {
        it("Should revert when caller is not owner", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(fileStorage.connect(user1).addAuthorizedUser(1, user4.address)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );
        });

        it("Should add Authorized User success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await fileStorage.addAuthorizedUser(1, user4.address);
            expect(await fileStorage.verify(1, user4.address)).to.equal(true);
        });
    });

    describe("removeAuthorizedUser function", async () => {
        it("Should revert when caller is not owner", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await expect(fileStorage.connect(user1).removeAuthorizedUser(1, user1.address)).to.be.revertedWith(
                "Ownable: caller is not the owner"
            );
        });

        it("Should remove Authorized User success", async () => {
            await fileStorage.createMetadata(
                "file_type",
                "file_name",
                "file_link",
                [user1.address, user2.address, user3.address],
                formatBytes32String("private_metadata"),
                user1.address
            );

            expect(await fileStorage.getCurrentId()).to.equal(1);

            await fileStorage.removeAuthorizedUser(1, user2.address);
            expect(await fileStorage.verify(1, user2.address)).to.equal(false);
        });
    });
});
