// frontend/src/components/BudgetForm.js
import React, { useState } from 'react';

const BudgetForm = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!name || !amount || !category) {
      alert('Please fill in all fields');
      return;
    }

    const budgetData = {
      name,
      amount: parseFloat(amount),
      category,
      date: new Date().toISOString(),
    };

    onSubmit(budgetData);

    // Clear the form
    setName('');
    setAmount('');
    setCategory('');
  };

  return (
    <form onSubmit={handleSubmit} className="budget-form">
      <h2>Add New Budget</h2>

      <div>
        <label>Budget Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Rent"
        />
      </div>

      <div>
        <label>Amount ($):</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="e.g., 1000"
