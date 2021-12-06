# Installation
To install this package from PyPi using pip just run `pip install image-builder-deployer`. If you want to build from source from GitRepo please follow [this](#build-from-source)

## Supported versions
To build and rus this package you will need to use python >=3.6

## <a name = "build-from-source"> </a> Build from source
To build this python package you will need to have python `build` and `venv` installed as a package. To do this please run `python -m pip install build`. To build image-builder-deployer navigate to root directory of this repo and run `python -m build`. When build finfishes new directory will appear under the name `dist`

### How to install
To install package after building from source simply run `python -m pip install dist/image_builder_deployer<version>.tag.gz>`

## Configuration
Before using this script it needs a configuration file, the template for this file can be found in `config/config_template`. Simply fill in the template file and store it somewhere in your system.
### Generate
This script can generate a config file for you. To do this run `python -m image_builder_deployer -g <path_where_config_will_be_saved>` to start config generation procedure. Enter data when prompted. <b>Attention secret values are masked</b>.

## How to run this package
To run use `python -m image_builder_deployer <remote Github or Girlab> <path_to_your_config_file>` and it should just work.

## Troubleshooting
### Config file loading
- `ConfigFileNotFound` this error will occur if the config file location that is provided as an argument as not found. To overcome this error check that config file exist at the location specified. Please be aware that the path to the config file should be relative to where you run the script from
- `WrongConfigFile` this error will occur if the config file format is different to the template one. If this error occurs please check that your config file follows same structure as template, you can also try to [generate](#generate) config file.
- `GetPublicKey` this error will occur if scritp can't retrive public key from github. This is ussualy becuase access key provided lucks such permissions. Permissions needed are `admin:public_key read`
- `GetActionFile` this error will occur if action file is no available, if this happends, please check that you have provided correct github token. If the token is up-to-date and correct please contact the owner of this repo.
- `ShaError` this error will occur of no sha was retrived from the action file. This can happen when first time uploading an action as the repo will not contain any action files. If this happens during the update of an action please check that github token is valid and correct.
- `UploadAction` this error will occur of uploading of the action failed. This is ussualy the permission error. Please check that GitHub token is correct and up-to-date.