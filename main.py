import click
import json
from transmission_rpc import Client


@click.group()
@click.option('--host', prompt=True, help="fqdn of transmission server")
@click.option('--port', prompt=True, help="port of transmission server")
@click.option('--username', prompt=True, help="api username")
@click.option('--password', prompt=True, hide_input=True, help="api user password")
@click.option('--protocol', type=click.Choice(['http', 'https'], case_sensitive=True), prompt=True)
@click.pass_context
def cli(ctx, **kwargs):
    """
    Transmission helper cli

    Provides some aid where the native cli falls short
    """
    ctx.obj = kwargs


@cli.command()
@click.pass_context
def show_torrents(ctx):
    """
    Lists all torrents
    """
    client = Client(**ctx.obj)
    torrents = client.get_torrents()
    print(json.dumps([
        torrent.fields
        for torrent in torrents
    ]))


@cli.command()
@click.argument('torrent_id', type=click.INT)
@click.pass_context
def show_torrent(ctx, torrent_id):
    """
    Show information about specific torrent
    """
    client = Client(**ctx.obj)
    torrent = client.get_torrent(torrent_id)
    print(json.dumps(torrent.fields))


@cli.command()
@click.option('--delete-data/--no-delete-data', default=False)
@click.argument('torrent_ids')
@click.pass_context
def delete_torrent(ctx, delete_data, torrent_ids):
    """
    Delete a list of torrent ids, optionally also removing the data
    """
    client = Client(**ctx.obj)
    ids = [int(_id) for _id in torrent_ids.split(',')]
    client.remove_torrent(ids=ids, delete_data=delete_data)


@cli.command(epilog="See https://github.com/trim21/transmission-rpc/blob/8cd8c22353adf85795a62687044526c5537fa516/transmission_rpc/client.py#L611")
@click.argument('torrent_ids')
@click.argument('attribute_key', type=click.STRING)
@click.argument('attribute_value', type=click.INT)
@click.pass_context
def change_torrent(ctx, torrent_ids, attribute_key, attribute_value):
    """
    Updates a list of torrent ids, for now limited to value of type int
    """
    client = Client(**ctx.obj)
    ids = [int(_id) for _id in torrent_ids.split(',')]
    client.change_torrent(**{"ids": ids, attribute_key: attribute_value})


if __name__ == '__main__':
    cli(auto_envvar_prefix='TR_CLI', max_content_width=256)
