# Return & Refund Analysis (E-commerce)

A complete, portfolio-ready project that analyzes product returns to reduce profitability leakage. 
Aligned with a Business Analyst role (e.g., Meesho JD): own metrics, find drivers, and recommend actions.

## 📦 Project Structure
```
return-refund-analysis/
├── data/
│   └── orders.csv               # synthetic dataset
├── sql/
│   └── return_analysis.sql      # core SQL for rates & risk matrices
├── src/
│   └── analysis.py              # chi-square, logistic regression
├── dashboard/
│   └── app.py                   # Streamlit dashboard
├── outputs/                     # generated outputs (after analysis)
├── reports/                     # add your PPT/MD/PDF
├── requirements.txt
└── README.md
```

## 🔧 Setup
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run Analysis
```bash
python src/analysis.py
```
Outputs will be saved to `outputs/` (e.g., return rates by category/region and a logistic regression summary).

## 📊 Run Dashboard
```bash
streamlit run dashboard/app.py
```

## 📁 Dataset Schema
- `order_id` (int)
- `order_date` (date)
- `customer_id` (str)
- `seller_id` (str)
- `category` (str)
- `price` (float)
- `region` (str)
- `seller_rating` (float 1.5–5.0)
- `payment_method` (str: COD/UPI/Card/NetBanking)
- `is_returned` (0/1)

## 📈 Questions Answered
- Which categories/regions/sellers have the highest return rates?
- Are returns significantly associated with category (chi-square)?
- How do price and seller rating affect return probability (logistic regression)?
- What interventions reduce returns?

## 🧭 Recommendations (Template)
- **Seller Ops:** Coach sellers with return rate > 20%, enforce minimum rating thresholds.
- **Content:** Improve titles/images for high-return categories (e.g., Fashion/Footwear).
- **Payments & CX:** Nudge towards prepaid methods where appropriate; refine return policy.
- **Region Ops:** Investigate packaging/logistics for high-return regions.

## 🔒 Notes
This is synthetic data for demonstration and learning purposes only.