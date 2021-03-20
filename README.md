# DatabaseMaintenance

## Developer Instructions

### Getting Google Application credentials

If you don't have a service account yet, follow these instructions:
- Go to firebase console
- Click on trojan check in check out project overview
- Click on the "gear" in the top left and click on "project settings"
- Go to service account tab
- Click "generate new private key" to download json file

Once you have the json file, set the environment variable, GOOGLE_APPLICATION_CREDENTIALS to the path of your json file
- So if your json file path is /home/users/tommy/data/key.json, you would enter the commaand:

`
export GOOGLE_APPLICATION_CREDENTIALS="/home/users/tommy/data/key.json"
`

Now, go into your main directory of the repository, and run the command:

`
pip install -r requirements.txt
`

You should have a CSV file with the format as specified by the current format in the repository.
If your csv file path is "buildings.csv", to initialize Firestore, run the command: 

`
python -i buildings.csv -o codes
`

The python script takes two paramets:
- -i : path to csv file
- -o output directory path of qr codes
