# Mutant Sampler: 

The Mutant Sampler is a collection of scripts and classes designed to load a DataFrame, sample mutants based on event types, and save the sampled data. This README provides step-by-step instructions on how to run and interact with the scripts and classes.

## Prerequisites: 
- Python 3.x
- pandas library

## Installation:
1. Clone the repository to your local machine:
   ```
   $ git clone https://github.com/ericboris/mutant-sampler.git
   ```

2. Navigate to the cloned directory:
   ```
   $ cd mutant-sampler
   ```

3. Install the required dependencies using pip:
   ```
   $ pip install -r requirements.txt
   ```

## Example Usage:
1. Navigate to the mutant-sampler directory:
   ```
   $ cd path/to/mutant-sampler
   ```

2. Run the main.py script with the following command-line arguments:
   ```
   $ python main.py --input-file-path path/to/input/file.csv --output-dir-path path/to/output/directory --output-file-name output.csv --num-samples 10
   ```

Command-line arguments:
- --input-file-path: Path to the input file containing the DataFrame as a csv.
- --output-dir-path: Path to the output directory where the sampled data will be saved.
- --output-file-name: Name of the output file to be saved.
- --num-samples: Number of samples to take for each event type.

Ensure that you provide the correct file paths and the desired number of samples.

3. The Mutant Sampler will load the DataFrame, sample the mutants, and save the sampled data in the specified output directory with the given file name.

# File Manager: 
The Mutant Sampler includes a file_manager.py class that provides functionality for loading and saving CSV files and pandas DataFrames. You can utilize this class in your own code to handle file operations.

## Example Usage: 
```
from file_manager import FileManager

# Load a DataFrame from a CSV file
df = FileManager.load_csv('path/to/file.csv')

# Save a DataFrame to a CSV file 
FileManager.save_csv(df, 'path/to/output.csv')
```

# Contributing: 
If you wish to contribute to the Mutant Sampler, please follow these steps:
1. Fork the repository on GitHub.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push them to your forked repository.
4. Submit a pull request with a detailed description of your changes.

# License: 
The Mutant Sampler is released under the MIT License.
# Contact: 

If you have any questions or suggestions regarding the Mutant Sampler, please feel free to contact us at email@example.com.
