/**
 * Keycloak API Client
 * Handles all Keycloak user and group management operations
 */

import apiClient from './api';

export interface KeycloakUser {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  enabled: boolean;
  emailVerified: boolean;
  createdTimestamp?: number;
}

export interface CreateUserRequest {
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  password: string;
  enabled?: boolean;
  emailVerified?: boolean;
  temporaryPassword?: boolean;
}

export interface UpdateUserRequest {
  email?: string;
  firstName?: string;
  lastName?: string;
  enabled?: boolean;
}

export interface KeycloakGroup {
  id: string;
  name: string;
  path: string;
  subGroups?: any[];
  attributes?: Record<string, string[]>;
}

export interface CreateGroupRequest {
  name: string;
  path?: string;
  attributes?: Record<string, string[]>;
}

export interface UserListResponse {
  users: KeycloakUser[];
  total: number;
  page: number;
  perPage: number;
}

export interface GroupListResponse {
  groups: KeycloakGroup[];
  total: number;
  page: number;
  perPage: number;
}

export interface UserStats {
  totalUsers: number;
  activeUsers: number;
  inactiveUsers: number;
}

export interface GroupStats {
  totalGroups: number;
}

class KeycloakAPI {
  // ==================== USER OPERATIONS ====================

  /**
   * List users with pagination and filters
   */
  async listUsers(params: {
    page?: number;
    perPage?: number;
    search?: string;
    email?: string;
    username?: string;
    enabled?: boolean;
  } = {}): Promise<UserListResponse> {
    const response = await apiClient.get('/api/v1/keycloak/users', { params });
    return response;
  }

  /**
   * Get user by ID
   */
  async getUser(userId: string): Promise<KeycloakUser> {
    const response = await apiClient.get(`/api/v1/keycloak/users/${userId}`);
    return response;
  }

  /**
   * Create a new user
   */
  async createUser(data: CreateUserRequest): Promise<{ id: string; message: string }> {
    const response = await apiClient.post('/api/v1/keycloak/users', data);
    return response;
  }

  /**
   * Update user information
   */
  async updateUser(userId: string, data: UpdateUserRequest): Promise<{ message: string }> {
    const response = await apiClient.put(`/api/v1/keycloak/users/${userId}`, data);
    return response;
  }

  /**
   * Delete a user
   */
  async deleteUser(userId: string): Promise<{ message: string }> {
    const response = await apiClient.delete(`/api/v1/keycloak/users/${userId}`);
    return response;
  }

  /**
   * Reset user password
   */
  async resetPassword(userId: string, newPassword: string, temporary: boolean = false): Promise<{ message: string }> {
    const response = await apiClient.post(
      `/api/v1/keycloak/users/${userId}/reset-password`,
      { newPassword, temporary }
    );
    return response;
  }

  /**
   * Get user groups
   */
  async getUserGroups(userId: string): Promise<{ groups: KeycloakGroup[] }> {
    const response = await apiClient.get(`/api/v1/keycloak/users/${userId}/groups`);
    return response;
  }

  /**
   * Get user statistics
   */
  async getUserStats(): Promise<UserStats> {
    const response = await apiClient.get('/api/v1/keycloak/users/stats/summary');
    return response;
  }

  // ==================== GROUP OPERATIONS ====================

  /**
   * List groups with pagination and filters
   */
  async listGroups(params: {
    page?: number;
    perPage?: number;
    search?: string;
  } = {}): Promise<GroupListResponse> {
    const response = await apiClient.get('/api/v1/keycloak/groups', { params });
    return response;
  }

  /**
   * Get group by ID
   */
  async getGroup(groupId: string): Promise<KeycloakGroup> {
    const response = await apiClient.get(`/api/v1/keycloak/groups/${groupId}`);
    return response;
  }

  /**
   * Create a new group
   */
  async createGroup(data: CreateGroupRequest): Promise<{ id: string; message: string }> {
    const response = await apiClient.post('/api/v1/keycloak/groups', data);
    return response;
  }

  /**
   * Update group information
   */
  async updateGroup(groupId: string, data: { name?: string; attributes?: Record<string, string[]> }): Promise<{ message: string }> {
    const response = await apiClient.put(`/api/v1/keycloak/groups/${groupId}`, data);
    return response;
  }

  /**
   * Delete a group
   */
  async deleteGroup(groupId: string): Promise<{ message: string }> {
    const response = await apiClient.delete(`/api/v1/keycloak/groups/${groupId}`);
    return response;
  }

  /**
   * Get group members
   */
  async getGroupMembers(groupId: string, params: { page?: number; perPage?: number } = {}): Promise<{ members: KeycloakUser[]; total: number }> {
    const response = await apiClient.get(`/api/v1/keycloak/groups/${groupId}/members`, { params });
    return response;
  }

  /**
   * Add user to group
   */
  async addUserToGroup(groupId: string, userId: string): Promise<{ message: string }> {
    const response = await apiClient.post(`/api/v1/keycloak/groups/${groupId}/members/${userId}`);
    return response;
  }

  /**
   * Remove user from group
   */
  async removeUserFromGroup(groupId: string, userId: string): Promise<{ message: string }> {
    const response = await apiClient.delete(`/api/v1/keycloak/groups/${groupId}/members/${userId}`);
    return response;
  }

  /**
   * Get group statistics
   */
  async getGroupStats(): Promise<GroupStats> {
    const response = await apiClient.get('/api/v1/keycloak/groups/stats/summary');
    return response;
  }
}

const keycloakAPI = new KeycloakAPI();
export default keycloakAPI;
