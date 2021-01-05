# Installation Instructions

### Datasets

The raw movies datasets used in this demo is from [IMDB](https://www.imdb.com/interfaces/)

To use or modify the dataset, download the files title.akas.tsv, title.basics.tsv, and title.ratings.tsv into the preprocessing file. Then run tsv_to_csv.py

### Server

We recommend downloading and installing Anaconda to obtain all relevant packages for this app.

Alternatively, `pip install` the following packages:
* Flask
* pandas
* scikit-learn 

### Client

Navigate to the `client` folder and run:
```
npm install
```

### Vega Specs Datasets

Datasets of vega specs are at the following locations:
```
./client/public/manual_specs_one_hot_encoding_2.csv
```

# Run the App

### Server

In the main folder run:
```
python server.py
```

### Client

Navigate to the `client` folder and run:
```
npm run dev
```

The application will be live at `localhost:5000`