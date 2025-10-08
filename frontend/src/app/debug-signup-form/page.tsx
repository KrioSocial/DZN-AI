'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { isValidEmail } from '@/lib/utils';
import toast from 'react-hot-toast';

export default function DebugSignupFormPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [debugInfo, setDebugInfo] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('=== SIGNUP FORM DEBUG ===');
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
    setDebugInfo(null);
    
    try {
      console.log('Calling api.signup...');
      const response = await api.signup(name, email, password);
      console.log('API Response:', response);
      
      setDebugInfo({ success: true, data: response });
      toast.success('Account created successfully!');
    } catch (error: any) {
      console.error('API Error:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText
      });
      
      setDebugInfo({ 
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
      <h1 className="text-3xl font-bold mb-6">Debug Signup Form</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
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
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="your@email.com"
          />
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
          className="w-full bg-blue-500 text-white py-2 px-4 rounded disabled:opacity-50"
        >
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>
      
      {debugInfo && (
        <div className="mt-8 bg-gray-100 p-6 rounded-lg">
          <h3 className="text-lg font-bold mb-4">
            {debugInfo.success ? '✅ Success' : '❌ Error'}
          </h3>
          <pre className="text-sm overflow-auto bg-white p-4 rounded border">
            {JSON.stringify(debugInfo, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
