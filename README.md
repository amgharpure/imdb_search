# IMDB Search
An API that allows the user to search top movies on IMDB by scraping and indexing data

## Setup

In the repository base folder, run:

```shell
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
flask run
```
## Example
### Request
```GET /search?search_term=steven%20crime```
### Response
```json
[
    "Minority Report",
    "Ocean's Eleven",
    "Scarface",
    "Catch Me If You Can"
]
```