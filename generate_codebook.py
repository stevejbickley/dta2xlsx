import pandas as pd
from pathlib import Path
import argparse


def export_stata_codebook(dta_path, output_dir=None, prefix=None):
    dta_path = Path(dta_path)

    if output_dir is None:
        output_dir = dta_path.parent
    else:
        output_dir = Path(output_dir)

    if prefix is None:
        prefix = dta_path.stem

    output_dir.mkdir(parents=True, exist_ok=True)

    reader = pd.io.stata.StataReader(dta_path)
    df = reader.read()

    var_labels = reader.variable_labels()
    value_labels = reader.value_labels()

    # ---- Long codebook ----
    rows = []
    for var in df.columns:
        var_label = var_labels.get(var, "")

        if var in value_labels:
            for val, val_label in value_labels[var].items():
                rows.append({
                    "variable": var,
                    "variable_label": var_label,
                    "value": val,
                    "value_label": val_label,
                    "dtype": str(df[var].dtype)
                })
        else:
            rows.append({
                "variable": var,
                "variable_label": var_label,
                "value": None,
                "value_label": None,
                "dtype": str(df[var].dtype)
            })

    codebook_long = pd.DataFrame(rows)
    codebook_long.to_csv(output_dir / f"{prefix}_codebook_long.csv", index=False)

    # ---- Variable summary ----
    var_rows = []
    for var in df.columns:
        var_rows.append({
            "variable": var,
            "variable_label": var_labels.get(var, ""),
            "dtype": str(df[var].dtype),
            "n_unique": df[var].nunique(dropna=True),
            "n_missing": df[var].isna().sum(),
            "has_value_labels": var in value_labels
        })

    variables_df = pd.DataFrame(var_rows)
    variables_df.to_csv(output_dir / f"{prefix}_variables.csv", index=False)

    print(f"[OK] Codebook saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate codebook from Stata .dta file")

    parser.add_argument("dta_path", help="Path to .dta file")
    parser.add_argument("--out", help="Output directory", default=None)
    parser.add_argument("--prefix", help="Filename prefix", default=None)

    args = parser.parse_args()

    export_stata_codebook(
        args.dta_path,
        output_dir=args.out,
        prefix=args.prefix
    )