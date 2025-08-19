// frontend/src/components/IncomeChartD.js
import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const IncomeChartD = ({ transactions }) => {
  // Filter and group income by month
  const incomeTransactions = transactions.filter(t => t.amount > 0);

  const incomeByMonth = {};

  incomeTransactions.forEach(t => {
    const month = new Date(t.date).toLocaleString('default', { month: 'short', year: 'numeric' });
    incomeByMonth[month] = (incomeByMonth[month] || 0) + t.amount;
  });

  const labels = Object.keys(incomeByMonth);
  const dataValues = Object.values(incomeByMonth);

  const data = {
    labels,
    datasets: [
      {
        label: 'Monthly Income',
        data: dataValues,
        backgroundColor: '#4caf50',
        borderRadius: 5,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="income-chart-container">
      <h2>Income Overview</h2>
      <Bar data={data} options={options} />
    </div>
  );
};

export default IncomeChartD;
