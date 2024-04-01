# Development Notes

# Setting up the environment

## Creating environment

```
python3 -m venv env #Creates the environment (first time only)
source env/bin/activate
deactivate
```

### Installing Qt

```
pip install pyside6
```

### Other Packages

* python-dotenv
* requests

# API Key

Get the API key through the Pokemon TCG API developer portal and place the following .env file within the root directory:

```
APIKEY=KEY
```