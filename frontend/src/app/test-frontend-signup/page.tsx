'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

export default function TestFrontendSignupPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testSignup = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Testing frontend API client...');
      
      const response = await api.signup(
        'Frontend Test User',
        `frontendtest${Date.now()}@example.com`,
        'password123'
      );
      
      console.log('Frontend API Response:', response);
      setResult({ success: true, data: response });
      toast.success('Signup successful!');
    } catch (error: any) {
      console.error('Frontend API Error:', error);
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        stack: error.stack
      });
      toast.error('Signup failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Test Frontend Signup API</h1>
      
      <div className="mb-6">
        <button 
          onClick={testSignup}
          disabled={loading}
          className="bg-green-500 text-white px-6 py-3 rounded-lg disabled:opacity-50 hover:bg-green-600"
        >
          {loading ? 'Testing Frontend API...' : 'Test Frontend Signup API'}
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
      
      <div className="mt-8 p-4 bg-green-50 rounded-lg">
        <h3 className="font-bold mb-2">This test uses the same API client as the signup form:</h3>
        <code className="text-sm">api.signup(name, email, password)</code>
      </div>
    </div>
  );
}
