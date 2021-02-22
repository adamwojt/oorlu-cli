"""Console script for oorlu_cli."""
import sys

import click
import requests

from oorlu_cli.oorlu import get_short_url
from oorlu_cli.validator import ValidationError, validate_long_url

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--limit", "-l", required=False, type=int, help="Set click limit for URL (default: no limit)")
@click.argument("long_url", required=False)
@click.pass_context
def main(ctx, long_url, limit):
    """oorlu is lightweight cli url shortener that uses https://oor.lu API.

    \b
    Example usage:
        oorlu www.verylongnastyurl.com
        oorlu www.only2clicks.com -l 2
    \b
    Long url max length: 500.
    For more information go to https://oor.lu
    """
    if long_url is None:
        return click.echo(ctx.get_help())
    try:
        validate_long_url(long_url)
    except ValidationError as e:
        raise click.BadParameter(f"`{long_url}`", param_hint="LONG_URL") from e
    if limit and limit < 0:
        raise click.BadParameter("It must be positive integer", param_hint="limit")
    try:
        res = get_short_url(long_url, limit=limit)
        short_url = res["short_url"]
    except (requests.exceptions.RequestException, KeyError) as e:
        raise click.ClickException("API / Connection error - please see if https://oor.lu works.")
    else:
        click.echo(short_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pylint: disable=no-value-for-parameter
