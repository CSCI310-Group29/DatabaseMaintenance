import pyqrcode
import argparse
import csv
import shutil
import os

SCALE = 8

def parse_arguments():
    description = 'Generates QR codes for each building in the CSV file'

    parser = argparse.ArgumentParser(description=description)

    required = parser.add_argument_group("required arguments")

    help_csv = 'CSV file containing building names, addresses, and capacities'
    required.add_argument('-i', '--csv', help=help_csv, type=str, required=True)

    help_out = 'Output directory for storing QR svg files'
    required.add_argument('-o', '--out_dir', help=help_out, type=str, required=True)

    args = parser.parse_args()

    return {
        'csv': args.csv,
        'out_dir': args.out_dir
    }


def process_csv(params):
    csv_file = params['csv']
    out_dir = params['out_dir']
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            generateQR(out_dir, row['buildingName'])



def generateQR(out_dir, buildingName, buildingId):
    qr = pyqrcode.create(str(buildingId))
    output_file = os.path.join(out_dir, buildingName + '.svg')
    qr.svg(output_file, scale=SCALE)

if __name__ == '__main__':
    process_csv(parse_arguments())
