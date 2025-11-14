import apiClient from './api';

const TOKEN_KEY = 'sentinela_token';
const USER_KEY = 'sentinela_user';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface User {
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  groups: string[];
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

class AuthService {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await apiClient.post('/api/v1/auth/login', credentials);

      // Store token and user data
      this.setToken(response.access_token);
      this.setUser(response.user);

      // Configure API client with the token
      apiClient.setToken(response.access_token);

      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw new Error('Invalid email or password');
    }
  }

  /**
   * Logout user
   */
  logout(): void {
    this.removeToken();
    this.removeUser();
    apiClient.setToken('');
  }

  /**
   * Get current authenticated user from API
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const token = this.getToken();
      if (!token) {
        return null;
      }

      // Configure API client with token
      apiClient.setToken(token);

      const response = await apiClient.get('/api/v1/auth/me');
      this.setUser(response);
      return response;
    } catch (error) {
      console.error('Get current user error:', error);
      this.logout();
      return null;
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    // Check if token is expired (basic check)
    try {
      const payload = this.decodeToken(token);
      const now = Math.floor(Date.now() / 1000);
      return payload.exp > now;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    if (typeof window === 'undefined') {
      return null;
    }
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Store token
   */
  private setToken(token: string): void {
    if (typeof window === 'undefined') {
      return;
    }
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Remove token
   */
  private removeToken(): void {
    if (typeof window === 'undefined') {
      return;
    }
    localStorage.removeItem(TOKEN_KEY);
  }

  /**
   * Get stored user
   */
  getUser(): User | null {
    if (typeof window === 'undefined') {
      return null;
    }
    const userJson = localStorage.getItem(USER_KEY);
    if (!userJson) {
      return null;
    }
    try {
      return JSON.parse(userJson);
    } catch (error) {
      return null;
    }
  }

  /**
   * Store user
   */
  private setUser(user: User): void {
    if (typeof window === 'undefined') {
      return;
    }
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Remove user
   */
  private removeUser(): void {
    if (typeof window === 'undefined') {
      return;
    }
    localStorage.removeItem(USER_KEY);
  }

  /**
   * Decode JWT token (without verification - just for reading payload)
   */
  private decodeToken(token: string): any {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (error) {
      throw new Error('Invalid token format');
    }
  }

  /**
   * Initialize auth state from localStorage
   */
  initializeAuth(): void {
    const token = this.getToken();
    if (token && this.isAuthenticated()) {
      apiClient.setToken(token);
    } else {
      this.logout();
    }
  }
}

const authService = new AuthService();
export default authService;
