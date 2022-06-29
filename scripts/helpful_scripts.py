from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache-local",
    "mainnet-fork-dev",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
STUDENT_MAPPING = {
    0: "AAKASH",
    1: "JONPAUL",
    2: "COHEN",
    3: "OAK",
    4: "JOHN",
    5: "EMELIO",
    6: "LUCAS",
    7: "KARYSSA",
    8: "NOAH",
    9: "LARA",
    10: "YAQING",
    11: "BELLE",
    12: "MATTEO",
    13: "JOHAN",
    14: "NATHAN",
    15: "KEVIN",
    16: "RYAN",
    17: "STEPHANIE",
    18: "DALUCHI",
    19: "ADAM",
    20: "AIDEN",
    21: "MATTHIAS",
    22: "MSKEDDY_SPECIAL",
}


def get_student(student_number):
    return STUDENT_MAPPING[student_number]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx
