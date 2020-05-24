## Basic Setup

We are using [pipenv](https://github.com/pypa/pipenv) as development workflow for Python. But if don't want it, or you have already installed boto3 globally then you can directly run the script, like
```sh
# Not recomendded but easier to start with
# Installing boto3 globally
# sudo pip3 install boto3
awsudo -u tvlk-dev -- python get_tagged_resources.py -h
```

#### Setting up pipenv
- Installing pipenv

For Ubuntu 18.04
```sh
echo 'export PATH="${HOME}/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
sudo apt install python3-pip
python3 -m pip install --user pipenv

# https://gist.github.com/planetceres/8adb62494717c71e93c96d8adad26f5c#troubleshooting-and-removal
```
For Ubuntu 20.04
```sh
sudo apt install pipenv
```
For Mac
```sh
brew install pipenv
```
- Setting up venv (by Pipenev)
```sh
pipenv install --three
# Should install boto3 also as it reads Pipfile automatically
```
- Activate venv or run directly
```sh
# activates venv on the shell
pipenv shell
# then you can run script
awsudo -u tvlk-dev -- python get_tagged_resources.py -h
# You can directly run script with
pipenv run python get_tagged_resources.py -h
```

## get_tagged_resources.py
This python script filters resources based on a tag and output it to a file in csv format.
```
# will now output all elasticache nodes with ProductDomain tag absent
awsudo -u tvlk-dev -- python get_tagged_resources.py --resource-type elasticache -file untagged_pd.csv --tag ProductDomain
# Get help printed
python get_tagged_resources.py -h
```