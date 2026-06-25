import argparse
import sys

from app.domain.exceptions.catalog_exception import CatalogException
from app.infrastructure.composition_root import run_create_catalog_use_case


def handle_create_catalog(args: argparse.Namespace) -> int:
    try:
        print (f"[INFRA.CLI] (handle_create_catalog), payload = [ args={args}]")

        catalog = run_create_catalog_use_case(
            connection_id=args.connection_id,
            user_id=args.user_id,
            alias=args.alias,
        )
    except CatalogException as error:
        print(f"ERROR: {error.message}", file=sys.stderr)
        return 1

    print("Catalog created successfully")
    print(f"  id:            {catalog.id}")
    print(f"  alias:         {catalog.alias}")
    print(f"  connection_id: {catalog.connection_id}")
    print(f"  user_id:       {catalog.user_id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MetroCali Data Quality - Worker Catalog CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_catalog = subparsers.add_parser(
        "create-catalog",
        help="Create a new catalog snapshot",
    )
    create_catalog.add_argument(
        "--connection-id",
        required=True,
        help="Connection identifier (numeric id from connections table, e.g. 1)",
    )
    create_catalog.add_argument(
        "--user-id",
        required=True,
        help="User identifier (e.g. user-1, user-2)",
    )
    create_catalog.add_argument(
        "--alias",
        required=True,
        help="Catalog alias/name",
    )

    create_catalog.set_defaults(handler=handle_create_catalog)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
