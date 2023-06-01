import argparse
from file_manager import FileManager as fm
from mutant_sampler import MutantSampler as ms

def main(args: argparse.Namespace) -> None:
    """
    Main function for selecting a subset of mutants for testing.

    Parameters:
    - args (argparse.Namespace): Command-line arguments parsed by argparse.

    Returns:
    - None
    """
    data = fm.load(args.input_file_path)
    selected_mutants = ms.get_sampled_data(data, args.num_samples)
    fm.save(selected_mutants, args.output_dir_path, args.output_file_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select mutant subset for testing')
    parser.add_argument('--input-file-path', type=str, help='Path to the input file')
    parser.add_argument('--output-dir-path', type=str, help='Path to the output directory')
    parser.add_argument('--output-file-name', type=str, help='Name of the output file')
    parser.add_argument('--num-samples', type=int, help='Number of samples to take of each type')
    args = parser.parse_args()

    main(args)

    print("Done")

