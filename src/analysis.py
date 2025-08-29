# src/analysis.py
# Run: python src/analysis.py
import os
import pandas as pd
import numpy as np

from scipy.stats import chi2_contingency
import statsmodels.api as sm

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "orders.csv")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# Load data and ensure correct data types
df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])

# Ensure numeric columns are of the correct type and handle potential errors
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['seller_rating'] = pd.to_numeric(df['seller_rating'], errors='coerce')
df = df.dropna(subset=['price', 'seller_rating']) # Drop rows where conversion failed

# 1) Quick summaries
summary = {}
summary['overall_return_rate'] = float(df['is_returned'].mean())

by_cat = df.groupby('category')['is_returned'].mean().sort_values(ascending=False)
by_region = df.groupby('region')['is_returned'].mean().sort_values(ascending=False)
by_seller = df.groupby('seller_id')['is_returned'].mean().sort_values(ascending=False)

# Save summaries
by_cat.to_csv(os.path.join(OUT_DIR, "return_rate_by_category.csv"))
by_region.to_csv(os.path.join(OUT_DIR, "return_rate_by_region.csv"))
by_seller.head(50).to_csv(os.path.join(OUT_DIR, "return_rate_by_seller_top50.csv"))

# 2) Chi-square test: category vs return
contingency = pd.crosstab(df['category'], df['is_returned'])
chi2, p, dof, ex = chi2_contingency(contingency)
summary['chi2_category_return'] = {'chi2': float(chi2), 'p_value': float(p), 'dof': int(dof)}

# 3) Logistic regression: is_returned ~ price + seller_rating + category dummies + region dummies + payment_method
# Build design matrix
X = pd.get_dummies(df[['price', 'seller_rating', 'category', 'region', 'payment_method']], drop_first=True)
y = df['is_returned'].astype(int)

# **FINAL FIX:** Convert the boolean dummy variables to integers (0 and 1)
# and ensure the entire dataframe is a single, consistent numeric dtype.
X = X.astype(float) # Converts booleans to 0.0 and 1.0

# Add a constant to the independent variable matrix
X = sm.add_constant(X)

logit = sm.Logit(y, X)
result = logit.fit()

# Save regression summary
with open(os.path.join(OUT_DIR, "logistic_regression_summary.txt"), "w") as f:
    f.write(result.summary().as_text())

print("Analysis complete. Outputs saved to the 'outputs' folder.")