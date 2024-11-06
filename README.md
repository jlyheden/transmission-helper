# transmission-helper

Seemingly meaningless CLI for interacting with Transmission - the headless torrent daemon. The CLI was built to address some of the shortcomings of the native CLI. Specifically:

* Outputs json, native CLI only prints in human-readable format that is cumbersome to parse with scripts.
* Ability to modify properties on existing torrents.

## Usage

```commandline
$ python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Transmission helper cli

  Provides some aid where the native cli falls short

Options:
  --host TEXT              fqdn of transmission server
  --port TEXT              port of transmission server
  --username TEXT          api username
  --password TEXT          api user password
  --protocol [http|https]
  --help                   Show this message and exit.

Commands:
  change-torrent  Updates a list of torrent ids, for now limited to value of type int
  delete-torrent  Delete a list of torrent ids, optionally also removing the data
  show-torrent    Show information about specific torrent
  show-torrents   Lists all torrents
```

Typical example of parameterising the cli and securing the password through env var:

```commandline
$ export TR_CLI_PASSWORD="***"
$ python main.py \
    --host my-ip \
    --port 9091 \
    --username myuser \
    --protocol http \
    show-torrent 123 | jq
{
  "activityDate": xxxxx,
  "addedDate": yyyyy,
  "bandwidthPriority": zzzz,
....
```

All options can be set using environment variables by prefixing with TR_CLI like `TR_CLI_USERNAME`, `TR_CLI_HOST` and so on.
