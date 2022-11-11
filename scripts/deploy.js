const hre = require("hardhat");
const fs = require("fs");
const ethers = hre.ethers;
const upgrades = hre.upgrades;
async function main() {
  //Loading accounts
  const accounts = await ethers.getSigners();
  const addresses = accounts.map(item => item.address);
  const owner = addresses[0];

  // Loading contract factory.
  const FileStorage = await ethers.getContractFactory("FileStorage");
  const AccessControl = await ethers.getContractFactory("AccessControl");
  // Deploy contracts
  console.log(
    "========================================================================================="
  );
  console.log("DEPLOY CONTRACTS");
  console.log(
    "========================================================================================="
  );

  const accessControl = await upgrades.deployProxy(AccessControl, []);
  await accessControl.deployed();

  console.log("accessControl deployed in:", accessControl.address);
  console.log(
    "========================================================================================="
  );

  const fileStorage = await upgrades.deployProxy(FileStorage, [
    accessControl.address
  ]);
  await fileStorage.deployed();
  console.log("fileStorage deployed in:", fileStorage.address);
  console.log(
    "========================================================================================="
  );
  console.log(
    "========================================================================================="
  );
  console.log("VERIFY CONTRACTS");
  console.log(
    "========================================================================================="
  );

  const accessControlVerify = await upgrades.erc1967.getImplementationAddress(
    accessControl.address
  );
  console.log("accessControlVerify deployed in:", accessControlVerify);
  console.log(
    "========================================================================================="
  );

  const contractAddresses = {
    fileStorage: fileStorage.address,
    accessControl: accessControl.address
  };
  console.log("contract Address:", contractAddresses);
  await fs.writeFileSync("contracts.json", JSON.stringify(contractAddresses));

  const contractAddresses_verify = {
    accessControl: accessControlVerify
  };

  await fs.writeFileSync(
    "contracts-verify.json",
    JSON.stringify(contractAddresses_verify)
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
