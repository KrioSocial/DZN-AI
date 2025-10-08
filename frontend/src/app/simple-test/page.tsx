'use client';

import { useState } from 'react';
import axios from 'axios';

export default function SimpleTestPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testDirectAPI = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Testing direct axios call...');
      
      const response = await axios.post('http://localhost:5001/api/auth/register', {
        name: 'Direct Test User',
        email: `directtest${Date.now()}@example.com`,
        password: 'password123'
      });
      
      console.log('Direct API Response:', response.data);
      setResult({ success: true, data: response.data });
    } catch (error: any) {
      console.error('Direct API Error:', error);
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
      <h1 className="text-3xl font-bold mb-6">Simple Direct API Test</h1>
      
      <div className="mb-6">
        <button 
          onClick={testDirectAPI}
          disabled={loading}
          className="bg-purple-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-purple-600"
        >
          {loading ? 'Testing...' : 'Test Direct API Call'}
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
      
      <div className="mt-8 p-4 bg-purple-50 rounded-lg">
        <h3 className="font-bold mb-2">This test bypasses the API client and calls the backend directly:</h3>
        <code className="text-sm">axios.post('http://localhost:5001/api/auth/register', data)</code>
      </div>
    </div>
  );
}
