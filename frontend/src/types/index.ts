/**
 * TypeScript Type Definitions
 * Defines all the data structures used throughout the application
 */

// User-related types
export interface User {
  id: number;
  name: string;
  email: string;
  role: 'designer' | 'admin';
  subscription_tier: 'free' | 'pro' | 'agency';
  ai_generations_used: number;
  ai_generations_limit: number;
  created_at: string;
}

// Client-related types
export interface Client {
  id: number;
  user_id: number;
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  style_preferences?: string;
  personality_profile?: Record<string, any>;
  budget_range?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  stats?: {
    active_projects: number;
    message_count: number;
    last_contact?: string;
  };
}

// Project-related types
export interface Project {
  id: number;
  user_id: number;
  client_id?: number;
  client_name?: string;
  title: string;
  description?: string;
  status: 'planning' | 'in_progress' | 'review' | 'completed' | 'on_hold';
  budget?: number;
  spent?: number;
  start_date?: string;
  deadline?: string;
  ai_insights?: Record<string, any>;
  created_at: string;
  updated_at: string;
  tasks?: Task[];
}

// Task-related types
export interface Task {
  id: number;
  project_id: number;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

// Design-related types
export interface Design {
  id: number;
  project_id: number;
  user_id: number;
  room_type: string;
  style: string;
  budget?: number;
  keywords?: string;
  image_urls: string[];
  color_palette: string[];
  description?: string;
  product_list: string[];
  created_at: string;
}

// Product-related types
export interface Product {
  id: number;
  project_id?: number;
  user_id: number;
  name: string;
  description?: string;
  price: number;
  vendor?: string;
  product_url?: string;
  image_url?: string;
  category?: string;
  style?: string;
  color?: string;
  is_purchased: boolean;
  created_at: string;
}

// Invoice-related types
export interface Invoice {
  id: number;
  user_id: number;
  project_id?: number;
  client_id?: number;
  client_name?: string;
  project_title?: string;
  invoice_number: string;
  type: 'invoice' | 'quote';
  amount: number;
  status: 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled';
  issue_date?: string;
  due_date?: string;
  paid_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Marketing content types
export interface MarketingContent {
  id: number;
  user_id: number;
  project_id?: number;
  project_title?: string;
  content_type: 'caption' | 'blog' | 'email' | 'post';
  platform?: string;
  title?: string;
  content: string;
  scheduled_date?: string;
  posted_date?: string;
  status: 'draft' | 'scheduled' | 'posted';
  created_at: string;
}

// Calendar event types
export interface CalendarEvent {
  id: number;
  user_id: number;
  project_id?: number;
  client_id?: number;
  client_name?: string;
  project_title?: string;
  title: string;
  description?: string;
  event_type: 'meeting' | 'deadline' | 'reminder' | 'automation';
  start_time: string;
  end_time?: string;
  location?: string;
  is_automated: boolean;
  reminder_sent: boolean;
  created_at: string;
}

// Dashboard statistics types
export interface DashboardStats {
  projects: {
    total_projects: number;
    active_projects: number;
    overdue_projects: number;
    total_budget: number;
    total_spent: number;
  };
  finances: {
    total_revenue: number;
    pending_payments: number;
    overdue_count: number;
    overdue_amount: number;
    pending_quotes: number;
  };
  clients: {
    total_count: number;
  };
  messages: {
    unread_count: number;
  };
  ai_usage: {
    used: number;
    limit: number;
    remaining: number;
  };
  subscription: {
    tier: string;
  };
  recent_activity: ActivityLog[];
}

// Activity log types
export interface ActivityLog {
  id: number;
  user_id: number;
  action: string;
  entity_type?: string;
  entity_id?: number;
  details?: Record<string, any>;
  created_at: string;
}

// Insight types for dashboard
export interface Insight {
  type: 'info' | 'warning' | 'alert' | 'success';
  title: string;
  message: string;
  action?: string;
  link?: string;
}

// API response types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Authentication types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials {
  name: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  message: string;
}

// Form state types
export interface FormState {
  isLoading: boolean;
  error: string | null;
  success: string | null;
}

// Pagination types
export interface PaginationParams {
  limit?: number;
  offset?: number;
}

// Filter types for various resources
export interface ProjectFilters {
  status?: Project['status'];
  client_id?: number;
}

export interface ProductFilters {
  project_id?: number;
  category?: string;
  style?: string;
  max_price?: number;
  vendor?: string;
}

export interface InvoiceFilters {
  status?: Invoice['status'];
  type?: Invoice['type'];
}

