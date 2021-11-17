import configparser
from pathlib import Path, PosixPath, WindowsPath
import sys
from typing import Union
import requests
import json
import ast
import argparse
from base64 import b64encode
from nacl import encoding, public
from requests.models import HTTPError


def get_config(path_to_config: Union[PosixPath, WindowsPath]) -> tuple:
    config = configparser.ConfigParser() # type: configparser.ConfigParser
    path = Path.cwd() / path_to_config # type: Path
    if not path.is_file():
        raise FileNotFoundError(f"ConfigFileNotFound at location {path}")
    config.read(path)
    try:
        config_github = dict(config.items("github"))
        secrets_dict = dict(config.items("secrets"))
    except configparser.NoSectionError:
        raise ValueError("Wrong config file, no sections github or secrets")
    url = f"https://api.github.com/repos/{config_github.get('repo_owner')}/{config_github.get('repo_name')}/"
    header = {
        "Authorization": f"token {config_github.get('access_token')}"
        }
    action_name = config_github.get("action_name")
    return secrets_dict, url, header, action_name

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def upload_secrets(secrets: 'dict[str,str]', base_url: str, header: 'dict[str,str]') -> None:
    response = requests.get(base_url+"actionsasd/secrets/public-key",headers=header)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print("Error while getting public key")
        raise e
    public_key = response.json().get("key"), response.json().get("key_id")
    for i in secrets:
        encrypted_value = encrypt(public_key[0],secrets[i])
        data = {"encrypted_value":encrypted_value, "key_id":public_key[1]}
        response = requests.put(base_url + f"actions/secrets/{i}",headers=header, data=json.dumps(data))
        try:
            response.raise_for_status()
        except HTTPError as e:
            print("Error while uploading secrets")
            raise e

def upload_action(base_url:str,header:'dict[str,str]',action_name: str,content: str,sha: Union[str, None]) -> None:
    if sha != None:
        param = {"message":"Update action file", "content":content, "sha":sha}
    else:
        param = {"message":"Upload action file", "content":content}
    data_json = json.dumps(param)
    response = requests.put(base_url + f"contents/.github/workflows/{action_name}.yaml",headers=header,data=data_json)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print("Error while uploading action")
        raise e

def get_file_action(header: 'dict[str,str]') -> str:
    response = requests.get("https://api.github.com/repos/vovsike/ImageBuilderAPIScript/contents/action_raw.yaml", headers=header)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print("Error getting action file")
        raise e
    content = ast.literal_eval(response.content.decode("utf-8")).get("content")
    return content

def get_sha(base_url, header, action_name) -> Union[str,None]:
    response = requests.get(base_url + f"contents/.github/workflows/{action_name}.yaml", headers=header)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print("Error geting sha of the action file")
        raise e
    if response.status_code == 200 and response.json().get("type"):
        return response.json().get("sha")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path to config", type=Path)
    args = parser.parse_args()
    if args.config != None:
        config_path = args.config # type: Path
        try:
            secrets_dict, base_url, header, action_name = get_config(config_path)
        except (ValueError,FileNotFoundError) as e:
            print("Exception was caught during loading of config file, stopping")
            sys.exit(e)
    try:
        content = get_file_action(header)
        sha = get_sha(base_url,header,action_name)
        upload_action(base_url,header,action_name,content,sha)
        upload_secrets(secrets_dict, base_url,header)
    except HTTPError as e:
        sys.exit(e)
    else:
        print("Script and secrets were uploaded/updated.")


if __name__ == "__main__":
    main()