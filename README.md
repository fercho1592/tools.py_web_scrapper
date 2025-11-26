## Installation

    pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r Requirements.txt

Also, you need to download a test driver for your browser, in this case it will be for Chrome. In case you want to use another browser you can change selenium implementation

## Configurations
The program use a file `config.ini` for all secrets and setups at root directory level

    [General]
    debug = True
    log_level = info

    [MangaStrategy]
    e_manga_domain = url_page
    tmh_manga_domain = url_page
    {... add other web implementations}

    [AzureServiceBus]
    connection_string = primary_conection_string

    [TelegramBot]
    token = telegram-token

## Virtual env
Action |CMD
-------|--------
Create env| `python3 -m venv .venv`
Activate|`source ./.venv/bin/activate`
Deactivate|`deactivate`

# Project execution
## Use download queue file implementation
### Requirements
Use a file on your project root folder named `download-queue.txt` to create a queue to downloads you mangas 


Each line in the file is a download, it have to has the url (index or first page), the name of the folder that is going to be download and the page number to start download separates by "|" element

### Running

    py src

## Use Azure Service Bus Implementation
### Requirements
Add the following params in config.ini file

    [AzureServiceBus]
    connection_string = {azureConnectionString}
    queue_name = {queueName}

### Running

    py src/azure_service_bus_trigger


## Common errors 

- https://medium.com/@yen.hoang.1904/resolve-issue-ssl-certificate-verify-failed-when-trying-to-open-an-url-with-python-on-macos-46d868b44e10