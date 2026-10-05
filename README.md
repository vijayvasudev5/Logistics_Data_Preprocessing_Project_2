# Logistics Data Collection and Preprocessing Project

## Objective
Simulate a logistics data-preprocessing pipeline involving data collection, cleaning, missing-value handling, outlier treatment, and normalization.

## Dataset
A synthetic logistics shipment dataset is included in `data/logistics_raw.csv`. It contains:
- Shipment ID
- Origin and destination
- Transport mode
- Distance
- Shipment weight
- Shipping time
- Shipping cost
- Delivery status

The dataset intentionally contains missing values, duplicate records, and numeric outliers so that the preprocessing pipeline can be demonstrated.

## How to Run

### 1. Open terminal in this project folder
```text
cd Logistics_Data_Preprocessing_Project
```

### 2. Install packages
```text
python -m pip install -r requirements.txt
```
If `python` is not recognized on Windows, try:
```text
py -m pip install -r requirements.txt
```

### 3. Run the preprocessing program
```text
python preprocess.py
```
or:
```text
py preprocess.py
```

### 4. Check the output folder
The program creates:
- `logistics_cleaned.csv`
- `logistics_preprocessed.csv`
- `outlier_report.csv`
- `preprocessing_summary.csv`

## Main Techniques
1. Duplicate removal using `drop_duplicates()`
2. Missing-value replacement using median/mode
3. IQR-based outlier detection and capping
4. Min-Max normalization to a 0-1 range
5. Export of cleaned and processed datasets

## Academic Note
The raw dataset is a simulation created for this project. The same pipeline can be applied to publicly available logistics, transportation, shipping, or inventory datasets.
