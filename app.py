from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import sys

# Increase CSV field limit to handle large code snippets
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

app = Flask(__name__)

# Directory where CSVs are located
CSV_DIR = '.'
# Directory where code files are located
CODE_DIR = os.path.join('buggy_dataset', 'buggy_snippets_files')

# Error types for filtering
ERROR_TYPES = [
    'AttributeError', 'TypeError', 'ValueError', 'KeyError', 'IndexError', 'AssertionError', 'RuntimeError', 'Exception',
    'ImportError', 'FileNotFoundError', 'OSError', 'UnicodeDecodeError', 'NotImplementedError', 'ModuleNotFoundError',
    'OperationalError', 'UnboundLocalError', 'IOError', 'subprocess.CalledProcessError', 'UnicodeEncodeError', 'NameError',
    'RecursionError', 'ZeroDivisionError', 'PermissionError', 'dvc.exceptions.RemoteCacheRequiredError',
    'botocore.exceptions.ClientError', 'sqlite3.OperationalError', 'pydantic.error_wrappers.ValidationError',
    'bleak.exc.BleakError', 'ConnectionResetError', 'SystemError', 'SyntaxError', 'BrokenPipeError',
    'json.decoder.JSONDecodeError', 'sphinx.errors.SphinxWarning'
]

# Helper to list CSV files in root
def list_csv_files():
    return [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

# Helper to read CSV rows
def read_csv_rows(csv_filename):
    rows = []
    with open(os.path.join(CSV_DIR, csv_filename), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean each cell value
            cleaned_row = {}
            for key, value in row.items():
                if value:
                    # Strip whitespace and normalize newlines
                    cleaned_value = value.strip().replace('\r\n', '\n').replace('\r', '\n')
                    cleaned_row[key] = cleaned_value
                else:
                    cleaned_row[key] = value
            rows.append(cleaned_row)
    return rows

@app.route('/')
def index():
    # Redirect to the main CSV viewer page
    return redirect(url_for('csv_viewer'))

@app.route('/csv')
def csv_viewer():
    csv_files = list_csv_files()
    selected_csv = request.args.get('csv', csv_files[0] if csv_files else '')
    selected_columns = request.args.getlist('columns')
    max_rows = int(request.args.get('max_rows', 10))
    selected_error_type = request.args.get('error_type', '')

    if not selected_csv:
        return "No CSV files found"

    rows = read_csv_rows(selected_csv)
    if not rows:
        return f"No data found in {selected_csv}"

    # Get all available columns
    all_columns = list(rows[0].keys()) if rows else []

    # Reorder columns: before_merge should come before after_merge
    reordered_columns = []
    before_merge_cols = [col for col in all_columns if 'before_merge' in col.lower()]
    after_merge_cols = [col for col in all_columns if 'after_merge' in col.lower()]
    other_cols = [col for col in all_columns if 'merge' not in col.lower()]
    
    # Add columns in order: other columns, before_merge, after_merge
    reordered_columns.extend(other_cols)
    reordered_columns.extend(before_merge_cols)
    reordered_columns.extend(after_merge_cols)

    # If 'traceback_type' is selected and error_type is chosen, filter rows
    if 'traceback_type' in selected_columns and selected_error_type:
        rows = [row for row in rows if row.get('traceback_type', '') == selected_error_type]

    # Create display rows with original indices
    display_rows_with_indices = []
    for i, row in enumerate(rows[:max_rows]):
        display_rows_with_indices.append({
            'row': row,
            'original_index': i
        })

    return render_template(
        'csv_viewer.html',
        csv_files=csv_files,
        selected_csv=selected_csv,
        selected_columns=selected_columns,
        all_columns=reordered_columns,  # Use reordered columns
        max_rows=max_rows,
        selected_error_type=selected_error_type,
        error_types=ERROR_TYPES,
        display_rows_with_indices=display_rows_with_indices,
        total_rows=len(rows)
    )

if __name__ == '__main__':
    app.run(debug=True) 