# drawtf

Draw diagrams from tf state files. You can add a bunch of options and also suppliment it wil config files etc.

NOTE: Azure support only for now.

## Features

### flags

```bash 
python drawtf.py --name Aggreko IPG Application (Dev) |
        --state ./tests/test/sample.tfstate |
        --json-config-path ./tests/test/config.json |
        --output-path ./tests/test/sample |
        --verbose
```

```json
{
    "links": [
        { 
            "from": "apim-exp-product-app-dev-azurerm_api_management", 
            "to": "kv-product-app-dev-azurerm_key_vault",
            "color": "darkgreen",
            "type": "dashed",
            "label": "Write only"
        }
    ]
}
```


### TODO

- [ ] Azure: SQL (MSSQL, MySQL, etc)
- [ ] Azure: Data engineering resources
- [ ] Other clouds

## Credits

This package was created with Cookiecutter and the audreyr/cookiecutter-pypackage project template.

* Cookiecutter: https://github.com/audreyr/cookiecutter
* audreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
