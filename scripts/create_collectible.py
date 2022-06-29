from brownie import ClassNFT
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def create_collectible():
    account = get_account()
    class_nft = ClassNFT[-1]
    fund_with_link(class_nft.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = class_nft.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")


def main():
    create_collectible()
