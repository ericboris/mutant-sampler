import pandas as pd
import random
from typing import Dict, Any, Set, List, Tuple

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
    def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops duplicate rows from the DataFrame based on 'method_id', 'eventType', and 'mutantId' columns.

        Args:
            df: A DataFrame.

        Returns:
            The DataFrame with duplicate rows removed.
        """
        return df.drop_duplicates(subset=['method_id', 'eventType', 'mutantId'])

    @staticmethod
    def populate_mutant_dict(df: pd.DataFrame) -> Dict[str, List[Any]]:
        """
        Populates a dictionary with event types as keys and a list of mutant IDs as values.

        Args:
            df: A DataFrame.

        Returns:
            A dictionary with event types as keys and corresponding mutant IDs as values.
        """
        mutant_dict = {}
        for _, row in df.iterrows():
            mutant_dict = MutantSampler.add_to_dict(row, mutant_dict)
        return mutant_dict

    @staticmethod
    def add_to_dict(row: pd.Series, mutant_dict: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """
        Adds a mutant ID to the mutant_dict based on the event type.

        Args:
            row: A row of the DataFrame.
            mutant_dict: A dictionary containing event types as keys and mutant IDs as values.

        Returns:
            The mutant_dict with the new mutant ID added.
        """
        if row['eventType'] not in mutant_dict:
            mutant_dict[row['eventType']] = []
        mutant_dict[row['eventType']].append(row['mutantId'])
        return mutant_dict   

    @staticmethod
    def sort_event_types(mutant_dict: Dict[str, List[Any]]) -> List[str]:
        """
        Sorts the event types based on the number of mutant IDs.

        Args:
            mutant_dict: A dictionary containing event types as keys and mutant IDs as values.

        Returns:
            A list of event types sorted by the number of mutant IDs.
        """
        return sorted(mutant_dict, key=lambda x: len(mutant_dict[x]))

    @staticmethod
    def sample_from_event_type(
        df: pd.DataFrame,
        mutant_dict: Dict[str, List[Any]],
        event_type: str,
        k: int,
        sampled_data: pd.DataFrame,
        sampled_mutants: Set[str]
    ) -> Tuple[pd.DataFrame, Set[str]]:
        """
        Samples k mutant IDs from the given event type and adds them to the sampled data.

        Args:
            df: A DataFrame.
            mutant_dict: A dictionary containing event types as keys and mutant IDs as values.
            event_type: The event type to sample from.
            k: The number of mutant IDs to sample.
            sampled_data: The DataFrame containing the sampled data.
            sampled_mutants: A set containing already sampled method IDs.

        Returns:
            The updated sampled_data and sampled_mutants.
        """
        sample_size = min(k, len(mutant_dict[event_type]))
        sampled_mutant_ids = random.sample(mutant_dict[event_type], sample_size)
        for mutant_id in sampled_mutant_ids:
            sampled_data, sampled_mutants = MutantSampler.add_sample_to_data(
                df, mutant_id, sampled_data, sampled_mutants
            )
        return sampled_data, sampled_mutants

    @staticmethod
    def determine_method_id(df: pd.DataFrame, mutant_id: Any) -> str:
        """
        Determines the method ID for a given mutant ID.

        Args:
            df: A DataFrame.
            mutant_id: A mutant ID.

        Returns:
            The method ID corresponding to the mutant ID.
        """
        return df[df['mutantId'] == mutant_id]['method_id'].values[0]

    @staticmethod
    def add_sample_to_data(
        df: pd.DataFrame,
        mutant_id: Any,
        sampled_data: pd.DataFrame,
        sampled_mutants: Set[str]
    ) -> Tuple[pd.DataFrame, Set[str]]:
        """
        Adds a sample (row) from the DataFrame for the given mutant ID to the sampled data.

        Args:
            df: A DataFrame.
            mutant_id: A mutant ID.
            sampled_data: The DataFrame containing the sampled data.
            sampled_mutants: A set containing already sampled method IDs.

        Returns:
            The updated sampled_data and sampled_mutants.
        """
        method_id = MutantSampler.determine_method_id(df, mutant_id)
        if method_id not in sampled_mutants:
            sampled_mutants.add(method_id)
            sampled_data = pd.concat([sampled_data, df[df['mutantId'] == mutant_id]])
        return sampled_data, sampled_mutants

    @staticmethod
    def get_sampled_data_from_types(
        df: pd.DataFrame,
        mutant_dict: Dict[str, List[Any]],
        sorted_event_types: List[str],
        k: int
    ) -> pd.DataFrame:
        """
        Generates the sampled data by sampling mutant IDs from each event type.

        Args:
            df: A DataFrame.
            mutant_dict: A dictionary containing event types as keys and mutant IDs as values.
            sorted_event_types: A list of event types sorted by the number of mutant IDs.
            k: The number of mutant IDs to sample from each event type.

        Returns:
            The DataFrame containing the sampled data.
        """
        sampled_data = pd.DataFrame()
        sampled_mutants = set()
        for event_type in sorted_event_types:
            sampled_data, sampled_mutants = MutantSampler.sample_from_event_type(
                df, mutant_dict, event_type, k, sampled_data, sampled_mutants
            )
        return sampled_data

    @staticmethod
    def remove_method_id_column(df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes the 'method_id' column from the DataFrame.

        Args:
            df: A DataFrame.

        Returns:
            The DataFrame without the 'method_id' column.
        """
        return df.drop(columns=['method_id'])

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
        df = MutantSampler.add_method_id_column(df)
        df = MutantSampler.drop_duplicates(df)
        mutant_dict = MutantSampler.populate_mutant_dict(df)
        sorted_event_types = MutantSampler.sort_event_types(mutant_dict)
        sampled_data = MutantSampler.get_sampled_data_from_types(
            df, mutant_dict, sorted_event_types, k
        )
        sampled_data = MutantSampler.remove_method_id_column(sampled_data)
        return sampled_data.sort_values(by='mutantId')
