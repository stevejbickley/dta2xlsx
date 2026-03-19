# dta2xlsx

Tools to work with Stata `.dta` files:

- `dta2xlsx.py` converts Stata `.dta` files into `.csv` and/or `.xlsx`
- `generate_codebook.py` generates a full data dictionary / codebook from a Stata `.dta` file

---

## What each script does

### `dta2xlsx.py`
Use this when you want the **actual dataset converted** into a format that is easier to open in Excel or use in other tools.

It can export:

- `.csv`
- `.xlsx`

This script is for the **data itself**.

### `generate_codebook.py`
Use this when you want the **metadata / codebook** for the Stata file.

It extracts:

- variable names
- variable labels
- value labels
- variable summary information such as dtype, number of unique values, and number of missing values

This script is for the **data dictionary / codebook**, not the dataset conversion itself.

---
## Preparation
 
### Navigate to the folder

```cd ./dta2xlsx```

### Set up the poetry environment

```poetry env use path_to_pyevn_python_version```

If you are not using pyenv, just replace the above with:

```poetry env use path_to_python_interpreter```

Activate the virtual environment if needed:

```source .venv/bin/activate```

### Install/update dependencies

```poetry update```

### Running Python and Scripts:

General pattern:
```poetry run python script.py```

For example:
```poetry run python dta2xlsx.py data/myfile.dta```

---

## Using `dta2xlsx.py`

### Convert a .dta file to both CSV and Excel
```poetry run python dta2xlsx.py data/myfile.dta```

By default, if no format flags are provided, the script exports both:
- myfile.csv 
- myfile.xlsx

### Export only CSV
```poetry run python dta2xlsx.py data/myfile.dta --csv```

### Export only Excel
```poetry run python dta2xlsx.py data/myfile.dta --xlsx```

### Specify output directory and prefix
```poetry run python dta2xlsx.py data/myfile.dta --out outputs --prefix survey_2022```

This will create files such as:
- outputs/survey_2022.csv
- outputs/survey_2022.xlsx

### Optional: convert labelled Stata variables to categoricals
```poetry run python dta2xlsx.py data/myfile.dta --convert-categoricals```

Use this only if you want labelled Stata variables converted on import. Otherwise, raw coded values are preserved.

---

## Using `generate_codebook.py`

### Generate codebook outputs
```poetry run python generate_codebook.py data/myfile.dta```

### Specify output directory and prefix
```poetry run python generate_codebook.py data/myfile.dta --out outputs/codebooks --prefix survey_2022```

### Outputs from `generate_codebook.py`
#### 1. Long codebook
`*_codebook_long.csv`

Contains one row per variable/value label combination.

Example columns:
- variable 
- variable_label 
- value 
- value_label 
- dtype

#### 2. Variable summary

`*_variables.csv`

Contains one row per variable.

Example columns:
- variable 
- variable_label 
- dtype 
- n_unique 
- n_missing 
- has_value_labels

---

## Example workflow

### Convert data and generate a codebook

Run:
```poetry run python dta2xlsx.py data/myfile.dta```

Followed by:
```poetry run python generate_codebook.py data/myfile.dta```

This gives you:
- the converted dataset (.csv / .xlsx)
- the associated codebook / data dictionary (_codebook_long.csv and _variables.csv)

---
## Creating your own poetry environment

### Create new poetry project (if required):
```poetry new dta2xlsx```

### Initialize the existing directory (if required):
```poetry init```

### Add a new package:
```poetry add package-name```

