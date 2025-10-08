/**
 * Next.js Configuration
 * Configures the Next.js application behavior, API rewrites, and optimization settings
 */

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for highlighting potential problems
  reactStrictMode: true,
  
  // Configure image domains for Next.js Image component
  images: {
    domains: [
      'localhost',
      // Add OpenAI DALL-E image domains
      'oaidalleapiprodscus.blob.core.windows.net',
    ],
  },
  
  // API proxy configuration to connect frontend to Flask backend
  async rewrites() {
    return [
      {
        // Proxy all /api requests to Flask backend
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*',
      },
    ]
  },
  
  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
  
  // TypeScript configuration
  typescript: {
    // Type checking is done separately, so we can skip it during build
    ignoreBuildErrors: false,
  },
  
  // ESLint configuration
  eslint: {
    // Run ESLint during builds
    ignoreDuringBuilds: false,
  },
}

module.exports = nextConfig

