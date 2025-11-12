'use client';

import { useState, useEffect } from 'react';
import { Plus, Search, Shield, Trash2, Edit, CheckCircle, XCircle, ExternalLink, Filter } from 'lucide-react';
import DashboardLayout from '../../components/DashboardLayout';
import ProtectedRoute from '../../components/ProtectedRoute';
import apiClient from '@/lib/api';

interface Resource {
  id: string;
  name: string;
  resource_type: string;
  application_id: string;
}

interface Action {
  id: string;
  resource_id: string;
  action_type: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface ActionWithResource extends Action {
  resource_name?: string;
  resource_type?: string;
}

export default function ActionsPage() {
  const [actions, setActions] = useState<ActionWithResource[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const [filterActive, setFilterActive] = useState<boolean | null>(null);
  const [filterResource, setFilterResource] = useState<string>('');

  // Form state
  const [formData, setFormData] = useState({
    resource_id: '',
    action_type: '',
    name: '',
    description: '',
    is_active: true
  });

  // Load actions and resources
  useEffect(() => {
    loadResources();
    loadActions();
  }, []);

  const loadResources = async () => {
    try {
      const data = await apiClient.get('/api/v1/resources/');
      setResources(data.resources || []);
    } catch (error) {
      console.error('Error loading resources:', error);
    }
  };

  const loadActions = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get('/api/v1/actions/');

      // Enrich actions with resource information
      const actionsWithResource = (data.actions || []).map((action: Action) => {
        const resource = resources.find(r => r.id === action.resource_id);
        return {
          ...action,
          resource_name: resource?.name || 'Unknown Resource',
          resource_type: resource?.resource_type || 'unknown'
        };
      });

      setActions(actionsWithResource);
    } catch (error) {
      console.error('Error loading actions:', error);
    } finally {
      setLoading(false);
    }
  };

  // Reload actions when resources change
  useEffect(() => {
    if (resources.length > 0) {
      loadActions();
    }
  }, [resources]);

