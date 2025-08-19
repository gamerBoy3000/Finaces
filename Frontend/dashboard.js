// frontend/src/pages/Dashboard.js
import React, { useState } from 'react';
import BudgetForm from '../components/BudgetForm';
import './dashboard.css';

const Dashboard = () => {
  const [budgets, setBudgets] = useState([]);
  const [transactions, setTransactions] = useState([
    {
      date: '2025-08-15',
      description: 'Groceries',
      category: 'Food',
      amount: -120,
    },
    {
      date: '2025-08-14',
      description: 'Electric Bill',
      category: 'Utilities',
      amount: -60,
    },
    {
      date: '2025-08-13',
      description: 'Salary',
      category: 'Income',
      amount: 3000,
    },
  ]);

  const handleAddBudget = (budgetData) => {
    setBudgets([...budgets, budgetData]);
  };

  const totalBudget = budgets.reduce((acc, b) => acc + b.amount, 0);
  const totalSpent = transactions
    .filter((t) => t.amount < 0)
    .reduce((acc, t) => acc + Math.abs(t.amount), 0);
  const remaining = totalBudget - totalSpent;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>My Budget Dashboard</h1>
      </div>

      <div className="dashboard-overview">
        <div className="overview-card">
          <h3>Total Budget</h3>
          <div className="amount">${totalBudget.toFixed(2)}</div>
        </div>
        <div className="overview-card">
          <h3>Spent</h3>
          <div className="amount">${totalSpent.toFixed(2)}</div>
        </div>
        <div className="overview-card">
          <h3>Remaining</h3>
          <div className="amount">${remaining.toFixed(2)}</div>
        </div>
      </div>

      <div className="transactions-section">
        <h2>Recent Transactions</h2>
        <table className="transactions-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Category</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t, idx) => (
              <tr key={idx}>
                <td>{t.date}</td>
                <td>{t.description}</td>
                <td>{t.category}</td>
                <td style={{ color: t.amount < 0 ? 'red' : 'green' }}>
                  {t.amount < 0 ? '-' : '+'}${Math.abs(t.amount).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="budget-form-section">
        <BudgetForm onSubmit={handleAddBudget} />
      </div>
    </div>
  );
};

export default Dashboard;
