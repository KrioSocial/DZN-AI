/**
 * Root Layout Component
 * Wraps all pages with global providers and styles
 */

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from 'react-hot-toast';
import './globals.css';

// Load Inter font with Latin subset
const inter = Inter({ subsets: ['latin'] });

// Metadata for SEO
export const metadata: Metadata = {
  title: 'AI Studio - Interior Design Platform',
  description: 'Run your design studio like a 10-person team — powered by AI. Manage clients, projects, and create stunning designs.',
  keywords: ['interior design', 'AI', 'design platform', 'project management'],
};

/**
 * Root layout component that wraps all pages
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full`}>
        {/* Main content */}
        {children}
        
        {/* Toast notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            className: '',
            success: {
              className: 'toast-success',
            },
            error: {
              className: 'toast-error',
            },
          }}
        />
      </body>
    </html>
  );
}