  const handleCreateAction = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setCreating(true);
      await apiClient.post('/api/v1/actions/', formData);
      await loadActions();
      setShowCreateModal(false);
      setFormData({
        resource_id: '',
        action_type: '',
        name: '',
        description: '',
        is_active: true
      });
    } catch (error) {
      console.error('Error creating action:', error);
      alert('Failed to create action');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteAction = async (id: string) => {
    if (!confirm('Are you sure you want to delete this action?')) {
      return;
    }

    try {
      await apiClient.delete(`/api/v1/actions/${id}`);
      setActions(actions.filter(action => action.id !== id));
    } catch (error) {
      console.error('Error deleting action:', error);
      alert('Failed to delete action');
    }
  };

  const handleToggleActive = async (action: Action) => {
    try {
      const endpoint = action.is_active ? 'deactivate' : 'activate';
      await apiClient.request(`/api/v1/actions/${action.id}/${endpoint}`, {
        method: 'PATCH',
      });
      await loadActions();
    } catch (error) {
      console.error('Error updating action:', error);
      alert('Failed to update action status');
    }
  };

  // Filter actions
  const filteredActions = actions.filter(action => {
    const matchesSearch =
      action.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      action.action_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (action.resource_name && action.resource_name.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesActive = filterActive === null || action.is_active === filterActive;
    const matchesResource = !filterResource || action.resource_id === filterResource;

    return matchesSearch && matchesActive && matchesResource;
  });

  const getResourceInfo = (resourceId: string) => {
    const resource = resources.find(r => r.id === resourceId);
    return resource || { name: 'Unknown', resource_type: 'unknown' };
  };

  const getActionTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'read': 'bg-blue-100 text-blue-800',
      'write': 'bg-green-100 text-green-800',
      'delete': 'bg-red-100 text-red-800',
      'update': 'bg-yellow-100 text-yellow-800',
      'execute': 'bg-purple-100 text-purple-800',
      'manage': 'bg-indigo-100 text-indigo-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  return (
    <ProtectedRoute>
      <DashboardLayout>
        {/* Header */}
        <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Actions</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage all actions across resources
              </p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <Plus className="h-5 w-5 mr-2" />
              New Action
            </button>
          </div>

          {/* Search and Filters */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search actions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>

            <div className="flex gap-2">
              <select
                value={filterResource}
                onChange={(e) => setFilterResource(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">All Resources</option>
                {resources.map((resource) => (
                  <option key={resource.id} value={resource.id}>
                    {resource.name}
                  </option>
                ))}
              </select>

              <select
                value={filterActive === null ? '' : filterActive.toString()}
                onChange={(e) => setFilterActive(e.target.value === '' ? null : e.target.value === 'true')}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">All Status</option>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-4 flex gap-4 text-sm text-gray-600">
            <span>Total: {filteredActions.length}</span>
            <span>Active: {filteredActions.filter(a => a.is_active).length}</span>
            <span>Inactive: {filteredActions.filter(a => !a.is_active).length}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          </div>
        ) : filteredActions.length === 0 ? (
          <div className="text-center py-12">
            <Shield className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No actions</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new action.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredActions.map((action) => {
              const resourceInfo = getResourceInfo(action.resource_id);
              return (
                <div
                  key={action.id}
                  className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
                >
                  {/* Header */}
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {action.name}
                      </h3>
                      <p className="text-xs text-gray-500 font-mono mt-1">
                        {action.action_type}
                      </p>
                    </div>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleToggleActive(action)}
                        className={`p-1.5 rounded-md transition-colors ${
                          action.is_active
                            ? 'text-green-600 hover:bg-green-50'
                            : 'text-gray-400 hover:bg-gray-50'
                        }`}
                        title={action.is_active ? 'Deactivate' : 'Activate'}
                      >
                        {action.is_active ? (
                          <CheckCircle className="h-4 w-4" />
                        ) : (
                          <XCircle className="h-4 w-4" />
                        )}
                      </button>
                      <button
                        onClick={() => handleDeleteAction(action.id)}
                        className="p-1.5 rounded-md text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  {/* Description */}
                  {action.description && (
                    <p className="text-sm text-gray-600 mb-3">
                      {action.description}
                    </p>
                  )}

                  {/* Badges */}
                  <div className="flex flex-wrap gap-2 mb-3">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActionTypeColor(action.action_type)}`}>
                      {action.action_type}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      action.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {action.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>

                  {/* Resource Info */}
                  <div className="pt-3 border-t border-gray-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <p className="text-xs text-gray-500">Resource</p>
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {resourceInfo.name}
                        </p>
                        <p className="text-xs text-gray-500 font-mono truncate">
                          {resourceInfo.resource_type}
                        </p>
                      </div>
                      <a
                        href={`/resources`}
                        className="text-indigo-600 hover:text-indigo-900 p-1"
                        title="View Resource"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>
                  </div>

                  {/* Timestamps */}
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="text-xs text-gray-400">
                      Created: {new Date(action.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">
                Create New Action
              </h3>
            </div>

            <form onSubmit={handleCreateAction} className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Resource *
                  </label>
                  <select
                    required
                    value={formData.resource_id}
                    onChange={(e) => setFormData({ ...formData, resource_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">Select a resource</option>
                    {resources.map((resource) => (
                      <option key={resource.id} value={resource.id}>
                        {resource.name} ({resource.resource_type})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Action Type *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.action_type}
                    onChange={(e) => setFormData({ ...formData, action_type: e.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, '-') })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-mono"
                    placeholder="read"
                    list="action-types"
                  />
                  <datalist id="action-types">
                    <option value="read" />
                    <option value="write" />
                    <option value="update" />
                    <option value="delete" />
                    <option value="execute" />
                    <option value="manage" />
                  </datalist>
                  <p className="mt-1 text-xs text-gray-500">
                    Common types: read, write, update, delete, execute, manage
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Read Access"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Brief description of this action"
                  />
                </div>
              </div>

              <div className="mt-6 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  disabled={creating}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                  disabled={creating}
                >
                  {creating ? 'Creating...' : 'Create Action'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      </DashboardLayout>
    </ProtectedRoute>
  );
}
