import os
import pandas as pd

class FileManager:
    @staticmethod
    def load(file: str) -> pd.DataFrame:
        """
        Loads a CSV file and returns its contents as a pandas DataFrame.

        Parameters:
        - file (str): The path to the CSV file to be loaded.

        Returns:
        - pandas.DataFrame: The contents of the CSV file as a DataFrame.
        """
        return pd.read_csv(file)

    @staticmethod
    def save(contents: pd.DataFrame, directory: str, file_name: str) -> None:
        """
        Saves the contents of a pandas DataFrame to a CSV file.

        Parameters:
        - contents (pandas.DataFrame): The DataFrame to be saved.
        - directory (str): The directory where the file should be saved.
        - file_name (str): The name of the file.

        Returns:
        - None
        """
        file_path = os.path.join(directory, file_name)
        contents.to_csv(file_path, index=False)

