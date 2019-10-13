const TestCoin = artifacts.require('TestCoin');

module.exports = function(deployer, network, accounts){
  const admin = accounts[0];

  return deployer
    .deploy(TestCoin, 100, { from: admin })
    .then(function() {
      console.log(`admin address: ${admin}`);
    });
};
