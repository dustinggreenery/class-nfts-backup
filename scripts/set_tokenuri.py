from brownie import network, ClassNFT
from scripts.helpful_scripts import OPENSEA_URL, get_student, get_account

student_metadata_dic = {
    "AAKASH": "https://ipfs.io/ipfs/QmYSvbiixc2w3N3cXmegaDmEFhKcPF2rY4ZLU7GkyEoiYf?filename=0-AAKASH.json",
    "JONPAUL": "",
    "COHEN": "",
    "OAK": "",
    "JOHN": "",
    "EMELIO": "",
    "LUCAS": "",
    "KARYSSA": "",
    "NOAH": "",
    "LARA": "https://ipfs.io/ipfs/QmZixzMZJfYXjBekuhQ7xoYiQurfJsPGNPHAhuPduq45iW?filename=0-LARA.jsons",
    "YAQING": "",
    "BELLE": "",
    "MATTEO": "",
    "JOHAN": "",
    "NATHAN": "",
    "KEVIN": "",
    "RYAN": "",
    "STEPHANIE": "",
    "DALUCHI": "",
    "ADAM": "",
    "AIDEN": "",
    "MATTHIAS": "",
    "MSKEDDY_SPECIAL": "",
}


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"You can now view NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("May take up to 20 minutes, make sure to hit the refresh metadata button")


def set_token_uri():
    print(f"Working on {network.show_active()}")
    class_nft = ClassNFT[-1]
    number_of_collectibles = class_nft.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        student = get_student(class_nft.tokenIdToStudent(token_id))
        if not class_nft.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, class_nft, student_metadata_dic[student])


def main():
    set_token_uri()
