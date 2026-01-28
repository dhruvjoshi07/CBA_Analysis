import pandas as pd
import os

# ---------- File Path ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "payment_transactions.csv")

print("Reading file from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# ---------- Data Validation ----------
print("\nData Validation Checks")

if df.empty:
    raise ValueError("Dataset is empty!")

missing = df.isnull().sum()
print("\nMissing Values:")
print(missing)

# Remove invalid records
df = df[df['amount_usd'] > 0]

# Convert date
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# ---------- Core Metrics ----------

# 1. Total Payment Volume (TPV)
tpv = df[df['status'] == 'Success']['amount_usd'].sum()
print("\nTotal Payment Volume (USD):", tpv)

# 2. Successful vs Failed Transactions
status_counts = df['status'].value_counts()
print("\nTransaction Status Summary:")
print(status_counts)

# 3. Country-wise TPV
country_tpv = df.groupby('receiver_country')['amount_usd'].sum()
print("\nCountry-wise TPV:")
print(country_tpv)

# 4. FX Impact Analysis
df['fx_impact'] = df['amount_usd'] * df['fx_rate']
fx_impact = df[df['status'] == 'Success']['fx_impact'].sum()
print("\nTotal FX Impact:", fx_impact)

# ---------- Advanced Metrics ----------

total_txns = len(df)
success_txns = len(df[df['status'] == 'Success'])
success_rate = (success_txns / total_txns) * 100

print("\nSuccess Rate (%):", round(success_rate, 2))

failure_by_country = (
    df[df['status'] == 'Failed']
    .groupby('receiver_country')
    .size()
)

print("\nFailure Count by Country:")
print(failure_by_country)

# ---------- Export for Dashboard ----------
output_path = os.path.join(BASE_DIR, "..", "dashboard", "cleaned_payments.csv")
df.to_csv(output_path, index=False)

print("\nCleaned data exported for Power BI at:")
print(output_path)
