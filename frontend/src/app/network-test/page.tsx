'use client';

import { useState } from 'react';
import axios from 'axios';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

export default function NetworkTestPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testDirectConnection = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Testing direct connection to backend...');
      
      // Test 1: Health check
      const healthResponse = await axios.get('http://localhost:5001/api/health');
      console.log('Health check:', healthResponse.data);
      
      // Test 2: Registration
      const registerResponse = await axios.post('http://localhost:5001/api/auth/register', {
        name: 'Network Test User',
        email: `networktest${Date.now()}@example.com`,
        password: 'password123'
      });
      console.log('Registration:', registerResponse.data);
      
      setResult({ 
        success: true, 
        data: {
          health: healthResponse.data,
          registration: registerResponse.data
        },
        method: 'Direct Axios'
      });
      toast.success('Direct connection successful!');
    } catch (error: any) {
      console.error('Direct connection error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        method: 'Direct Axios'
      });
      toast.error('Direct connection failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const testApiClient = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Testing API client...');
      
      const response = await api.signup(
        'API Client Test User',
        `apiclienttest${Date.now()}@example.com`,
        'password123'
      );
      
      console.log('API Client Response:', response);
      setResult({ success: true, data: response, method: 'API Client' });
      toast.success('API client successful!');
    } catch (error: any) {
      console.error('API Client Error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        method: 'API Client'
      });
      toast.error('API client failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const testFetch = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Testing fetch API...');
      
      const response = await fetch('http://localhost:5001/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: 'Fetch Test User',
          email: `fetchtest${Date.now()}@example.com`,
          password: 'password123'
        })
      });
      
      const data = await response.json();
      console.log('Fetch Response:', data);
      
      setResult({ success: true, data, method: 'Fetch API' });
      toast.success('Fetch API successful!');
    } catch (error: any) {
      console.error('Fetch Error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        method: 'Fetch API'
      });
      toast.error('Fetch API failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Network Connection Test</h1>
      <p className="text-gray-600 mb-6">This will test different ways to connect to the backend API.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <button 
          onClick={testDirectConnection}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-blue-600"
        >
          {loading ? 'Testing...' : 'Test Direct Axios'}
        </button>
        
        <button 
          onClick={testApiClient}
          disabled={loading}
          className="bg-green-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-green-600"
        >
          {loading ? 'Testing...' : 'Test API Client'}
        </button>
        
        <button 
          onClick={testFetch}
          disabled={loading}
          className="bg-purple-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-purple-600"
        >
          {loading ? 'Testing...' : 'Test Fetch API'}
        </button>
      </div>
      
      {result && (
        <div className="bg-gray-100 p-6 rounded-lg">
          <h3 className="text-lg font-bold mb-4">
            {result.success ? '✅ Success' : '❌ Error'} - {result.method}
          </h3>
          <pre className="text-sm overflow-auto bg-white p-4 rounded border">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
      
      <div className="mt-8 p-4 bg-yellow-50 rounded-lg">
        <h3 className="font-bold mb-2">Test Results:</h3>
        <ul className="list-disc list-inside text-sm space-y-1">
          <li><strong>Direct Axios:</strong> Tests raw axios connection to backend</li>
          <li><strong>API Client:</strong> Tests the configured API client used by signup form</li>
          <li><strong>Fetch API:</strong> Tests native browser fetch API</li>
        </ul>
        <p className="text-sm mt-2 text-gray-600">
          If Direct Axios works but API Client fails, the issue is in the API client configuration.
          If all fail, there's a network/CORS issue.
        </p>
      </div>
    </div>
  );
}
