const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || ${{ values.port }};

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Routes
app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: '${{ values.name }}' });
});

app.get('/api/v1/', (req, res) => {
  res.json({ 
    message: 'Welcome to ${{ values.name }}',
    description: '${{ values.description }}'
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`${{ values.name }} running on port ${PORT}`);
});

module.exports = app;
