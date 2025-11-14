'use client';

import { useState, useEffect } from 'react';
import { Plus, Search, Shield, Trash2, Edit, CheckCircle, XCircle } from 'lucide-react';
import DashboardLayout from '../../components/DashboardLayout';
import ProtectedRoute from '../../components/ProtectedRoute';
import apiClient from '@/lib/api';
import { showToast } from '@/lib/toast';
import { PageLoader, CardSkeleton, LoadingButton } from '@/components/LoadingStates';
import { ConfirmationModal } from '@/components/ConfirmationModal';

interface Application {
  id: string;
  name: string;
  slug: string;
}

interface Resource {
  id: string;
  application_id: string;
  resource_type: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  actions_count: number;
}

interface Action {
  id: string;
  resource_id: string;
  action_type: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
}

export default function ResourcesPage() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const [selectedResource, setSelectedResource] = useState<string | null>(null);
  const [actions, setActions] = useState<{ [key: string]: Action[] }>({});
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [resourceToDelete, setResourceToDelete] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    application_id: '',
    resource_type: '',
    name: '',
    description: '',
    is_active: true
  });

  // Load resources and applications
  useEffect(() => {
    loadApplications();
    loadResources();
  }, []);

  const loadApplications = async () => {
    try {
      const data = await apiClient.get('/api/v1/applications/');
      setApplications(data.applications || []);
    } catch (error) {
      showToast.error('Failed to load applications');
    }
  };

  const loadResources = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get('/api/v1/resources/');
      setResources(data.resources || []);
    } catch (error) {
      showToast.error('Failed to load resources');
    } finally {
      setLoading(false);
    }
  };

  const loadActions = async (resourceId: string) => {
    try {
      const data = await apiClient.get(`/api/v1/actions/?resource_id=${resourceId}`);
      setActions(prev => ({ ...prev, [resourceId]: data.actions || [] }));
    } catch (error) {
      showToast.error('Failed to load actions');
    }
  };

  const handleCreateResource = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setCreating(true);
      await apiClient.post('/api/v1/resources/', formData);
      await loadResources();
      setShowCreateModal(false);
      setFormData({
        application_id: '',
        resource_type: '',
        name: '',
        description: '',
        is_active: true
      });
      showToast.success('Resource created successfully');
    } catch (error) {
      showToast.error('Failed to create resource');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteResource = (id: string) => {
    setResourceToDelete(id);
    setShowDeleteModal(true);
  };

  const confirmDeleteResource = async () => {
    if (!resourceToDelete) return;

    try {
      setDeleting(true);
      await apiClient.delete(`/api/v1/resources/${resourceToDelete}`);
      setResources(resources.filter(res => res.id !== resourceToDelete));
      showToast.success('Resource deleted successfully');
      setShowDeleteModal(false);
      setResourceToDelete(null);
    } catch (error) {
      showToast.error('Failed to delete resource');
    } finally {
      setDeleting(false);
    }
  };

  const toggleResourceExpand = async (resourceId: string) => {
    if (selectedResource === resourceId) {
      setSelectedResource(null);
    } else {
      setSelectedResource(resourceId);
      if (!actions[resourceId]) {
        await loadActions(resourceId);
      }
    }
  };

  // Filter resources
  const filteredResources = resources.filter(res =>
    res.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    res.resource_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getApplicationName = (appId: string) => {
    const app = applications.find(a => a.id === appId);
    return app ? app.name : 'Unknown';
  };

  return (
    <DashboardLayout>
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Resources</h1>
              <p className="mt-1 text-sm text-gray-500">
                Define resources and their associated actions
              </p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <Plus className="h-5 w-5 mr-2" />
              New Resource
            </button>
          </div>

          {/* Search */}
          <div className="mt-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search resources..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <PageLoader />
        ) : filteredResources.length === 0 ? (
          <div className="text-center py-12">
            <Shield className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No resources</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new resource.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredResources.map((resource) => (
              <div
                key={resource.id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
              >
                {/* Resource Header */}
                <div className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {resource.name}
                        </h3>
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          resource.is_active
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {resource.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 font-mono mt-1">
                        {resource.resource_type}
                      </p>
                      <p className="text-sm text-gray-600 mt-2">
                        {resource.description || 'No description'}
                      </p>
                      <p className="text-xs text-gray-500 mt-2">
                        Application: {getApplicationName(resource.application_id)}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => toggleResourceExpand(resource.id)}
                        className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                      >
                        {selectedResource === resource.id ? 'Hide' : 'Show'} Actions ({resource.actions_count})
                      </button>
                      <button
                        onClick={() => handleDeleteResource(resource.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>

                {/* Actions List */}
                {selectedResource === resource.id && (
                  <div className="border-t border-gray-200 bg-gray-50 px-6 py-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-3">Actions</h4>
                    {actions[resource.id] && actions[resource.id].length > 0 ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {actions[resource.id].map((action) => (
                          <div
                            key={action.id}
                            className="bg-white rounded-md border border-gray-200 p-3"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <p className="text-sm font-medium text-gray-900">{action.name}</p>
                                <p className="text-xs text-gray-500 font-mono mt-1">{action.action_type}</p>
                              </div>
                              {action.is_active ? (
                                <CheckCircle className="h-4 w-4 text-green-600" />
                              ) : (
                                <XCircle className="h-4 w-4 text-gray-400" />
                              )}
                            </div>
                            {action.description && (
                              <p className="text-xs text-gray-600 mt-2">{action.description}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">No actions defined</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">
                Create New Resource
              </h3>
            </div>

            <form onSubmit={handleCreateResource} className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Application *
                  </label>
                  <select
                    required
                    value={formData.application_id}
                    onChange={(e) => setFormData({ ...formData, application_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">Select an application</option>
                    {applications.map((app) => (
                      <option key={app.id} value={app.id}>
                        {app.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Resource Type *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.resource_type}
                    onChange={(e) => setFormData({ ...formData, resource_type: e.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, '-') })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-mono"
                    placeholder="users"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Lowercase letters, numbers, underscores, and hyphens only
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
                    placeholder="User Management"
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
                    placeholder="Brief description of this resource"
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
                 <LoadingButton
                   type="submit"
                   loading={creating}
                   className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
                 >
                   {creating ? '' : 'Create Resource'}
                 </LoadingButton>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={() => {
          if (!deleting) {
            setShowDeleteModal(false);
            setResourceToDelete(null);
          }
        }}
        onConfirm={confirmDeleteResource}
        title="Delete Resource"
        message="Are you sure you want to delete this resource? This will also delete all associated actions. This action cannot be undone."
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </DashboardLayout>
  );
}
