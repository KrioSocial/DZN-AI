'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { isValidEmail } from '@/lib/utils';
import toast from 'react-hot-toast';

export default function WorkingSignupTestPage() {
  const [name, setName] = useState('Test User');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('password123');
  const [confirmPassword, setConfirmPassword] = useState('password123');
  const [termsAccepted, setTermsAccepted] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Generate a unique email
  const generateUniqueEmail = () => {
    const timestamp = Date.now();
    const randomNum = Math.floor(Math.random() * 1000);
    return `testuser${timestamp}${randomNum}@example.com`;
  };

  const handleGenerateEmail = () => {
    setEmail(generateUniqueEmail());
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('=== WORKING SIGNUP TEST ===');
    console.log('Form data:', { name, email, password, confirmPassword, termsAccepted });
    
    // Validate inputs
    if (!name || !email || !password || !confirmPassword) {
      const error = 'Please fill in all fields';
      console.log('Validation error:', error);
      toast.error(error);
      return;
    }
    
    if (!isValidEmail(email)) {
      const error = 'Please enter a valid email address';
      console.log('Email validation error:', error);
      toast.error(error);
      return;
    }
    
    if (password.length < 8) {
      const error = 'Password must be at least 8 characters';
      console.log('Password validation error:', error);
      toast.error(error);
      return;
    }
    
    if (password !== confirmPassword) {
      const error = 'Passwords do not match';
      console.log('Password match error:', error);
      toast.error(error);
      return;
    }
    
    if (!termsAccepted) {
      const error = 'Please accept the Terms of Service';
      console.log('Terms validation error:', error);
      toast.error(error);
      return;
    }
    
    setIsLoading(true);
    setResult(null);
    
    try {
      console.log('Calling api.signup with:', { name, email, password });
      const response = await api.signup(name, email, password);
      console.log('API Response:', response);
      
      setResult({ success: true, data: response });
      toast.success('Account created successfully! You can now login.');
    } catch (error: any) {
      console.error('API Error:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText
      });
      
      setResult({ 
        success: false, 
        error: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText
      });
      
      const errorMessage = error.response?.data?.error || 'Failed to create account';
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Working Signup Test</h1>
      <p className="text-gray-600 mb-6">This page will help you create an account successfully.</p>
      
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md mb-8">
        <div>
          <label className="block text-sm font-medium mb-2">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Your name"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <div className="flex gap-2">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="flex-1 p-2 border rounded"
              placeholder="your@email.com"
            />
            <button
              type="button"
              onClick={handleGenerateEmail}
              className="px-3 py-2 bg-gray-500 text-white rounded text-sm"
            >
              Generate
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">Click "Generate" to create a unique email</p>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Password"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Confirm password"
          />
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={termsAccepted}
            onChange={(e) => setTermsAccepted(e.target.checked)}
            className="mr-2"
          />
          <label className="text-sm">I accept the terms</label>
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-green-500 text-white py-2 px-4 rounded disabled:opacity-50"
        >
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>
      
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
        <h3 className="font-bold mb-2">Instructions:</h3>
        <ol className="list-decimal list-inside text-sm space-y-1">
          <li>Click "Generate" to create a unique email address</li>
          <li>Fill in your name (or keep "Test User")</li>
          <li>Keep the password as "password123" or change it</li>
          <li>Make sure passwords match</li>
          <li>Check the terms checkbox</li>
          <li>Click "Create Account"</li>
        </ol>
      </div>
    </div>
  );
}
