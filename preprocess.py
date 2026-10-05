import pandas as pd
import numpy as np
from pathlib import Path

INPUT = Path("data/logistics_raw.csv")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(INPUT)
print("Original shape:", df.shape)

# 2. Basic inspection
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# 3. Remove exact duplicate records
df = df.drop_duplicates().copy()

# 4. Convert numeric columns to numeric type
numeric_cols = [
    "Distance_km",
    "Weight_kg",
    "Shipping_Time_hr",
    "Shipping_Cost_INR"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Handle missing values
# Median is used because it is less sensitive to outliers than the mean.
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Categorical missing values, if any, are replaced with the mode.
categorical_cols = ["Origin", "Destination", "Transport_Mode", "Status"]
for col in categorical_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].mode()[0])

# 6. Outlier detection and treatment using IQR capping
# Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are capped.
outlier_report = []
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    before = ((df[col] < lower) | (df[col] > upper)).sum()
    df[col] = df[col].clip(lower=lower, upper=upper)
    outlier_report.append({
        "Column": col,
        "Lower_Bound": lower,
        "Upper_Bound": upper,
        "Outliers_Treated": int(before)
    })

pd.DataFrame(outlier_report).to_csv(
    OUTPUT_DIR / "outlier_report.csv", index=False
)

# 7. Min-Max normalization
# Creates values in the 0-1 range for machine-learning/analytics use.
normalized = df.copy()
for col in numeric_cols:
    min_val = normalized[col].min()
    max_val = normalized[col].max()
    if max_val != min_val:
        normalized[col + "_Normalized"] = (
            (normalized[col] - min_val) / (max_val - min_val)
        )
    else:
        normalized[col + "_Normalized"] = 0.0

# 8. Save cleaned and normalized dataset
df.to_csv(OUTPUT_DIR / "logistics_cleaned.csv", index=False)
normalized.to_csv(OUTPUT_DIR / "logistics_preprocessed.csv", index=False)

# 9. Save summary
summary = pd.DataFrame({
    "Metric": [
        "Rows after duplicate removal",
        "Columns",
        "Total missing values after cleaning",
        "Duplicate rows after cleaning"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df.isnull().sum().sum()),
        int(df.duplicated().sum())
    ]
})
summary.to_csv(OUTPUT_DIR / "preprocessing_summary.csv", index=False)

print("\nPreprocessing completed successfully.")
print("Cleaned file:", OUTPUT_DIR / "logistics_cleaned.csv")
print("Normalized file:", OUTPUT_DIR / "logistics_preprocessed.csv")
