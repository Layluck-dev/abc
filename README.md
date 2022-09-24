# Welcome

To the ABC (Avans BlockChain) repo.

# Setup your Python virtual environments
Create a new Python virtual environment: `python -m venv _env`  
## Switch to the new Python virtual environment:
Mac OS / Linux: `source _env/bin/activate`  
Windows: `_env\Scripts\activate`  
  
Check if the new Python virtual environment is active `pip -V`  
Upgrade pip in the virtual environment: `pip install --upgrade pip`  
Install the needed dependencies: `pip install -r requirements.txt`  
Add to requirements.txt: `pip freeze > requirements.txt`  
  
For more information see [this page](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

# Run Flask 
To run the server locally: `flask --app blockchain --debug run`  
also rename the file folder to 'blockchain' to prevent import issues :^)

# OPDR 1-2
- Why are timestamps important?  
Because a timestamp is used to generate a hash. Therefore if the timetsamp is tempered with, the hash and by extension the blockchain will be rendered inavild.  
Ensuring the legitimacy of transactions.