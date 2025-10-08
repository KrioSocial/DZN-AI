/**
 * Landing Page Component
 * Modern, beautiful landing page with hero section, features, and pricing
 */

import Link from 'next/link';
import { ArrowRight, CheckCircle2, Sparkles, Users, Calendar, DollarSign, Palette, ShoppingBag, MessageSquare } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-amber-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Palette className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">AI Studio</span>
            </div>
            
            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-primary-600 transition">Features</a>
              <a href="#pricing" className="text-gray-600 hover:text-primary-600 transition">Pricing</a>
              <Link href="/auth/login" className="text-gray-600 hover:text-primary-600 transition">
                Login
              </Link>
              <Link href="/auth/signup" className="btn btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Hero Text */}
            <div className="space-y-8 animate-in">
              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                Run your design studio like a{' '}
                <span className="text-primary-600">10-person team</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Powered by AI, built for interior designers. Manage clients, create stunning designs, and automate your workflow — all in one beautiful platform.
              </p>
              
              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/auth/signup" className="btn btn-primary btn-lg group">
                  Start Free Trial
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link href="#demo" className="btn btn-secondary btn-lg">
                  Watch Demo
                </Link>
              </div>
              
              {/* Feature Badges */}
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>5 free AI designs</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span>2 minute setup</span>
                </div>
              </div>
            </div>
            
            {/* Hero Image/Demo */}
            <div className="relative animate-slide-up">
              <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
                <div className="bg-gray-100 px-4 py-3 flex items-center space-x-2 border-b border-gray-200">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <div className="p-8 space-y-4">
                  {/* Simulated dashboard preview */}
                  <div className="h-4 bg-gray-200 rounded w-1/3 animate-pulse"></div>
                  <div className="space-y-3">
                    <div className="h-20 bg-gradient-to-r from-primary-100 to-primary-50 rounded-lg"></div>
                    <div className="h-20 bg-gradient-to-r from-purple-100 to-purple-50 rounded-lg"></div>
                    <div className="h-20 bg-gradient-to-r from-amber-100 to-amber-50 rounded-lg"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Everything you need to run your design business</h2>
            <p className="text-xl text-gray-600">Replace Notion, Pinterest, Canva, Gmail, and Excel with one powerful platform</p>
          </div>
          
          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition-all duration-300"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Simple, transparent pricing</h2>
            <p className="text-xl text-gray-600">Start free, upgrade as you grow</p>
          </div>
          
          {/* Pricing Cards */}
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {pricingTiers.map((tier, index) => (
              <div
                key={index}
                className={`relative rounded-2xl border-2 p-8 ${
                  tier.popular
                    ? 'border-primary-600 shadow-xl scale-105'
                    : 'border-gray-200'
                }`}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </div>
                )}
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold mb-2">{tier.name}</h3>
                  <div className="text-4xl font-bold mb-2">
                    £{tier.price}
                    <span className="text-lg text-gray-500 font-normal">/month</span>
                  </div>
                  <p className="text-gray-600">{tier.description}</p>
                </div>
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature, fIndex) => (
                    <li key={fIndex} className="flex items-start gap-3">
                      <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/auth/signup"
                  className={`block text-center py-3 rounded-lg font-medium transition ${
                    tier.popular
                      ? 'bg-primary-600 text-white hover:bg-primary-700'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {tier.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold mb-6">Ready to transform your design business?</h2>
          <p className="text-xl mb-8 text-indigo-100">Join hundreds of interior designers already using AI Studio</p>
          <Link href="/auth/signup" className="inline-flex items-center px-8 py-4 bg-white text-primary-600 rounded-lg font-semibold text-lg hover:bg-gray-50 transition">
            Start Free Trial
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
          <p className="mt-6 text-sm text-indigo-200">No credit card required • 5 free AI designs • Cancel anytime</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                  <Palette className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold text-white">AI Studio</span>
              </div>
              <p className="text-sm">Empowering interior designers with AI-powered tools.</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#features" className="hover:text-white transition">Features</a></li>
                <li><a href="#pricing" className="hover:text-white transition">Pricing</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">About</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition">Contact</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-sm text-center">
            <p>&copy; 2024 AI Studio. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Feature data
const features = [
  {
    icon: <Sparkles className="w-6 h-6 text-primary-600" />,
    title: 'AI Design Generator',
    description: 'Generate moodboards, color palettes, and product suggestions instantly',
  },
  {
    icon: <Users className="w-6 h-6 text-primary-600" />,
    title: 'Client Management',
    description: 'Track preferences, messaging, and AI-powered sentiment analysis',
  },
  {
    icon: <Calendar className="w-6 h-6 text-primary-600" />,
    title: 'Project Tracking',
    description: 'Visual timelines, task management, and AI predictions',
  },
  {
    icon: <DollarSign className="w-6 h-6 text-primary-600" />,
    title: 'Finance Manager',
    description: 'Create invoices, track payments, and budget alerts',
  },
  {
    icon: <ShoppingBag className="w-6 h-6 text-primary-600" />,
    title: 'Product Sourcing',
    description: 'AI-powered product search with budget tracking',
  },
  {
    icon: <MessageSquare className="w-6 h-6 text-primary-600" />,
    title: 'Marketing Assistant',
    description: 'Generate social media content with AI copywriting',
  },
];

// Pricing data
const pricingTiers = [
  {
    name: 'Free',
    price: 0,
    description: 'Perfect for trying out AI Studio',
    features: [
      '2 projects',
      '5 AI generations/month',
      'Client management',
      'Basic invoicing',
      'Email support',
    ],
    cta: 'Get Started',
    popular: false,
  },
  {
    name: 'Pro',
    price: 29,
    description: 'For professional designers',
    features: [
      'Unlimited projects',
      'Unlimited AI generations',
      'Marketing tools',
      'Product sourcing AI',
      'Priority support',
      'Export & sharing',
    ],
    cta: 'Start Pro Trial',
    popular: true,
  },
  {
    name: 'Agency',
    price: 79,
    description: 'For design teams',
    features: [
      'Everything in Pro',
      'Team collaboration',
      'Advanced analytics',
      'Custom branding',
      'API access',
      'Dedicated support',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

