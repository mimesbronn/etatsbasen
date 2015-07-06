# Etatsbasen

Verktøy til å eksportere fra https://github.com/mimesbronn/etatsbasen-data
Lager import som er egnet for import til alaveteli.

## Installasjon

```sh
$ git clone https://github.com/mimesbronn/etatsbasen.git
$ cd etatsbasen
$ sudo npm install -g
$ git clone https://github.com/mimesbronn/etatsbasen-data.git
$ cd etatsbasen-data
$ etatsbasen
```

## Opsjoner (python)

Opsjoner skal ikke være nødvendig. Den har default verdier som er egnet for Mimes brønn.

```
$ ./etatsbasen.py -h
usage: etatsbasen.py [-h] [-c all | -c 12 -c 14 -c ...] [-f file]
                     [-u headerName1 -u ...] [-v]

Tool for exporting etatsbasen-data to a file that can be imported into
alaveteli.

optional arguments:
  -h, --help            show this help message and exit
  -c all | -c 12 -c 14 -c ...
                        Categories to include (default: "all")
  -f file               File to read from (default: "etatsbasen.csv")
  -u headerName1 -u ...
                        Columns and order of columns to output (default: id,re
                        quest_email,name,name.nn,name.en,tag_string,home_page)
  -v                    Print version (python-etatsbasen-v0.1) and exit
```

## Opsjoner (javascript)

Opsjoner skal ikke være nødvendig. Den har default verdier som er egnet for Mimes brønn.
Dokumentasjonen på opsjonene under er utdatert.

```sh
$ etatsbasen -h
 Usage: etatsbasen [options]

  -c [all|[c1,c2,..]]   Categories to include (defaults: `12,14,17,18,27,33,38,66,68,76`)
  -f [file]             File to read from (defaults: `etatsbasen.csv`)
  -o h1[,h2,h3]         Include only these headers in output (id or name)
  -v                    Print version.
  -h                    Write this help.
```
