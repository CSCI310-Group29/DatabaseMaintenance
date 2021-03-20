import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import shutil
import argparse
import csv
import pyqrcode

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

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def get_firestore_instance():
    firebase_admin.initialize_app()
    db = firestore.client()
    return db


def generateQR(out_dir, buildingName, buildingId):
    qr = pyqrcode.create(str(buildingId))
    output_file = os.path.join(out_dir, buildingName + '.svg')
    qr.svg(output_file, scale=SCALE)


def process_csv(params):
    csv_file = params['csv']
    out_dir = params['out_dir']
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    db = get_firestore_instance()
    delete_collection(db.collection("buildings"), 200)
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for building in reader:

            process_building(out_dir, db, building)


def process_building(out_dir, db, building):
    doc = db.collection("buildings").document()
    doc.set({
        'buildingName': building['buildingName'],
        'address': building['address'],
        'capacity': building['capacity']
    })
    generateQR(out_dir, building['buildingName'], doc.id)

if __name__ == '__main__':
    process_csv(parse_arguments())