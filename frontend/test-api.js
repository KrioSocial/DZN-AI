// Test script to check API connectivity
const axios = require('axios');

async function testSignup() {
  try {
    console.log('Testing signup API...');
    const response = await axios.post('http://localhost:5001/api/auth/register', {
      name: 'Test User',
      email: 'newuser@example.com',
      password: 'password123'
    });
    console.log('Success:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

testSignup();
