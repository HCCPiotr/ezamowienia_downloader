# The problem?

https://ezamowienia.gov.pl doesnt have a "download all attachments" button

# The solution?

a simple script that does exactly that

```
usage: ez_dl [-h] [-o OUTPUT] id

https://ezamowienia.gov.pl downloader

positional arguments:
  id                   The tender id

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output path. Defaults to ./{tender_id}
```
