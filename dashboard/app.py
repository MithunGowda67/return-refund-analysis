# dashboard/app.py
# Run: streamlit run dashboard/app.py
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "orders.csv")

st.set_page_config(page_title="Return & Refund Dashboard", layout="wide")
st.title("📦 Return & Refund Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    return df

df = load_data()

st.subheader("Key KPIs")
col1, col2, col3, col4 = st.columns(4)
overall_return_rate = df['is_returned'].mean()
col1.metric("Overall Return Rate", f"{overall_return_rate*100:.2f}%")
col2.metric("Total Orders", f"{len(df):,}")
col3.metric("Unique Sellers", df['seller_id'].nunique())
col4.metric("Unique Customers", df['customer_id'].nunique())

st.divider()

# Filters
regions = ["All"] + sorted(df['region'].unique().tolist())
cats = ["All"] + sorted(df['category'].unique().tolist())
sellers = ["All"] + sorted(df['seller_id'].unique().tolist())

f1, f2, f3 = st.columns(3)
region_sel = f1.selectbox("Filter by Region", regions, index=0)
cat_sel = f2.selectbox("Filter by Category", cats, index=0)
seller_sel = f3.selectbox("Filter by Seller", sellers, index=0)

mask = pd.Series(True, index=df.index)
if region_sel != "All":
    mask &= df['region'] == region_sel
if cat_sel != "All":
    mask &= df['category'] == cat_sel
if seller_sel != "All":
    mask &= df['seller_id'] == seller_sel

fdf = df[mask]

st.subheader("Return Rates")
cc1, cc2, cc3 = st.columns(3)

with cc1:
    st.caption("By Category")
    st.bar_chart(fdf.groupby('category')['is_returned'].mean().sort_values(ascending=False))

with cc2:
    st.caption("By Region")
    st.bar_chart(fdf.groupby('region')['is_returned'].mean().sort_values(ascending=False))

with cc3:
    st.caption("Top 15 Sellers by Return Rate (min 50 orders)")
    tmp = fdf.groupby('seller_id').agg(n=('is_returned', 'size'), rate=('is_returned', 'mean'))
    tmp = tmp[tmp['n']>=50].sort_values('rate', ascending=False).head(15)['rate']
    if len(tmp) > 0:
        st.bar_chart(tmp)
    else:
        st.write("Not enough data after filters.")

st.subheader("Daily Rolling Return Rate (30D)")
daily = fdf.groupby(fdf['order_date'].dt.date).agg(total=('is_returned','size'),
                                                    returns=('is_returned','sum'))
daily = daily.sort_index()
if len(daily) > 0:
    daily['rolling_rate'] = (daily['returns'].rolling(30).sum() / daily['total'].rolling(30).sum()).fillna(0)
    st.line_chart(daily['rolling_rate'])
else:
    st.write("No data for selected filters.")

st.subheader("Raw Data (sample)")
st.dataframe(fdf.sample(min(500, len(fdf))).reset_index(drop=True))