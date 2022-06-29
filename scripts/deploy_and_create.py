from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import ClassNFT, network, config
from web3 import Web3


def deploy_and_create():
    account = get_account()
    class_nft = ClassNFT.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(class_nft.address)
    creating_tx = class_nft.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created.")
    return class_nft, creating_tx

def deploy():
    account = get_account()
    class_nft = ClassNFT.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )

def main():
    deploy_and_create()
