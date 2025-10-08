'use client';

import { useState } from 'react';
import axios from 'axios';

export default function DebugSignupPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testSignup = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Making API call to:', 'http://localhost:5001/api/auth/register');
      
      const response = await axios.post('http://localhost:5001/api/auth/register', {
        name: 'Debug User',
        email: `debug${Date.now()}@example.com`,
        password: 'password123'
      });
      
      console.log('API Response:', response.data);
      setResult({ success: true, data: response.data });
    } catch (error: any) {
      console.error('API Error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Debug Signup API</h1>
      
      <div className="mb-6">
        <button 
          onClick={testSignup}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-blue-600"
        >
          {loading ? 'Testing...' : 'Test Signup API'}
        </button>
      </div>
      
      {result && (
        <div className="bg-gray-100 p-6 rounded-lg">
          <h3 className="text-lg font-bold mb-4">
            {result.success ? '✅ Success' : '❌ Error'}
          </h3>
          <pre className="text-sm overflow-auto bg-white p-4 rounded border">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
      
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-bold mb-2">API Endpoint:</h3>
        <code className="text-sm">http://localhost:5001/api/auth/register</code>
        
        <h3 className="font-bold mb-2 mt-4">Expected Request:</h3>
        <pre className="text-sm bg-white p-2 rounded border">
{`{
  "name": "Debug User",
  "email": "debug@example.com", 
  "password": "password123"
}`}
        </pre>
      </div>
    </div>
  );
}
