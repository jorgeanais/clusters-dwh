# clusters-dwh
A simple DB structure for store cluster data for the dashboard and a python program to populate tables

# Conda environment
To create a conda environment with the required packages, run the following commands:

```
conda create -n datacluster python=3.10
conda activate datacluster
pip install -r requirements.txt
```

Then run the `main.py` file to populate the tables.


Notice that sqlalchemy > 2.0 has problems with df.to_sql() method. So, I recommend to use the versions detailed in the `requirements.txt` file .