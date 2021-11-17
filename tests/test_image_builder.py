import pytest
import pathlib
from image_builder_deployer.deploy_script import get_config, get_file_action

def test_config_returns_correct_values():
    path = pathlib.Path.cwd() / 'tests' / 'data' / 'test_config.ini'
    secrets_dict, base_url, header, action_name = get_config(path)
    assert secrets_dict == {"harbor_username":"TestHarborUsername","harbor_token":"TestHarborToken"}
    assert base_url == "https://api.github.com/repos/TestRepoOwner/TestRepoName/"
    assert header == {"Authorization": "token TestAccessToken"}
    assert action_name == "TestActionName"

def test_config_throws_FileNotFoundError_exception():
    path = pathlib.Path.cwd() /'wrong_path'/ 'tests' / 'data' / 'test_config.ini'
    with pytest.raises(FileNotFoundError):
        get_config(path)

def test_config_throws_ValueError_exception():
    path = pathlib.Path.cwd() / 'tests' / 'data' / 'bad_test_config.ini'
    with pytest.raises(ValueError):
        get_config(path)

def test_get_file_action():
    header = {}
    test_var = get_file_action(header)
    print (test_var)