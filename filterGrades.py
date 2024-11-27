import pandas as pd
import argparse
import os

class GradesParser:
    def __init__(self, ids_file, excel_file, output_file, columns, csv_format):
        assert os.path.exists(ids_file), f"File {ids_file} does not exist"
        assert os.path.exists(excel_file), f"File {excel_file} does not exist"
        with open(ids_file, 'r') as f:
            self.desired_ids = [int(line.strip()) for line in f.readlines()]
        self.gr_data_frame = pd.read_excel(excel_file)
        self.output_file = output_file
        self.needed_columns = columns
        self.is_csv = csv_format

    def filter_students_data(self):
        # Filter the DataFrame to include only the desired IDs
        df = self.gr_data_frame
        df_filtered = df[df['ID'].isin(self.desired_ids)]

        # Filter the DataFrame to include only the specified columns
        df_filtered = df_filtered[['ID'] + self.needed_columns]

        # Fill non-finite values with a default integer value, e.g., 0
        df_filtered[self.needed_columns] = df_filtered[self.needed_columns].fillna(0).astype(int)

        # Determine the separator and header settings
        sep = ',' if self.is_csv else ' '
        header = self.is_csv

        # Check if the output file already exists
        if os.path.exists(self.output_file) is False:
            df_filtered[::-1].to_csv(self.output_file, index=False, sep=sep, header=header)
            print(f"Data has been written to {self.output_file}")
            return

        user_input = input(f"The file {self.output_file} already exists. Do you want to overwrite it? [y/n]: ")
        if user_input.lower() == 'y':
            df_filtered[::-1].to_csv(self.output_file, index=False, sep=sep, header=header)
            print(f"Data has been written to {self.output_file}")
        else:
            print("The file will not be overwritten.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Students IDs and get Grades from previous semesters Excel file.')
    parser.add_argument('--ids', type=str, help='Path to the file containing students IDs, where each row contains exactly a single ID')
    parser.add_argument('--gr_file', type=str, help='Path to the Excel file - created by GR - that contains the students data')
    parser.add_argument('--output_file', type=str, default='filtered.txt', help='Path to the output file')
    parser.add_argument('--columns', type=str, nargs='+', default=['HOMEWORK_TOTAL'], help='Columns to include in the output, e.g., HW1 HW2 HW3')
    parser.add_argument('--csv_format', action='store_true', help='Create a regular CSV file with commas and header')

    args = parser.parse_args()
    parser = GradesParser(args.ids, args.gr_file, args.output_file, args.columns, args.csv_format)
    parser.filter_students_data()
