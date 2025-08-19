// frontend/src/components/ExpenseList.js
import React from 'react';
import './ExpenseList.css'; // Optional for custom styles

const ExpenseList = ({ expenses }) => {
  if (expenses.length === 0) {
    return <p>No expenses recorded.</p>;
  }

  return (
    <div className="expense-list">
      <h2>Expense List</h2>
      <table className="expense-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Category</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense, index) => (
            <tr key={index}>
              <td>{expense.date}</td>
              <td>{expense.description}</td>
              <td>{expense.category}</td>
              <td
                style={{
                  color: expense.amount < 0 ? 'red' : 'green',
                }}
              >
                {expense.amount < 0 ? '-' : '+'}${Math.abs(expense.amount).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExpenseList;
