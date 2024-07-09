import pandas as pd
import numpy as np
import datetime

# Date range for the past 12 months
date_range = pd.date_range(start=(datetime.datetime.now() - datetime.timedelta(days=365)), periods=365, freq='D')

# Dummy data for Revenue and Profit
revenue = np.random.randint(50000, 150000, size=len(date_range))
profit = revenue - np.random.randint(20000, 100000, size=len(date_range))

# Dummy data for Expenses Breakdown
expense_categories = ['Salaries', 'Marketing', 'R&D', 'Operations', 'Miscellaneous']
expenses = {category: np.random.randint(5000, 30000, size=len(date_range)) for category in expense_categories}

# Dummy data for Cash Flow
cash_inflow = revenue + np.random.randint(10000, 50000, size=len(date_range))
cash_outflow = cash_inflow - profit

# Dummy data for Financial Ratios
current_ratio = np.round(np.random.uniform(1.0, 3.0, size=len(date_range)), 2)
quick_ratio = np.round(np.random.uniform(0.8, 2.5, size=len(date_range)), 2)
debt_to_equity_ratio = np.round(np.random.uniform(0.5, 2.0, size=len(date_range)), 2)
gross_margin = np.round(np.random.uniform(0.2, 0.6, size=len(date_range)), 2)

# Combine data into a DataFrame
data = pd.DataFrame({
    'Date': date_range,
    'Revenue': revenue,
    'Profit': profit,
    'Cash Inflow': cash_inflow,
    'Cash Outflow': cash_outflow,
    'Current Ratio': current_ratio,
    'Quick Ratio': quick_ratio,
    'Debt-to-Equity Ratio': debt_to_equity_ratio,
    'Gross Margin': gross_margin
})

for category, values in expenses.items():
    data[category + ' Expense'] = values

data.to_csv("financial_database.csv", index=False)