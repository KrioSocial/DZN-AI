/**
 * Dashboard Home Page
 * Main dashboard with statistics, insights, and recent activity
 */

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, Users, Briefcase, DollarSign, AlertCircle,
  Plus, Sparkles, Calendar, ArrowRight
} from 'lucide-react';
import { api } from '@/lib/api';
import { formatCurrency, formatRelativeTime } from '@/lib/utils';
import type { DashboardStats, Insight } from '@/types';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);

  /**
   * Load dashboard data on mount
   */
  useEffect(() => {
    loadDashboard();
  }, []);

  /**
   * Fetch dashboard data from API
   */
  const loadDashboard = async () => {
    try {
      setLoading(true);
      const [dashboardData, insightsData] = await Promise.all([
        api.getDashboardOverview(),
        api.getDashboardInsights(),
      ]);
      
      setStats(dashboardData.dashboard);
      setInsights(insightsData.insights || []);
    } catch (error) {
      toast.error('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Overview of your design studio</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {loading ? (
          // Loading skeletons
          Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="stat-card">
              <div className="skeleton h-12 w-12 rounded-lg mb-4"></div>
              <div className="skeleton h-8 w-24 mb-2"></div>
              <div className="skeleton h-4 w-32"></div>
            </div>
          ))
        ) : (
          <>
            {/* Active Projects */}
            <StatsCard
              icon={<Briefcase className="w-6 h-6 text-primary-600" />}
              label="Active Projects"
              value={stats?.projects.active_projects || 0}
              trend="+2 this month"
              trendUp
            />

            {/* Total Clients */}
            <StatsCard
              icon={<Users className="w-6 h-6 text-purple-600" />}
              label="Total Clients"
              value={stats?.clients.total_count || 0}
              trend="All time"
            />

            {/* Total Revenue */}
            <StatsCard
              icon={<DollarSign className="w-6 h-6 text-green-600" />}
              label="Total Revenue"
              value={formatCurrency(stats?.finances.total_revenue || 0)}
              trend="+15% vs last month"
              trendUp
            />

            {/* Overdue Projects */}
            <StatsCard
              icon={<AlertCircle className="w-6 h-6 text-red-600" />}
              label="Overdue Projects"
              value={stats?.projects.overdue_projects || 0}
              trend="Need attention"
              trendUp={false}
            />
          </>
        )}
      </div>

      {/* AI Insights */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-amber-500" />
            AI Insights
          </h2>
          <button
            onClick={loadDashboard}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="skeleton h-24 rounded-lg"></div>
        ) : insights.length > 0 ? (
          <div className="space-y-3">
            {insights.map((insight, index) => (
              <InsightCard key={index} insight={insight} />
            ))}
          </div>
        ) : (
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <h4 className="font-semibold text-blue-900">Welcome to AI Studio!</h4>
                <p className="text-sm text-blue-700 mt-1">
                  Get started by creating your first project or generating an AI design concept.
                </p>
              </div>
              <Link
                href="/dashboard/projects?action=new"
                className="btn btn-sm btn-primary"
              >
                Get Started
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickActionCard
            icon={<Plus className="w-5 h-5" />}
            label="New Project"
            href="/dashboard/projects?action=new"
          />
          <QuickActionCard
            icon={<Users className="w-5 h-5" />}
            label="Add Client"
            href="/dashboard/clients?action=new"
          />
          <QuickActionCard
            icon={<Sparkles className="w-5 h-5" />}
            label="Generate Design"
            href="/dashboard/designs?action=generate"
            featured
          />
          <QuickActionCard
            icon={<DollarSign className="w-5 h-5" />}
            label="Create Invoice"
            href="/dashboard/invoices?action=new"
          />
        </div>
      </div>

      {/* Recent Activity & Upcoming Events */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Recent Projects */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Recent Projects</h2>
            <Link href="/dashboard/projects" className="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="text-center py-8 text-gray-500">
            <Briefcase className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No projects yet</p>
            <Link href="/dashboard/projects?action=new" className="btn btn-primary btn-sm mt-4">
              Create Project
            </Link>
          </div>
        </div>

        {/* Upcoming Events */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Upcoming Events</h2>
            <Link href="/dashboard/calendar" className="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
              View Calendar <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="text-center py-8 text-gray-500">
            <Calendar className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No upcoming events</p>
            <Link href="/dashboard/calendar?action=new" className="btn btn-primary btn-sm mt-4">
              Add Event
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

// Stats Card Component
function StatsCard({
  icon,
  label,
  value,
  trend,
  trendUp,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  trend?: string;
  trendUp?: boolean;
}) {
  return (
    <div className="stat-card">
      <div className="flex items-start justify-between">
        <div className="p-3 bg-gray-50 rounded-lg">{icon}</div>
        {trend && trendUp !== undefined && (
          <TrendingUp
            className={`w-5 h-5 ${trendUp ? 'text-green-500' : 'text-gray-400'}`}
          />
        )}
      </div>
      <div className="mt-4">
        <div className="text-3xl font-bold text-gray-900">{value}</div>
        <div className="text-sm text-gray-600 mt-1">{label}</div>
        {trend && (
          <div className={`text-xs mt-2 ${trendUp ? 'text-green-600' : 'text-gray-500'}`}>
            {trend}
          </div>
        )}
      </div>
    </div>
  );
}

// Insight Card Component
function InsightCard({ insight }: { insight: Insight }) {
  const colorClasses = {
    info: 'bg-blue-50 border-blue-500 text-blue-900',
    warning: 'bg-yellow-50 border-yellow-500 text-yellow-900',
    alert: 'bg-red-50 border-red-500 text-red-900',
    success: 'bg-green-50 border-green-500 text-green-900',
  };

  return (
    <div className={`border-l-4 p-4 rounded ${colorClasses[insight.type]}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <h4 className="font-semibold">{insight.title}</h4>
          <p className="text-sm mt-1 opacity-90">{insight.message}</p>
        </div>
        {insight.action && insight.link && (
          <Link href={insight.link} className="btn btn-sm btn-secondary flex-shrink-0">
            {insight.action}
          </Link>
        )}
      </div>
    </div>
  );
}

// Quick Action Card Component
function QuickActionCard({
  icon,
  label,
  href,
  featured,
}: {
  icon: React.ReactNode;
  label: string;
  href: string;
  featured?: boolean;
}) {
  return (
    <Link
      href={href}
      className={`flex flex-col items-center justify-center p-6 rounded-lg border-2 transition-all hover:scale-105 ${
        featured
          ? 'bg-gradient-to-br from-primary-600 to-purple-600 text-white border-transparent'
          : 'bg-gray-50 border-gray-200 hover:border-primary-300'
      }`}
    >
      <div className={`mb-3 ${featured ? 'text-white' : 'text-primary-600'}`}>
        {icon}
      </div>
      <span className={`text-sm font-medium text-center ${featured ? 'text-white' : 'text-gray-900'}`}>
        {label}
      </span>
    </Link>
  );
}

