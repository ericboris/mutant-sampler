import pandas as pd
from typing import Dict, Tuple

class MutantSampler:
    @staticmethod
    def create_method_id(df: pd.DataFrame) -> pd.Series:
        """
        Creates a method ID column by combining package, class, and method columns.

        Args:
            df: A DataFrame containing 'package', 'class', and 'method' columns.

        Returns:
            A Series containing the method ID for each row in the DataFrame.
        """
        return df['package'] + '.' + df['class'] + '.' + df['method']

    @staticmethod
    def add_method_id_column(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'method_id' column to the DataFrame.

        Args:
            df: A DataFrame.

        Returns:
            The DataFrame with an additional 'method_id' column.
        """
        df['method_id'] = MutantSampler.create_method_id(df)
        return df

    @staticmethod
    def shuffle_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Shuffles the DataFrame.

        Args:
            df: A DataFrame.

        Returns:
            The DataFrame shuffled.
        """
        return df.sample(frac=1).reset_index(drop=True)

    @staticmethod
    def add_row_to_sampled_data(row: pd.Series, sampled_data: pd.DataFrame, event_type_counts: Dict[str, int], k: int) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Adds a row to the sampled data if it meets the conditions.

        Args:
            row: A row from the DataFrame.
            sampled_data: The DataFrame containing the sampled data.
            event_type_counts: A dictionary containing event types as keys and their counts as values.
            k: The number of mutant IDs to sample from each event type.

        Returns:
            The sampled_data and event_type_counts updated.
        """
        # Check if the method_id of the current row already exists in the sampled data.
        # If it does, we skip this row to ensure the uniqueness of method_ids in the sampled data.
        if (sampled_data['method_id'] == row['method_id']).any():
            return sampled_data, event_type_counts

        # Check if the count of the current row's event type in the sampled data is less than k.
        # If it is, we add this row to the sampled data and increment the count of this event type.
        if event_type_counts[row['eventType']] < k:
            sampled_data = pd.concat([sampled_data, row.to_frame().T])
            event_type_counts[row['eventType']] += 1

        return sampled_data, event_type_counts

    @staticmethod
    def all_event_types_sampled(event_type_counts: Dict[str, int], k: int) -> bool:
        """
        Checks if all event types have been sampled k times.
        Args:

            event_type_counts: A dictionary containing event types as keys and their counts as values.
            k: The number of mutant IDs to sample from each event type.

        Returns:
            True if all event types have been sampled k times, False otherwise.
        """
        return all(count >= k for count in event_type_counts.values())

    @staticmethod
    def get_sampled_data(df: pd.DataFrame, k: int) -> pd.DataFrame:
        """
        Performs sampling of mutant IDs from the DataFrame and returns the sampled data.

        Args:
            df: A DataFrame.
            k: The number of mutant IDs to sample from each event type.

        Returns:
            The DataFrame containing the sampled data.
        """
        # We add a 'method_id' column to the DataFrame to identify unique methods.
        df = MutantSampler.add_method_id_column(df)

        # Shuffling the DataFrame ensures that our sampling is random.
        df = MutantSampler.shuffle_dataframe(df)

        # Initialize the counts of all event types to 0.
        event_type_counts = {et: 0 for et in df['eventType'].unique()}
        
        # Initialize an empty DataFrame for storing the sampled data.
        sampled_data = pd.DataFrame(columns=df.columns)

        # Iterate over each row in the shuffled DataFrame.
        for _, row in df.iterrows():
            # Attempt to add the current row to the sampled data.
            sampled_data, event_type_counts = MutantSampler.add_row_to_sampled_data(row, sampled_data, event_type_counts, k)

            # If we have sampled k mutant IDs for all event types, we can stop sampling.
            if MutantSampler.all_event_types_sampled(event_type_counts, k):
                break

        # Sort the sampled data by mutantId before returning.
        sampled_data = sampled_data.sort_values(by='mutantId')
        return sampled_data
