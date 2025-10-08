/**
 * API Client Library
 * Handles all HTTP requests to the Flask backend with authentication
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';
import type { 
  User, Client, Project, Design, Product, Invoice, 
  MarketingContent, CalendarEvent, DashboardStats, AuthResponse 
} from '@/types';

// Base API URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

/**
 * Create configured axios instance with interceptors
 */
class ApiClient {
  private client: AxiosInstance;

  constructor() {
    // Create axios instance with base configuration
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 second timeout
    });

    // Add request interceptor to attach JWT token
    this.client.interceptors.request.use(
      (config) => {
        // Get token from localStorage
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        // Handle 401 Unauthorized errors
        if (error.response?.status === 401) {
          // Clear authentication and redirect to login
          this.clearAuth();
          if (typeof window !== 'undefined') {
            window.location.href = '/auth/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Get JWT token from localStorage
   */
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  /**
   * Save authentication data to localStorage
   */
  private saveAuth(token: string, refreshToken: string, user: User): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
      localStorage.setItem('refresh_token', refreshToken);
      localStorage.setItem('user', JSON.stringify(user));
    }
  }

  /**
   * Clear authentication data from localStorage
   */
  private clearAuth(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  }

  // ==================
  // AUTHENTICATION APIs
  // ==================

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/auth/login', {
      email,
      password,
    });
    
    // Save authentication data
    this.saveAuth(
      response.data.access_token,
      response.data.refresh_token,
      response.data.user
    );
    
    return response.data;
  }

  async signup(name: string, email: string, password: string): Promise<{ message: string }> {
    const response = await this.client.post('/auth/register', {
      name,
      email,
      password,
    });
    return response.data;
  }

  async getProfile(): Promise<{ user: User; stats: any }> {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  logout(): void {
    this.clearAuth();
  }

  // ==================
  // DASHBOARD APIs
  // ==================

  async getDashboardOverview(): Promise<{ dashboard: DashboardStats }> {
    const response = await this.client.get('/dashboard/overview');
    return response.data;
  }

  async getDashboardInsights(): Promise<{ insights: any[] }> {
    const response = await this.client.get('/dashboard/insights');
    return response.data;
  }

  // ==================
  // CLIENT APIs
  // ==================

  async getClients(params?: { limit?: number; offset?: number; search?: string }): Promise<{ clients: Client[]; count: number }> {
    const response = await this.client.get('/clients', { params });
    return response.data;
  }

  async getClient(id: number): Promise<{ client: Client }> {
    const response = await this.client.get(`/clients/${id}`);
    return response.data;
  }

  async createClient(data: Partial<Client>): Promise<{ client: Client; message: string }> {
    const response = await this.client.post('/clients', data);
    return response.data;
  }

  async updateClient(id: number, data: Partial<Client>): Promise<{ message: string }> {
    const response = await this.client.put(`/clients/${id}`, data);
    return response.data;
  }

  async deleteClient(id: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/clients/${id}`);
    return response.data;
  }

  // ==================
  // PROJECT APIs
  // ==================

  async getProjects(params?: { status?: string; limit?: number; offset?: number }): Promise<{ projects: Project[]; count: number }> {
    const response = await this.client.get('/projects', { params });
    return response.data;
  }

  async getProject(id: number): Promise<{ project: Project }> {
    const response = await this.client.get(`/projects/${id}`);
    return response.data;
  }

  async createProject(data: Partial<Project>): Promise<{ project: Project; message: string }> {
    const response = await this.client.post('/projects', data);
    return response.data;
  }

  async updateProject(id: number, data: Partial<Project>): Promise<{ message: string }> {
    const response = await this.client.put(`/projects/${id}`, data);
    return response.data;
  }

  async deleteProject(id: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/projects/${id}`);
    return response.data;
  }

  async generateProjectInsights(id: number): Promise<{ insights: any; message: string }> {
    const response = await this.client.post(`/projects/${id}/ai-insights`);
    return response.data;
  }

  // ==================
  // DESIGN APIs
  // ==================

  async getDesigns(params?: { project_id?: number; limit?: number }): Promise<{ designs: Design[]; count: number }> {
    const response = await this.client.get('/designs', { params });
    return response.data;
  }

  async getDesign(id: number): Promise<{ design: Design }> {
    const response = await this.client.get(`/designs/${id}`);
    return response.data;
  }

  async generateDesign(data: {
    project_id: number;
    room_type: string;
    style: string;
    budget?: number;
    keywords?: string;
  }): Promise<{ design: Design; message: string }> {
    const response = await this.client.post('/designs/generate', data);
    return response.data;
  }

  async deleteDesign(id: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/designs/${id}`);
    return response.data;
  }

  // ==================
  // PRODUCT APIs
  // ==================

  async getProducts(params?: any): Promise<{ products: Product[]; count: number }> {
    const response = await this.client.get('/products', { params });
    return response.data;
  }

  async createProduct(data: Partial<Product>): Promise<{ product: Product; message: string }> {
    const response = await this.client.post('/products', data);
    return response.data;
  }

  async updateProduct(id: number, data: Partial<Product>): Promise<{ message: string }> {
    const response = await this.client.put(`/products/${id}`, data);
    return response.data;
  }

  async deleteProduct(id: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/products/${id}`);
    return response.data;
  }

  // ==================
  // INVOICE APIs
  // ==================

  async getInvoices(params?: any): Promise<{ invoices: Invoice[]; count: number }> {
    const response = await this.client.get('/invoices', { params });
    return response.data;
  }

  async createInvoice(data: Partial<Invoice>): Promise<{ invoice: Invoice; message: string }> {
    const response = await this.client.post('/invoices', data);
    return response.data;
  }

  async updateInvoice(id: number, data: Partial<Invoice>): Promise<{ message: string }> {
    const response = await this.client.put(`/invoices/${id}`, data);
    return response.data;
  }

  async getFinancialSummary(): Promise<{ summary: any }> {
    const response = await this.client.get('/invoices/summary');
    return response.data;
  }

  // ==================
  // MARKETING APIs
  // ==================

  async getMarketingContent(params?: any): Promise<{ content: MarketingContent[]; count: number }> {
    const response = await this.client.get('/marketing', { params });
    return response.data;
  }

  async generateMarketingContent(data: {
    content_type: string;
    project_id?: number;
    platform?: string;
    title?: string;
  }): Promise<{ content: MarketingContent; message: string }> {
    const response = await this.client.post('/marketing/generate', data);
    return response.data;
  }

  // ==================
  // CALENDAR APIs
  // ==================

  async getCalendarEvents(params?: any): Promise<{ events: CalendarEvent[]; count: number }> {
    const response = await this.client.get('/calendar/events', { params });
    return response.data;
  }

  async createCalendarEvent(data: Partial<CalendarEvent>): Promise<{ event: CalendarEvent; message: string }> {
    const response = await this.client.post('/calendar/events', data);
    return response.data;
  }
}

// Export singleton instance
export const api = new ApiClient();

