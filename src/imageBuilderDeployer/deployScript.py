import configparser
import os
import sys
import requests
import json
import base64
import ast
from base64 import b64encode
from nacl import encoding, public


def get_config(path_to_config):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), path_to_config))
    config_github = dict(config.items("github"))
    url = f"https://api.github.com/repos/{config_github.get('repo_owner')}/{config_github.get('repo_name')}/"
    header = {
        "Authorization": f"token {config_github.get('access_token')}"
        }
    action_name = config_github.get("action_name")
    secrets_dict = dict(config.items("secrets"))
    return secrets_dict, url, header, action_name

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def upload_secrets(secrets, base_url, header):
    response = requests.get(base_url+"actions/secrets/public-key",headers=header)
    public_key = response.json().get("key"), response.json().get("key_id")
    for i in secrets:
        encrypted_value = encrypt(public_key[0],secrets[i])
        data = {"encrypted_value":encrypted_value, "key_id":public_key[1]}
        response = requests.put(base_url + f"actions/secrets/{i}",headers=header, data=json.dumps(data))

def upload_action(base_url,header,action_name,content,sha):
    if sha != None:
        param = {"message":"Update action file", "content":content, "sha":sha}
    else:
        param = {"message":"Upload action file", "content":content}
    data_json = json.dumps(param)
    response = requests.put(base_url + f"contents/.github/workflows/{action_name}.yaml",headers=header,data=data_json)
    return response

def get_file_action(header):
    response = requests.get("https://api.github.com/repos/vovsike/ImageBuilderAPIScript/contents/action_raw.yaml", headers=header)
    content = ast.literal_eval(response.content.decode("utf-8")).get("content")
    return content

def get_sha(base_url, header, action_name):
    response = requests.get(base_url + f"contents/.github/workflows/{action_name}.yaml", headers=header)
    if response.status_code == 200 and response.json().get("type"):
        return response.json().get("sha")

def main():
    if len(sys.argv) < 2:
        print("Usage python -m imageBuilderDeployer <configfile>")
        sys.exit(1)
    else:
        config_path = sys.argv[-1]
    secrets_dict, base_url, header, action_name = get_config(config_path)
    content = get_file_action(header)
    sha = get_sha(base_url,header,action_name)
    upload_action(base_url,header,action_name,content,sha)
    upload_secrets(secrets_dict, base_url,header)


if __name__ == "__main__":
    main()