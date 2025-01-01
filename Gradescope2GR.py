import csv
import argparse
import math

def process_grades(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, delimiter=' ')
        
        # Write the header of the output file
        writer.writerow(['ID', 'Grade'])
        
        # Process each row in the input file
        for row in reader:
            sid = row['SID']
            autograder_grade = row.get('1: Autograder (70.0 pts)')
            dry_part_grade = row.get('2: Dry Part (30.0 pts)')
            
            # Check if the grades are missing (None or empty string), and skip the row if they are
            if autograder_grade is None or autograder_grade == '' or dry_part_grade is None or dry_part_grade == '':
                continue
            
            # Convert the grades to float
            autograder_grade = float(autograder_grade)
            dry_part_grade = float(dry_part_grade)
            
            # Calculate the total grade and round it up
            total_grade = math.ceil(autograder_grade + dry_part_grade)
            
            # Convert total grade to integer
            total_grade = int(total_grade)
            
            # Write the SID and total grade to the output file
            writer.writerow([sid, total_grade])

def main():
    parser = argparse.ArgumentParser(description="Process grades from a CSV file.")
    parser.add_argument('input_file', help="The input CSV file with student grades")
    parser.add_argument('output_file', help="The output CSV file with processed grades")

    args = parser.parse_args()
    
    process_grades(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
