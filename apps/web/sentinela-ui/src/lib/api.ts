const TOKEN_KEY = 'sentinela_token';

class APIClient {
  private token: string = '';

  constructor() {
    // Initialize token from localStorage on creation
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (storedToken) {
        this.token = storedToken;
      }
    }
  }

  setToken(token: string) {
    this.token = token;
  }

  getToken(): string {
    // Always check localStorage for latest token
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (storedToken) {
        this.token = storedToken;
      }
    }
    return this.token;
  }

  async request(endpoint: string, options: RequestInit & { params?: Record<string, any> } = {}) {
    // Use Business API for auth endpoints, Policy API for others
    let baseUrl;
    if (endpoint.includes('/auth/')) {
      baseUrl = process.env.NEXT_PUBLIC_BUSINESS_API_URL || 'http://localhost:8002';
    } else {
      baseUrl = process.env.NEXT_PUBLIC_POLICY_API_URL || 'http://localhost:8001';
    }

    // Build URL with query params if provided
    let url = `${baseUrl}${endpoint}`;
    if (options.params) {
      const queryParams = new URLSearchParams();
      Object.entries(options.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, String(value));
        }
      });
      const queryString = queryParams.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    // Get fresh token from localStorage on every request
    const currentToken = this.getToken();

    const { params, ...fetchOptions } = options;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(currentToken && { Authorization: `Bearer ${currentToken}` }),
        ...fetchOptions.headers,
      },
      ...fetchOptions,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Error Response:', errorData);
        throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('API Success Response:', data);
      return data;
    } catch (error) {
      console.error('API Request Failed:', error);
      throw error;
    }
  }

  async get(endpoint: string, options?: { params?: Record<string, any> }) {
    return this.request(endpoint, { method: 'GET', ...options });
  }

  async post(endpoint: string, data?: any, options?: { params?: Record<string, any> }) {
    return this.request(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });
  }

  async put(endpoint: string, data?: any, options?: { params?: Record<string, any> }) {
    return this.request(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });
  }

  async delete(endpoint: string, options?: { params?: Record<string, any> }) {
    return this.request(endpoint, { method: 'DELETE', ...options });
  }
}

const apiClient = new APIClient();
export default apiClient;