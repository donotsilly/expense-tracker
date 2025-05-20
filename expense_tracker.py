import streamlit as st
import pandas as pd
from datetime import date

st.title("💸 Daily Expense Tracker")

if "expenses" not in st.session_state:
    try:
        st.session_state.expenses = pd.read_csv("expenses.csv")
    except FileNotFoundError:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

with st.form("add_expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Fuel", "Transport", "Entertainment", "Bills", "Other"])
    amount = st.number_input("Amount (AUD)", min_value=0.0, format="%.2f")
    note = st.text_input("Notes (optional)")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_expense = {
        "Date": expense_date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }
    st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_expense])], ignore_index=True)
    st.session_state.expenses.to_csv("expenses.csv", index=False)
    st.success("Expense added!")
    st.rerun()

st.subheader("📊 All Expenses")

df = st.session_state.expenses

if df.empty:
    st.info("No expenses yet. Add one above!")
else:
    for idx, row in df.iterrows():
        cols = st.columns([2, 2, 1, 3, 1])
        cols[0].write(row["Date"])
        cols[1].write(row["Category"])
        cols[2].write(f"${row['Amount']:.2f} AUD")
        cols[3].write(row["Note"])
        if cols[4].button("Delete", key=f"del_{idx}"):
            st.session_state.expenses = st.session_state.expenses.drop(idx).reset_index(drop=True)
            st.session_state.expenses.to_csv("expenses.csv", index=False)
            st.rerun()

    st.write(f"### 💰 Total Spent: ${df['Amount'].sum():.2f} AUD")
