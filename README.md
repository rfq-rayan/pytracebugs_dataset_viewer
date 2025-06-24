# Dataset Viewer

Simple web app to view our pytracebugs dataset better.

I already have created the csv file, `bugfixes_train_sampled_1000.csv` from the `bugfixes_train.pickle` file in the `buggy_dataset` folder which is not included in this repository, can be downloaded from the [pytracebugs](https://github.com/acheshkov/pytracebugs) repository.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rfq-rayan/pytracebugs_dataset_viewer.git
   ```
2. **Go to the repository**
   ```bash
   cd pytracebugs_dataset_viewer
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. Navigate to `http://localhost:5000`

## Usage

### Basic Navigation
- Select a CSV file from the dropdown
- Choose which columns to display using the `checkboxes`
- Adjust the number of rows to display
- Use the "Update View" button to apply changes


### Filtering
- Use the error type dropdown to filter data by specific error types
- This feature is only available when the `traceback_type` column is selected

### Default Settings

When you first visit the application, the following settings are automatically configured:

**Pre-selected Columns:**
- `traceback_type` (if available in the dataset)
- `before_merge` (if available in the dataset)
- `after_merge` (if available in the dataset)

**Default Filters:**
- **Error Type**: `TypeError` (only shows TypeError errors by default)
- **Display Mode**: Diff highlighting enabled (shows visual differences between before/after code)
- **Max Rows**: 10 rows displayed

**Column Ordering:**
- Merge-related columns are automatically paired and displayed side by side
- `before_merge` and `after_merge` columns are grouped together
- Other merge pairs (like `full_file_code_before_merge` and `full_file_code_after_merge`) are also paired
- Non-merge columns appear first in the table

These defaults provide an optimal viewing experience for analyzing code changes and error patterns in the dataset.

## File Structure

```
dataset_viewer/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── static/              # Static assets
│   ├── style.css        # CSS styles
│   ├── script.js        # JavaScript functionality
│   └── highlight-init.js # Syntax highlighting initialization
├── templates/           # HTML templates
│   └── csv_viewer.html  # Main template
└── *.csv               # Your CSV data files
```

