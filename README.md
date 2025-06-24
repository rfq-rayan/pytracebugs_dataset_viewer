# Buggy Code Dataset Viewer

A simple web-based tool to visualize and explore buggy code snippets from the PyTraceBugs dataset. This tool displays before/after merge code snippets side by side with syntax highlighting and diff visualization.

## Features

- **Side-by-side code comparison**: View before and after merge code snippets
- **Diff highlighting**: Color-coded differences (red=deleted, green=added, yellow=modified)
- **Syntax highlighting**: Dark theme with line numbers
- **Error type filtering**: Filter by specific error types
- **Copy functionality**: Easy copy buttons for code sections
- **Responsive design**: Works on different screen sizes

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download** this repository
2. **Navigate** to the project directory:
   ```bash
   cd dataset_viewer
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## What to Expect

### Main Interface
- **CSV File Selector**: Choose from available dataset files
- **Column Selection**: Select which data columns to display
- **Error Type Filter**: Filter by specific error types (if available)
- **Display Mode**: Toggle between normal view and diff highlighting
- **Row Limit**: Control how many rows to display

### Code Display
- **Dark theme**: Easy on the eyes for code reading
- **Line numbers**: Helps track specific lines
- **Copy buttons**: Hover over code cells to see copy buttons
- **Diff mode**: Shows color-coded changes between before/after versions

### Dataset Files
The tool includes several CSV files with different sample sizes:
- `bugfixes_train_sampled_100.csv` - 100 sample entries
- `bugfixes_train_sampled_1000.csv` - 1000 sample entries
- `bugfixes_train.pickle` - Full training dataset
- `bugfixes_test.pickle` - Test dataset
- `bugfixes_valid.pickle` - Validation dataset

## Usage Tips

1. **Start with smaller files** (100 or 1000 samples) to get familiar with the interface
2. **Use diff mode** to easily spot changes between before/after code
3. **Filter by error types** to focus on specific bug categories
4. **Copy code sections** for further analysis or documentation

## Technical Details

- **Backend**: Flask web framework
- **Frontend**: HTML/CSS/JavaScript with Highlight.js for syntax highlighting
- **Data**: CSV and pickle files containing buggy code snippets
- **Port**: Runs on localhost:5000 by default

## Troubleshooting

- **Port already in use**: Change the port in `app.py` or kill the existing process
- **Missing dependencies**: Ensure all packages in `requirements.txt` are installed
- **File not found**: Check that CSV files are in the `buggy_dataset/` directory

## Dataset Source

This tool works with the PyTraceBugs dataset, which contains real-world Python bug fixes from open-source projects. The dataset includes code snippets before and after bug fixes, along with metadata about the types of errors.

---

*This is a utility tool for exploring and understanding buggy code patterns as part of a larger research project.* 