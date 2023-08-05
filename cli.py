#!/usr/bin/python3
import argparse
import pathlib
import requests
from python_freeipa import ClientMeta
import python_freeipa.exceptions
from src.utils.logger import idm_logger
import sys

logger = idm_logger('IdM-Manager-Main')
def run_archive(client:ClientMeta, args) -> None:
    pathlib.Path.mkdir(args.dest, exist_ok=True)
    logger.info(f"Archiving {args.domain} objects to the {str(args.dest).split('/')[-1]} directory.")

def run_import(client:ClientMeta, args) -> None:
    logger.info(f"Importing objects from {args.path} to the {str(args.domain).split('/')[-1]} domain")

def cli() -> argparse.Namespace:
    """

    The CLI function is returns a CLI Parser object that runs archive and imports of the program.

    """
    parser = argparse.ArgumentParser(

        prog='FreeIPA/IdM Manager',
        description='CLI Interface for Creating and \
                    Importing FreeIPA Domain Objects',
        exit_on_error=True,
        add_help=True,
        usage='%(prog)s [options]'

    )
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-D','--domain',type=str, required=True, help='FreeIPA Hostname',)
    parent_parser.add_argument('-U','--username', type=str, required=True, help='FreeIPA Username',)
    parent_parser.add_argument('-P','--password',type=str, required=True, help='FreeIPA Password',)
    parent_parser.add_argument('--verify-ssl',action="store_true", default=False, help='Verify SSL')

    import_parser = subparsers.add_parser(name='import', help='Import Command', parents=[parent_parser])
    import_parser.add_argument('-p', '--path', type=lambda p: pathlib.Path(p).absolute(), required=True, help='Manifest directory path')
    import_parser.set_defaults(func=run_import)

    archive_parser = subparsers.add_parser(name='archive', help='Archive Command', parents=[parent_parser])
    archive_parser.add_argument('-d', '--dest',type=lambda p:pathlib.Path(p).absolute(), required=True, help='Manifest directory path')
    archive_parser.set_defaults(func=run_archive)
    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = cli()

        if args.verify_ssl:
            client = ClientMeta(host=args.domain,verify_ssl=True, dns_discovery=True)
        else:
            client = ClientMeta(host=args.domain,verify_ssl=False, dns_discovery=True)

        client.login(username=args.username, password=args.password)
        app = args.func(client,args)

    except (python_freeipa.exceptions.Unauthorized, requests.exceptions.ConnectionError) as e:
        logger.error(f"Authentication to {args.domain} failed! Exiting Program...")
        logger.error(e)
        sys.exit()
