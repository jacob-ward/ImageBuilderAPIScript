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
from base64 import b64encode
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
        main_config = dict(config.items("github"))
        secrets_dict = dict(config.items("secrets"))
    except configparser.NoSectionError as no_section_e:
        raise ValueError("Wrong config file, no sections github or secrets") from no_section_e
    url = f"https://gitlab.stfc.ac.uk/api/v4/projects/{main_config.get('project_url')}%2F{main_config.get('project_name')}"
    header = {"PRIVATE-TOKEN":f"{main_config.get('access_token')}"}
    action_name = main_config.get("action_name")
    return secrets_dict, url, header, action_name

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
    

# def get_file_action(header: 'dict[str,str]') -> str:
#     """Gets action file form main repo

#         Args:
#             header (dict[str,str]): Header with auth token

#         Raises:
#             get_aciton_file_e: Raised when no aciton file was collected

#         Returns:
#             str: The content of the action file
#     """
#     response = requests.get("https://api.github.com/repos/vovsike/ImageBuilderAPIScript/contents/action_raw.yaml", headers=header)
#     try:
#         response.raise_for_status()
#     except HTTPError as get_aciton_file_e:
#         print("Error getting action file")
#         raise get_aciton_file_e
#     content = ast.literal_eval(response.content.decode("utf-8")).get("content")
#     return content


# def get_sha(base_url, header, action_name) -> Union[str, None]:
#     """Gets sha of the action file

#         Args:
#             base_url (str): The url to the repo
#             header (dict[str,str]): Header with auth token
#             action_name (str): The name of the action file

#         Raises:
#             get_sha_e: Raised when cant get sha

#         Returns:
#             Union[str,None]: Returns either sha or None (if file does not exist)
#     """
#     response = requests.get(base_url + f"contents/.github/workflows/{action_name}.yaml", headers=header)
#     try:
#         response.raise_for_status()
#     except HTTPError as get_sha_e:
#         print("Error geting sha of the action file")
#         return None
#     sha = response.json().get("sha")
#     return sha


# def upload_action(base_url: str, header: 'dict[str,str]', action_name: str,
#                   content: str, sha: Union[str, None]) -> None:
#     """Uploads action file to github repo

#         Args:
#             base_url (str): The url to the repo
#             header (dict[str,str]): Header with auth token
#             action_name (str): The name of the action file
#             content (str): The content of the aciton file
#             sha (Union[str, None]): Sha of the action file, needed for updating the file

#         Raises:
#             upload_action_e: Raised when no aciton been uploaded
#     """
#     if sha is not None:
#         param = {"message": "Update action file", "content": content, "sha": sha}
#     else:
#         param = {"message": "Upload action file", "content": content}
#     data_json = json.dumps(param)
#     response = requests.put(base_url + f"contents/.github/workflows/{action_name}.yaml", headers=header, data=data_json)
#     try:
#         response.raise_for_status()
#     except HTTPError as upload_action_e:
#         print("Error while uploading action")
#         raise upload_action_e


def main():
    """Main method
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path to config", type=Path)
    args = parser.parse_args()
    if args.config is not None:
        config_path = args.config  # type: Path
        try:
            secrets_dict, base_url, header, action_name = get_config(config_path)
        except (ValueError, FileNotFoundError) as config_error:
            print("Exception was caught during loading of config file, stopping")
            sys.exit(config_error)
    try:
        upload_secrets(secrets_dict, base_url, header)
    except HTTPError as http_error:
        sys.exit(http_error)
    else:
        print("Script and secrets were uploaded/updated.")

if __name__ == "__main__":
    main()
