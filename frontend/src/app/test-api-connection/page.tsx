'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import axios from 'axios';
import toast from 'react-hot-toast';

export default function TestApiConnectionPage() {
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
      setResult({ success: true, data: response.data, method: 'Direct Axios' });
      toast.success('Direct API call successful!');
    } catch (error: any) {
      console.error('Direct API Error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        method: 'Direct Axios'
      });
      toast.error('Direct API call failed: ' + (error.response?.data?.error || error.message));
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
      toast.success('API client call successful!');
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
      toast.error('API client call failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Test API Connection</h1>
      <p className="text-gray-600 mb-6">This will test both direct API calls and the API client to see what's working.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <button 
          onClick={testDirectAPI}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-blue-600"
        >
          {loading ? 'Testing...' : 'Test Direct API Call'}
        </button>
        
        <button 
          onClick={testApiClient}
          disabled={loading}
          className="bg-green-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-green-600"
        >
          {loading ? 'Testing...' : 'Test API Client'}
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
        <h3 className="font-bold mb-2">Instructions:</h3>
        <ol className="list-decimal list-inside text-sm space-y-1">
          <li>Click "Test Direct API Call" first - this should work</li>
          <li>Click "Test API Client" second - this will show if the API client is working</li>
          <li>If both work, the issue is in the signup form</li>
          <li>If only direct API works, the issue is in the API client</li>
        </ol>
      </div>
    </div>
  );
}
