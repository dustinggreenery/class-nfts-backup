from venv import create
from scripts.helpful_scripts import get_student
from metadata.sample_metadata import metadata_template
from brownie import ClassNFT, network
from pathlib import Path
import requests
import json
import os

# Props to Lara to becoming the first nft. Noah is runner-up, and Nathan is third.
student_to_image_uri = {
    "AAKASH": "https://ipfs.io/ipfs/QmSG8uBu1yU4xTup3Vrj2b7uDW9zPJH6EXuWACf8BKWsJG?filename=aakash.png",
    "JONPAUL": "",
    "COHEN": "",
    "OAK": "",
    "JOHN": "",
    "EMELIO": "",
    "LUCAS": "",
    "KARYSSA": "",
    "NOAH": "",
    "LARA": "",
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

student_to_attribute = {
    "AAKASH": "PC Power",
    "JONPAUL": "Monke",
    "COHEN": "Linus Tech Tips",
    "OAK": "Tree",
    "JOHN": "American",
    "EMELIO": "Emelio Birdcall",
    "LUCAS": "Terraria Gamer",
    "KARYSSA": "Theatre Person",
    "NOAH": "Turtle Lover",
    "LARA": "Anti Singing Horses",
    "YAQING": "Presentation Dogs",
    "BELLE": "Ur Mom",
    "MATTEO": "Comrade",
    "JOHAN": "Joham",
    "NATHAN": "Sus",
    "KEVIN": "Koolade Addict",
    "RYAN": "Famous Youtuber",
    "STEPHANIE": "Book Reader",
    "DALUCHI": "Falling of Chairs",
    "ADAM": "A Beaver Dam",
    "AIDEN": "Rubix Cuber",
    "MATTHIAS": "Father Lucien",
    "MSKEDDY_SPECIAL": "Afternoon Attendance",
}


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        PINATA_BASE_URL = "https://api.pinata.cloud/"
        endpoint = "pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
        }
        filename = filepath.split("/")[-1:][0]
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def create_metadata():
    class_nft = ClassNFT[-1]
    number_of_class_nft = class_nft.tokenCounter()
    print(f"{number_of_class_nft} collectibles have been created.")
    for token_id in range(number_of_class_nft):
        student = get_student(class_nft.tokenIdToStudent(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{student}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists.")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = student
            collectible_metadata[
                "description"
            ] = f"{student} in the Grade 8 Gifted Program in St. Mark!"
            collectible_metadata["attributes"] = [
                {"trait_type": student_to_attribute[student], "value": 100}
            ]
            image_path = "./img/" + student.lower() + ".png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else student_to_image_uri[student]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def main():
    create_metadata()
