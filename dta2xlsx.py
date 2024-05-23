
#### 1) Import the required packages and define functions

import pandas as pd
import pyreadstat
import re
import os
#os.getcwd() # check current working directory

# Experimental for xlsx export option - doesn't work yet..
#import openpyxl
#del openpyxl # Remove the module reference

# Function to extract filename without extension
def extract_filename(filepath):
    # Regular expression to match the filename without extension
    pattern = r'([^/]+)(?=\.[^.]+$)'
    match = re.search(pattern, filepath)
    if match:
        return match.group(1)
    else:
        return None

# Function to flatten value labels dictionary
def flatten_value_labels(value_labels_dict, column_names):
    flattened_labels = []
    for name in column_names:
        if name in value_labels_dict:
            label_dict = value_labels_dict[name]
            if isinstance(label_dict, dict):
                flattened_label = ', '.join(f'{k}: {v}' for k, v in label_dict.items())
            else:
                flattened_label = str(label_dict)
        else:
            flattened_label = ""
        flattened_labels.append(flattened_label)
    return flattened_labels

# Function to split value labels string correctly
def split_value_labels(value_labels_str):
    #pattern = re.compile(r',\s(?!(?:[^()]*\([^()]*\))*[^()]*\))') # Regular expression to split on commas not within parentheses
    pattern = re.compile(r',\s(?=-?\d+:)') # Regular expression to split on commas followed by a space, a number, and a colon
    return pattern.split(value_labels_str)

#### 2) Define the file name to convert
filename = "/Users/stevenbickley/stevejbickley/Integrated_values_surveys_1981-2021.dta"

#### 3) Read in the stata file and convert to xlsx and/or csv format
# Read Stata file
data_df, meta = pyreadstat.read_dta(filename)

# Extract variable labels
variable_labels = meta.column_labels

# Replace dataframe column names with variable labels
data_df.columns = variable_labels

# Display first few rows of the dataframe to verify
print(data_df.head())

# Write to CSV (optional)
data_df.to_csv(str(extract_filename(filename)) + ".csv", index=False, encoding='utf-8')

# Write to Excel - NOTE: this code is not working for some reason...
#data_df.to_excel(str(extract_filename(filename)) + ".xlsx", index=False)

# Explanation
# variable_labels = meta.column_labels: Directly assigns the list of variable labels to variable_labels.
# df.columns = variable_labels: Sets the DataFrame's column names to the variable labels from the meta object.

#### 4) Exploring the 'meta' object
# Print the metadata attributes
print(dir(meta))

# Print the variable labels
print(meta.column_labels)
#len(meta.column_labels) # 840

# Print the variable names
print(meta.column_names)
#len(meta.column_names) # 840

# Print the value labels (if any)
print(meta.value_labels)
#len(meta.value_labels) # 806

# Print the variable value labels (if any)
print(meta.variable_value_labels)
#len(meta.variable_value_labels) # 821

#### 5) Exporting the 'meta' object to csv

# Assign to global variable names
column_labels = meta.column_labels
column_names = meta.column_names
value_labels = meta.value_labels
variable_value_labels = meta.variable_value_labels
original_variable_types = meta.original_variable_types
readstat_variable_types = meta.readstat_variable_types
variable_alignment = meta.variable_alignment
variable_measure = meta.variable_measure
variable_to_label = meta.variable_to_label

# Ensure lengths match by padding with None or trimming to the shortest length
max_length = max(len(column_labels), len(column_names), len(value_labels), len(variable_value_labels),
                 len(original_variable_types), len(readstat_variable_types), len(variable_alignment),
                 len(variable_measure), len(variable_to_label))
column_labels += [None] * (max_length - len(column_labels))
column_names += [None] * (max_length - len(column_names))

# Flatten value labels dictionary for DataFrame creation
value_labels_flattened = flatten_value_labels(value_labels, column_names)
variable_value_labels_flattened = flatten_value_labels(variable_value_labels, column_names)
original_variable_types_flattened = flatten_value_labels(original_variable_types, column_names)
readstat_variable_types_flattened = flatten_value_labels(readstat_variable_types, column_names)
variable_alignment_flattened = flatten_value_labels(variable_alignment, column_names)
variable_measure_flattened = flatten_value_labels(variable_measure, column_names)
variable_to_label_flattened = flatten_value_labels(variable_to_label, column_names)

# Pad the value labels list to ensure it matches the length of the other lists
value_labels_flattened += [""] * (max_length - len(value_labels_flattened))
variable_value_labels_flattened += [""] * (max_length - len(variable_value_labels_flattened))
original_variable_types_flattened += [""] * (max_length - len(original_variable_types_flattened))
readstat_variable_types_flattened += [""] * (max_length - len(readstat_variable_types_flattened))
variable_alignment_flattened += [""] * (max_length - len(variable_alignment_flattened))
variable_measure_flattened += [""] * (max_length - len(variable_measure_flattened))
variable_to_label_flattened += [""] * (max_length - len(variable_to_label_flattened))

# Create DataFrame with appropriate lengths
meta_df = pd.DataFrame({
    "Column Labels": column_labels[:max_length],
    "Column Names": column_names[:max_length],
    "Value Labels": value_labels_flattened[:max_length],
    "Variable Value Labels": variable_value_labels_flattened[:max_length],
    "Original Variable Types": original_variable_types_flattened[:max_length],
    "Readstat Variable Types": readstat_variable_types_flattened[:max_length],
    "Variable Alignment": variable_alignment_flattened[:max_length],
    "Variable Measure": variable_measure_flattened[:max_length],
    "Variable to Label": variable_to_label_flattened[:max_length]
})

# Write to CSV (Optional)
meta_df.to_csv(str(extract_filename(filename)) + "_metadata.csv", index=False, encoding='utf-8')

# Write to Excel - NOTE: this code is not working for some reason...
#data_df.to_excel(str(extract_filename(filename)) + "_metadata.xlsx", index=False)

# Iterate through meta_df to process each variable with value labels
for index, row in meta_df.iterrows():
    column_label = row['Column Labels']
    column_name = row['Column Names']
    value_labels_str = row['Value Labels']
    if pd.notna(value_labels_str):  # Check if value labels column is not empty
        # Convert the value labels string to a dictionary
        value_labels_list = split_value_labels(value_labels_str) #value_labels_str.split(', ')
        value_labels_dict = {}
        for item in value_labels_list:
            if ': ' in item:
                key, value = item.split(': ', 1)
                try:
                    value_labels_dict[int(key)] = value.strip()
                except ValueError:
                    value_labels_dict[key] = value.strip()
        # Check if the column exists in data_df
        if column_label in data_df.columns:
            # Replace the coded values in the corresponding column of data_df
            try:
                data_df[column_label] = data_df[column_label].astype(int)  # Ensure the column is of type int
            except ValueError:
                pass  # Column cannot be converted to int, skip this step
            data_df[column_label] = data_df[column_label].replace(value_labels_dict)
        else:
            print(f"Column '{column_label}' not found in data_df")

# Display the first few rows of the cleaned data_df to verify the replacements
print(data_df.head())
# https://medium.com/analytics-vidhya/how-to-summarize-data-with-pandas-2c9edffafbaf
# For example: .info(), .describe(), .value_counts(), .nunique(), .sum(), ...

# Write to CSV (optional)
data_df.to_csv(str(extract_filename(filename)) + "_decoded.csv", index=False, encoding='utf-8')

# Write to Excel - NOTE: this code is not working for some reason...
#data_df.to_excel(str(extract_filename(filename)) + ".xlsx", index=False)