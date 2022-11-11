const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");
const { ethers } = require("hardhat");
const { BigNumber } = require("ethers");
const { provider } = ethers;
const { AddressZero: ADDRESS_ZERO, MaxUint256: MAX_UINT256 } = ethers.constants;

function BN(value) {
  return BigNumber.from(value.toString());
}

const skipTime = async seconds => {
  await network.provider.send("evm_increaseTime", [seconds]);
  await network.provider.send("evm_mine");
};

const getCurrentTime = async () => {
  const blockNumber = await hre.ethers.provider.getBlockNumber();
  const block = await hre.ethers.provider.getBlock(blockNumber);
  return block.timestamp;
};

const generateMerkleTree = accounts => {
  const leaves = accounts.map(value => keccak256(value));
  return new MerkleTree(leaves, keccak256, { sort: true });
};

const generateLeaf = account => {
  return keccak256(account);
};

module.exports = {
  provider,
  BN,
  ADDRESS_ZERO,
  MAX_UINT256,
  skipTime,
  getCurrentTime,
  generateMerkleTree,
  generateLeaf
};
