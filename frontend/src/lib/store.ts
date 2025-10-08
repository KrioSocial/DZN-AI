/**
 * Global State Management with Zustand
 * Manages application-wide state including user, theme, and UI states
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';

/**
 * Authentication Store
 * Manages user authentication state
 */
interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      
      // Set user and mark as authenticated
      setUser: (user) =>
        set({
          user,
          isAuthenticated: !!user,
        }),
      
      // Clear user and mark as not authenticated
      logout: () =>
        set({
          user: null,
          isAuthenticated: false,
        }),
    }),
    {
      name: 'auth-storage', // localStorage key
      // Only persist user data, not the whole state
      partialize: (state) => ({ user: state.user }),
    }
  )
);

/**
 * UI Store
 * Manages UI-related state like sidebar, modals, etc.
 */
interface UIStore {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  
  // Set sidebar open/closed
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  
  // Toggle sidebar state
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));

/**
 * Loading Store
 * Manages loading states for different operations
 */
interface LoadingStore {
  isLoading: Record<string, boolean>;
  setLoading: (key: string, loading: boolean) => void;
  isOperationLoading: (key: string) => boolean;
}

export const useLoadingStore = create<LoadingStore>((set, get) => ({
  isLoading: {},
  
  // Set loading state for a specific operation
  setLoading: (key, loading) =>
    set((state) => ({
      isLoading: { ...state.isLoading, [key]: loading },
    })),
  
  // Check if a specific operation is loading
  isOperationLoading: (key) => get().isLoading[key] || false,
}));

