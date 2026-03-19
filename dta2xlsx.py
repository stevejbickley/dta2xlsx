import pandas as pd
from pathlib import Path
import argparse


def convert_dta(
    dta_path,
    output_dir=None,
    prefix=None,
    to_csv=True,
    to_xlsx=True,
    convert_categoricals=False
):
    """
    Convert a Stata .dta file to .csv and/or .xlsx.

    Parameters
    ----------
    dta_path : str or Path
        Path to the .dta file.
    output_dir : str or Path, optional
        Output directory. Defaults to the same folder as the input file.
    prefix : str, optional
        Prefix for output filenames. Defaults to the input filename stem.
    to_csv : bool, default True
        Whether to export CSV.
    to_xlsx : bool, default True
        Whether to export Excel.
    convert_categoricals : bool, default False
        Whether to convert labelled Stata variables to pandas categoricals
        when reading. Keep False if you want raw coded values preserved.
    """

    dta_path = Path(dta_path)

    if not dta_path.exists():
        raise FileNotFoundError(f"Input file not found: {dta_path}")

    if output_dir is None:
        output_dir = dta_path.parent
    else:
        output_dir = Path(output_dir)

    if prefix is None:
        prefix = dta_path.stem

    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_stata(dta_path, convert_categoricals=convert_categoricals)

    output_paths = {}

    if to_csv:
        csv_path = output_dir / f"{prefix}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        output_paths["csv"] = csv_path
        print(f"[OK] CSV saved to: {csv_path}")

    if to_xlsx:
        xlsx_path = output_dir / f"{prefix}.xlsx"
        df.to_excel(xlsx_path, index=False)
        output_paths["xlsx"] = xlsx_path
        print(f"[OK] Excel saved to: {xlsx_path}")

    if not to_csv and not to_xlsx:
        print("[WARN] No output selected. Use --csv and/or --xlsx.")

    return df, output_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a Stata .dta file to .csv and/or .xlsx"
    )

    parser.add_argument("dta_path", help="Path to .dta file")
    parser.add_argument("--out", help="Output directory", default=None)
    parser.add_argument("--prefix", help="Filename prefix", default=None)

    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export CSV"
    )
    parser.add_argument(
        "--xlsx",
        action="store_true",
        help="Export Excel (.xlsx)"
    )
    parser.add_argument(
        "--convert-categoricals",
        action="store_true",
        help="Convert labelled Stata variables to pandas categoricals on read"
    )

    args = parser.parse_args()

    # If neither flag is supplied, export both by default
    to_csv = args.csv
    to_xlsx = args.xlsx
    if not to_csv and not to_xlsx:
        to_csv = True
        to_xlsx = True

    convert_dta(
        args.dta_path,
        output_dir=args.out,
        prefix=args.prefix,
        to_csv=to_csv,
        to_xlsx=to_xlsx,
        convert_categoricals=args.convert_categoricals
    )