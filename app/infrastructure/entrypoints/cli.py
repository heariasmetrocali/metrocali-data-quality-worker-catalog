import argparse
import sys

from app.domain.exceptions.catalog_exception import CatalogException
from app.infrastructure.composition_root import run_build_catalog_service


def handle_build_catalog(args: argparse.Namespace) -> int:
    try:
        result = run_build_catalog_service(
            connection_id=args.connection_id,
            user_id=args.user_id,
            alias=args.alias,
        )
    except CatalogException as error:
        print(f"ERROR: {error.message}", file=sys.stderr)
        return 1

    catalog = result.catalog
    print("Catalog built successfully")
    print(f"  id:            {catalog.id}")
    print(f"  alias:         {catalog.alias}")
    print(f"  connection_id: {catalog.connection_id}")
    print(f"  user_id:       {catalog.user_id}")
    print(f"  tables:        {len(result.tables)}")
    for table in result.tables:
        print(f"    - {table.name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MetroCali Data Quality - Worker Catalog CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_catalog = subparsers.add_parser(
        "build-catalog",
        help="Create catalog and inspect source schema (tables/columns)",
    )
    build_catalog.add_argument(
        "--connection-id",
        required=True,
        help="Connection identifier (numeric id from connections table, e.g. 1)",
    )
    build_catalog.add_argument(
        "--user-id",
        required=True,
        help="User identifier (numeric id from users table, e.g. 1)",
    )
    build_catalog.add_argument(
        "--alias",
        required=True,
        help="Catalog alias/name",
    )
    build_catalog.set_defaults(handler=handle_build_catalog)

    create_catalog = subparsers.add_parser(
        "create-catalog",
        help="Alias of build-catalog",
    )
    create_catalog.add_argument(
        "--connection-id",
        required=True,
        help="Connection identifier (numeric id from connections table, e.g. 1)",
    )
    create_catalog.add_argument(
        "--user-id",
        required=True,
        help="User identifier (numeric id from users table, e.g. 1)",
    )
    create_catalog.add_argument(
        "--alias",
        required=True,
        help="Catalog alias/name",
    )
    create_catalog.set_defaults(handler=handle_build_catalog)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
