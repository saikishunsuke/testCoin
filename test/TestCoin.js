const { BN, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');
const TestCoin = artifacts.require('./TestCoin.sol');
const { expect } = require('chai');

contract('TestCoin', accounts => {
  sender = accounts[0];
  receiver = accounts[1];
  before(async () => {
    testCoin = await TestCoin.deployed();
  })

  it('should put 100TCIN after deploy', async () => {
    let balance = testCoin.balanceOf(sender);
    expect(await testCoin.balanceOf(sender)).to.be.bignumber.equal(
      new BN(100)
    )
  });
})
