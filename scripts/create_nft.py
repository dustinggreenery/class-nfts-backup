from turtle import update
from scripts.deploy_and_create import deploy
from scripts.create_collectible import create_collectible
from scripts.create_metadata import create_metadata
from scripts.set_tokenuri import set_token_uri
import time
import yaml
import json
import os
import shutil


def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def update_front_end():
    copy_folders_to_front_end("./build", "./front_end/src/chain-info")

    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front End Updated")


def create_nft(front_end_update=False):
    deploy()
    create_collectible()
    time.sleep(180)
    create_metadata()
    if front_end_update:
        update_front_end()


def main():
    # create_nft()
    set_token_uri()
