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
This script can generate a config file for you. To do this run `python -m image_builder_deployer -g` to start config generation procedure. After that follow enter data when prompted. Attention secret values are masked.

## How to run this package
To run use `python -m image_builder_deployer <remote Github or Girlab> <path_to_your_config_file>` and it should just work.

## Troubleshooting
TODO