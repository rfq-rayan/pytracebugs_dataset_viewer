from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv
import sys
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Increase CSV field limit to handle large code snippets
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Directory where CSVs are located
CSV_DIR = app.config['CSV_DIR']

# Error types for filtering
ERROR_TYPES = app.config['ERROR_TYPES']

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
    diff_mode = request.args.get('diff_mode', 'diff')  # Default to diff mode

    if not selected_csv:
        return "No CSV files found"

    rows = read_csv_rows(selected_csv)
    if not rows:
        return f"No data found in {selected_csv}"

    # Get all available columns
    all_columns = list(rows[0].keys()) if rows else []

    # Reorder columns: pair before_merge with after_merge, full_file_code_before_merge with full_file_code_after_merge, etc.
    reordered_columns = []
    other_cols = [col for col in all_columns if 'merge' not in col.lower()]
    
    # Get all merge-related columns
    merge_cols = [col for col in all_columns if 'merge' in col.lower()]
    
    # Group merge columns by their base name (before/after pairs)
    merge_pairs = {}
    for col in merge_cols:
        if 'before_merge' in col.lower():
            # Extract the base name (e.g., 'full_file_code' from 'full_file_code_before_merge')
            base_name = col.replace('_before_merge', '')
            if base_name not in merge_pairs:
                merge_pairs[base_name] = {'before': None, 'after': None}
            merge_pairs[base_name]['before'] = col
        elif 'after_merge' in col.lower():
            # Extract the base name (e.g., 'full_file_code' from 'full_file_code_after_merge')
            base_name = col.replace('_after_merge', '')
            if base_name not in merge_pairs:
                merge_pairs[base_name] = {'before': None, 'after': None}
            merge_pairs[base_name]['after'] = col
    
    # Add other columns first
    reordered_columns.extend(other_cols)
    
    # Add merge pairs side by side
    for base_name, pair in merge_pairs.items():
        if pair['before']:
            reordered_columns.append(pair['before'])
        if pair['after']:
            reordered_columns.append(pair['after']) 

    # If no columns are selected, pre-select before_merge and after_merge columns
    if not selected_columns:
        # Only select columns that are exactly named 'before_merge' and 'after_merge'
        exact_merge_cols = []
        if 'before_merge' in all_columns:
            exact_merge_cols.append('before_merge')
        if 'after_merge' in all_columns:
            exact_merge_cols.append('after_merge')
        
        # Add traceback_type at the beginning if it exists
        if 'traceback_type' in all_columns:
            selected_columns = ['traceback_type'] + exact_merge_cols
        else:
            selected_columns = exact_merge_cols

    # If no error type is selected and traceback_type is in selected columns, default to TypeError
    if not selected_error_type and 'traceback_type' in selected_columns:
        selected_error_type = 'TypeError'

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
        total_rows=len(rows),
        diff_mode=diff_mode
    )

if __name__ == '__main__':
    app.run(debug=True) 