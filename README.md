# Installation Instructions

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