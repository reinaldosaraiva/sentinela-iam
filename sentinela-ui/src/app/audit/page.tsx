'use client';

import { useState, useEffect } from 'react';
import { Activity, Search, Filter, Download, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';

interface AuditLog {
  id: string;
  timestamp: string;
  user: string;
  action: string;
  resource: string;
  result: 'allow' | 'deny';
  details: string;
}

export default function AuditPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterResult, setFilterResult] = useState<'all' | 'allow' | 'deny'>('all');

  const [auditLogs] = useState<AuditLog[]>([
    {
      id: '1',
      timestamp: '2025-01-15 14:32:15',
      user: 'alice@company.com',
      action: 'read',
      resource: 'Document::public',
      result: 'allow',
      details: 'User accessed public document successfully'
    },
    {
      id: '2',
      timestamp: '2025-01-15 14:30:42',
      user: 'bob@company.com',
      action: 'delete',
      resource: 'Document::confidential',
      result: 'deny',
      details: 'User does not have permission to delete confidential documents'
    },
    {
      id: '3',
      timestamp: '2025-01-15 14:28:10',
      user: 'admin@company.com',
      action: 'update',
      resource: 'Policy::employee-access',
      result: 'allow',
      details: 'Policy updated successfully'
    },
    {
      id: '4',
      timestamp: '2025-01-15 14:25:33',
      user: 'alice@company.com',
      action: 'read',
      resource: 'Document::secret',
      result: 'deny',
      details: 'Access denied - insufficient privileges'
    },
    {
      id: '5',
      timestamp: '2025-01-15 14:22:18',
      user: 'manager@company.com',
      action: 'create',
      resource: 'User::new-employee',
      result: 'allow',
      details: 'New user created successfully'
    }
  ]);

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
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  const filteredLogs = auditLogs.filter(log => {
    const matchesSearch =
      log.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.resource.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesFilter =
      filterResult === 'all' || log.result === filterResult;

    return matchesSearch && matchesFilter;
  });

  const getResultIcon = (result: 'allow' | 'deny') => {
    if (result === 'allow') {
      return <CheckCircle className="h-5 w-5 text-green-600" />;
    }
    return <XCircle className="h-5 w-5 text-red-600" />;
  };

  const getResultBadge = (result: 'allow' | 'deny') => {
    if (result === 'allow') {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Allow
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
        Deny
      </span>
    );
  };

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
            title="Audit Logs"
            subtitle="Track all authorization decisions and system events"
          />

          <main className="p-8 animate-fade-in">
            {/* Header Actions */}
            <div className="mb-8 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Authorization Audit Trail</h2>
                <p className="text-slate-600 mt-1">Monitor all access decisions and policy evaluations</p>
              </div>
              <button className="inline-flex items-center px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-xl hover:bg-slate-50 transition-all shadow-sm">
                <Download className="h-4 w-4 mr-2" />
                Export Logs
              </button>
            </div>

            {/* Filters */}
            <div className="mb-6 flex flex-col sm:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search by user, action, or resource..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setFilterResult('all')}
                  className={`px-4 py-2 rounded-xl transition-all ${
                    filterResult === 'all'
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setFilterResult('allow')}
                  className={`px-4 py-2 rounded-xl transition-all ${
                    filterResult === 'allow'
                      ? 'bg-green-600 text-white shadow-lg shadow-green-500/25'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  Allowed
                </button>
                <button
                  onClick={() => setFilterResult('deny')}
                  className={`px-4 py-2 rounded-xl transition-all ${
                    filterResult === 'deny'
                      ? 'bg-red-600 text-white shadow-lg shadow-red-500/25'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  Denied
                </button>
              </div>
            </div>

            {/* Audit Logs Table */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        Timestamp
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        User
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        Action
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        Resource
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        Result
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">
                        Details
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {filteredLogs.map((log) => (
                      <tr key={log.id} className="hover:bg-slate-50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                          {log.timestamp}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                          {log.user}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {log.action}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                          {log.resource}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center gap-2">
                            {getResultIcon(log.result)}
                            {getResultBadge(log.result)}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-600">
                          {log.details}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {filteredLogs.length === 0 && (
                <div className="text-center py-12">
                  <Activity className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                  <p className="text-slate-600">No audit logs found matching your criteria.</p>
                </div>
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
