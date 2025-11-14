'use client';

import { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import PolicyEditor from '../../components/PolicyEditor';
import { showToast } from '@/lib/toast';
import { useConfirmation } from '@/components/ConfirmationModal';
import { Plus, Search, FileText, Edit, Trash2, Eye, CheckCircle, AlertCircle, Clock } from 'lucide-react';

interface Policy {
  id: string;
  name: string;
  description: string;
  content: string;
  status: 'active' | 'inactive' | 'draft';
  created_at: string;
  updated_at: string;
  version?: string;
}

export default function PoliciesPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | undefined>();
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showEditor, setShowEditor] = useState(false);

  // Load policies
  useEffect(() => {
    loadPolicies();
  }, []);

  const loadPolicies = async () => {
    try {
      const response = await fetch('http://localhost:8001/policies/');
      if (!response.ok) throw new Error('Failed to load policies');
      
      const data = await response.json();
      setPolicies(data);
    } catch (error) {
      showToast.error('Failed to load policies');
      console.error('Load policies error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePolicy = async (policyData: Partial<Policy>) => {
    try {
      showToast.info('Saving policy...');
      
      const url = policyData.id 
        ? `http://localhost:8001/policies/${policyData.id}`
        : 'http://localhost:8001/policies/';
      
      const method = policyData.id ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(policyData)
      });
      
      if (!response.ok) throw new Error('Failed to save policy');
      
      showToast.success('Policy saved successfully');
      setShowEditor(false);
      setSelectedPolicy(undefined);
      loadPolicies(); // Reload list
    } catch (error) {
      showToast.error('Failed to save policy');
      console.error('Save policy error:', error);
    }
  };

  const handleTestPolicy = async (policyContent: string) => {
    try {
      showToast.info('Testing policy...');
      
      const response = await fetch('http://localhost:8001/policies/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: policyContent })
      });
      
      if (!response.ok) throw new Error('Failed to test policy');
      
      const result = await response.json();
      showToast.success('Policy test completed');
      return result;
    } catch (error) {
      showToast.error('Failed to test policy');
      console.error('Test policy error:', error);
      return null;
    }
  };

  const { confirm, ConfirmationComponent } = useConfirmation();

  const handleDeletePolicy = async (policyId: string) => {
    confirm({
      title: 'Delete Policy',
      message: 'Are you sure you want to delete this policy? This action cannot be undone.',
      onConfirm: async () => {
        try {
          showToast.info('Deleting policy...');
          
          const response = await fetch(`http://localhost:8001/policies/${policyId}`, {
            method: 'DELETE'
          });
          
          if (!response.ok) throw new Error('Failed to delete policy');
          
          showToast.success('Policy deleted successfully');
          await loadPolicies();
        } catch (error) {
          showToast.error('Failed to delete policy');
          console.error('Delete policy error:', error);
        }
      },
      confirmText: 'Delete',
      cancelText: 'Cancel',
      variant: 'danger'
  });
  };

  const handleEditPolicy = (policy: Policy) => {
    setSelectedPolicy(policy);
    setShowEditor(true);
  };

  const handleCreateNew = () => {
    setSelectedPolicy(undefined);
    setShowEditor(true);
  };

  const filteredPolicies = policies.filter(policy =>
    policy.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    policy.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'inactive':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      case 'draft':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'inactive':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (showEditor) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
        <div className="flex">
          {/* Sidebar */}
          <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden`}>
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(!sidebarOpen)} />
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <Header 
              title={selectedPolicy ? `Edit Policy: ${selectedPolicy.name}` : "Create New Policy"} 
              subtitle={
                <button
                  onClick={() => setShowEditor(false)}
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  ← Back to Policies
                </button>
              }
            />
            
            <main className="h-[calc(100vh-73px)]">
              <PolicyEditor
                policy={selectedPolicy}
                onSave={handleSavePolicy}
                onTest={handleTestPolicy}
              />
            </main>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
      <div className="flex">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden`}>
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(!sidebarOpen)} />
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <Header 
            title="Policy Management" 
            subtitle="Create and manage authorization policies"
          />
          
          <main className="p-6">
            {/* Actions Bar */}
            <div className="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <div className="flex flex-col sm:flex-row gap-4 flex-1 max-w-2xl">
                {/* Search */}
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search policies..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Create Button */}
              <button
                onClick={handleCreateNew}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                Create Policy
              </button>
            </div>

            {/* Policies List */}
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : filteredPolicies.length === 0 ? (
              <div className="text-center py-12">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No policies found</h3>
                <p className="text-gray-500 mb-4">
                  {searchTerm ? 'Try adjusting your search terms' : 'Get started by creating your first policy'}
                </p>
                {!searchTerm && (
                  <button
                    onClick={handleCreateNew}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                    Create Policy
                  </button>
                )}
              </div>
            ) : (
              <div className="grid gap-4">
                {filteredPolicies.map((policy) => (
                  <div key={policy.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">{policy.name}</h3>
                          <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(policy.status)}`}>
                            {getStatusIcon(policy.status)}
                            {policy.status.charAt(0).toUpperCase() + policy.status.slice(1)}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-3">{policy.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <span>Version: {policy.version || '1.0.0'}</span>
                          <span>Updated: {new Date(policy.updated_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2 ml-4">
                        <button
                          onClick={() => handleEditPolicy(policy)}
                          className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Edit policy"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeletePolicy(policy.id)}
                          className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete policy"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
      
      {/* Confirmation Modal */}
      <ConfirmationComponent />
    </div>
  );
}