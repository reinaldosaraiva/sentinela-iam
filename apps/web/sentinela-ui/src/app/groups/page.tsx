'use client';

import { useState, useEffect } from 'react';
import { Users, Plus, Search, Shield, Trash2, Edit2 } from 'lucide-react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import { Spinner } from '@/components/LoadingStates';

interface Group {
  id: string;
  name: string;
  description: string;
  memberCount: number;
  createdAt: string;
}

export default function GroupsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [groups, setGroups] = useState<Group[]>([
    {
      id: '1',
      name: 'Administrators',
      description: 'System administrators with full access',
      memberCount: 3,
      createdAt: '2025-01-10'
    },
    {
      id: '2',
      name: 'Employees',
      description: 'Regular employees with standard access',
      memberCount: 25,
      createdAt: '2025-01-12'
    },
    {
      id: '3',
      name: 'Managers',
      description: 'Department managers with elevated permissions',
      memberCount: 8,
      createdAt: '2025-01-15'
    }
  ]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('sentinela_token');
    if (!token) {
      window.location.href = '/login';
    } else {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Spinner size="lg" />
          <div className="text-white text-xl">Loading...</div>
        </div>
      </div>
    );
  }

  const filteredGroups = groups.filter(group =>
    group.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    group.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
      <div className="flex">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 ease-in-out overflow-hidden`}>
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(!sidebarOpen)} />
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <Header
            title="Groups Management"
            subtitle="Manage user groups and permissions"
          />

          <main className="p-8 animate-fade-in">
            {/* Header Actions */}
            <div className="mb-8 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Groups</h2>
                <p className="text-slate-600 mt-1">Organize users into groups for easier permission management</p>
              </div>
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-500/25 hover:shadow-xl"
              >
                <Plus className="h-4 w-4 mr-2" />
                Create Group
              </button>
            </div>

            {/* Search */}
            <div className="mb-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search groups..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            {/* Groups Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map((group) => (
                <div
                  key={group.id}
                  className="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg transition-all group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/25">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-2 hover:bg-slate-100 rounded-lg transition-colors">
                        <Edit2 className="h-4 w-4 text-slate-600" />
                      </button>
                      <button className="p-2 hover:bg-red-50 rounded-lg transition-colors">
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-lg font-semibold text-slate-900 mb-2">
                    {group.name}
                  </h3>
                  <p className="text-sm text-slate-600 mb-4">
                    {group.description}
                  </p>

                  <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-2">
                      <div className="flex -space-x-2">
                        {[...Array(Math.min(group.memberCount, 3))].map((_, i) => (
                          <div
                            key={i}
                            className="h-8 w-8 rounded-full bg-gradient-to-br from-slate-400 to-slate-500 border-2 border-white flex items-center justify-center"
                          >
                            <span className="text-xs text-white font-medium">
                              {String.fromCharCode(65 + i)}
                            </span>
                          </div>
                        ))}
                      </div>
                      <span className="text-sm text-slate-600">
                        {group.memberCount} {group.memberCount === 1 ? 'member' : 'members'}
                      </span>
                    </div>
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      View →
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {filteredGroups.length === 0 && (
              <div className="text-center py-12">
                <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No groups found matching your search.</p>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
