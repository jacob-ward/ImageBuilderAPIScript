"""This script uploads image builder action to the desired github repo
    As well as uploading the most recent verion of the script it alos
    uploads secrets that are needed to run the script.
"""
import configparser
from pathlib import Path, PosixPath, WindowsPath
import sys
from typing import Union
import json
import ast
import argparse
import base64
from nacl import encoding, public
import requests
from requests.models import HTTPError


def get_config(path_to_config: Union[PosixPath, WindowsPath]) -> tuple:
    """Function to get config file and retrive data that is needed
        for the script to run

            Args:
                path_to_config (Union[PosixPath, WindowsPath]): relative path to the
                config file

            Raises:
                FileNotFoundError: Raised if config file does not exist
                ValueError: Raised if config file is of wrong format

            Returns:
                tuple: data that is used throughout the script
    """
    config = configparser.ConfigParser()  # type: configparser.ConfigParser
    path = Path.cwd() / path_to_config  # type: Path
    if not path.is_file():
        raise FileNotFoundError(f"ConfigFileNotFound at location {path}")
    config.read(path)
    try:
        main_config = dict(config.items("main"))
        secrets_dict = dict(config.items("secrets"))
        github_tocken=config.get("github","access_token")
    except configparser.NoSectionError as no_section_e:
        raise ValueError("Wrong config file, no sections github or secrets") from no_section_e
    url = f"https://gitlab.stfc.ac.uk/api/v4/projects/{main_config.get('project_url')}%2F{main_config.get('project_name')}"
    header = {"PRIVATE-TOKEN":f"{main_config.get('access_token')}"}
    action_name = main_config.get("action_name")
    return secrets_dict, url, header, action_name, github_tocken

def upload_secrets(secrets: 'dict[str,str]', base_url: str, header: 'dict[str, str]') -> None:
    """Uploads encrypted secret to github repo

        Args:
            secrets (dict[str,str]): Secret to be uploaded
            base_url (str): The url to the repo
            header (dict[str,str]): Header with auth token

        Raises:
            no_secret_found: Raised when no secret was found in the repo
            secret_upload_e: Raised when no secret was uplaoded
    """
    for i in secrets:
        response = requests.get(base_url+f"/variables/{i}",headers=header)
        data = {"key":i, "value":secrets[i]}
        try:
            response.raise_for_status()
        except HTTPError as no_secret_found:
            response = requests.post(base_url+"/variables",headers=header,data=data)
        else:
            response = requests.put(base_url+f"/variables/{i}",headers=header,data=data)
    try:
        response.raise_for_status()
    except HTTPError as secret_upload_e:
        print("Error while uploading secrets")
        raise secret_upload_e

def get_file_action(github_token: str) -> str:
    """Gets action file form main repo

        Args:
            header (dict[str,str]): Header with auth token

        Raises:
            get_aciton_file_e: Raised when no aciton file was collected

        Returns:
            str: The content of the action file
    """
    header = {
        "Authorization": f"token {github_token}"}
    #TODO
    #! CHANGE TO MAIN BRANCH AFTER WHEN FINSIEHD TESTING
    #TODO
    response = requests.get("https://api.github.com/repos/vovsike/ImageBuilderAPIScript/contents/.gitlab-ci.yml?ref=support_gitlab", headers=header)
    try:
        response.raise_for_status()
    except HTTPError as get_aciton_file_e:
        print("Error getting action file")
        raise get_aciton_file_e
    content = ast.literal_eval(response.content.decode("utf-8")).get("content")
    return base64.b64decode(content)


def upload_action(base_url: str, header: 'dict[str,str]', content: str, action_name: str) -> None:
    """Uploads action file to github repo

        Args:
            base_url (str): The url to the repo
            header (dict[str,str]): Header with auth token
            content (str): The content of the aciton file
            action_name (str): The name of the action file
        Raises:
            upload_action_e: Raised when no aciton been uploaded
    """
    data = {"commit_message": "Update CI file", "content": content,"branch":"master"}
    response = requests.post(base_url + f"/repository/files/%2E{action_name}%2Eyml", headers=header, data=data)
    try:
        response.raise_for_status()
    except HTTPError as upload_action_e:
        print("Error while uploading action")
        raise upload_action_e


def main():
    """Main method
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path to config", type=Path)
    args = parser.parse_args()
    if args.config is not None:
        config_path = args.config  # type: Path
        try:
            secrets_dict, base_url, header, action_name, github_token = get_config(config_path)
        except (ValueError, FileNotFoundError) as config_error:
            print("Exception was caught during loading of config file, stopping")
            sys.exit(config_error)
    try:
        content = get_file_action(github_token)
        upload_action(base_url,header,content,action_name)
        upload_secrets(secrets_dict, base_url, header)
    except HTTPError as http_error:
        sys.exit(http_error)
    else:
        print("Script and secrets were uploaded/updated.")

if __name__ == "__main__":
    main()
