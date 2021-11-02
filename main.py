import configparser
import requests
import json
import base64
from base64 import b64encode
from nacl import encoding, public

config = configparser.ConfigParser()
config.read("secrets.cfg")
dockerRegistryUsername = config["secrets"]["harbor_username"]
dockerRegistryToken = config["secrets"]["harbor_token"]
repoOwner = config["github"]["repo_owner"]
repoName =config["github"]["repo_name"]
token = config["github"]["access_token"]


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def get_pk():
    url = "https://api.github.com/repos/{}/{}/actions/secrets/public-key".format(repoOwner,repoName)
    header = {"Authorization": f"token {token}"}
    response = requests.get(url,headers=header)
    return response.json().get("key"), response.json().get("key_id")

def put_request(value, keyId,secretName):
    url = "https://api.github.com/repos/{}/{}/actions/secrets/{}".format(repoOwner,repoName,secretName)
    header = {"Authorization": f"token {token}"}
    param = {"encrypted_value":value, "key_id":keyId}
    response = requests.put(url,headers=header, data=json.dumps(param))
def upload_action():
    url = "https://api.github.com/repos/{}/{}/contents/.github/workflows/FinalTest.yaml".format(repoOwner,repoName)
    header = {"Authorization": f"token {token}"}
    with open('action_raw.yaml', 'r') as file:
        data_raw = file.read()
    data_encoded_utf = data_raw.encode('utf-8')
    data_encoded64 = base64.b64encode(data_encoded_utf)
    param = {"message":"Upload Image builder action","content":data_encoded64.decode("utf-8")}
    dataJson = json.dumps(param)
    requests.put(url,headers=header,data=dataJson)

def main():
    upload_action()
    put_request(encrypt(get_pk()[0],dockerRegistryUsername),get_pk()[1],"HARBOR_USERNAME")
    put_request(encrypt(get_pk()[0],dockerRegistryToken),get_pk()[1],"HARBOR_TOKEN")

if __name__ == "__main__":
    main()