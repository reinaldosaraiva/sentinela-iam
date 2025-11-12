'use client';

import { useState, useEffect } from 'react';
import { Settings, Shield, Bell, Key, Database, Globe, Save } from 'lucide-react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';

export default function SettingsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState('general');

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

  const tabs = [
    { id: 'general', name: 'General', icon: Settings },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'api', name: 'API Keys', icon: Key },
    { id: 'database', name: 'Database', icon: Database },
  ];

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
            title="Settings"
            subtitle="Configure your IAM system preferences"
          />

          <main className="p-8 animate-fade-in">
            <div className="max-w-6xl mx-auto">
              {/* Tabs */}
              <div className="mb-8 border-b border-slate-200">
                <nav className="-mb-px flex space-x-8">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`
                          group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-all
                          ${activeTab === tab.id
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                          }
                        `}
                      >
                        <Icon className={`h-5 w-5 mr-2 ${activeTab === tab.id ? 'text-blue-500' : 'text-slate-400 group-hover:text-slate-500'}`} />
                        {tab.name}
                      </button>
                    );
                  })}
                </nav>
              </div>

              {/* General Settings */}
              {activeTab === 'general' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-xl border border-slate-200 p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">System Information</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                          System Name
                        </label>
                        <input
                          type="text"
                          defaultValue="Sentinela IAM"
                          className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                          Organization
                        </label>
                        <input
                          type="text"
                          defaultValue="My Company"
                          className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                          Time Zone
                        </label>
                        <select className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                          <option>UTC</option>
                          <option>America/New_York</option>
                          <option>America/Sao_Paulo</option>
                          <option>Europe/London</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Security Settings */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-xl border border-slate-200 p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Authentication</h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-slate-900">Two-Factor Authentication</p>
                          <p className="text-sm text-slate-600">Add an extra layer of security</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" className="sr-only peer" />
                          <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                      <div className="flex items-center justify-between pt-4 border-t">
                        <div>
                          <p className="font-medium text-slate-900">Session Timeout</p>
                          <p className="text-sm text-slate-600">Automatically logout after inactivity</p>
                        </div>
                        <select className="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500">
                          <option>15 minutes</option>
                          <option>30 minutes</option>
                          <option>1 hour</option>
                          <option>2 hours</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white rounded-xl border border-slate-200 p-6">
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Password Policy</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                          Minimum Length
                        </label>
                        <input
                          type="number"
                          defaultValue="8"
                          min="6"
                          max="32"
                          className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-700">Require uppercase letters</span>
                        <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-700">Require numbers</span>
                        <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-700">Require special characters</span>
                        <input type="checkbox" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Settings */}
              {activeTab === 'notifications' && (
                <div className="bg-white rounded-xl border border-slate-200 p-6">
                  <h3 className="text-lg font-semibold text-slate-900 mb-4">Email Notifications</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-slate-900">Policy Changes</p>
                        <p className="text-sm text-slate-600">Receive alerts when policies are modified</p>
                      </div>
                      <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-slate-900">Failed Login Attempts</p>
                        <p className="text-sm text-slate-600">Get notified of suspicious login activity</p>
                      </div>
                      <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-slate-900">User Management</p>
                        <p className="text-sm text-slate-600">Alerts for user additions and removals</p>
                      </div>
                      <input type="checkbox" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                    </div>
                  </div>
                </div>
              )}

              {/* API Keys Settings */}
              {activeTab === 'api' && (
                <div className="bg-white rounded-xl border border-slate-200 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-semibold text-slate-900">API Keys</h3>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                      Generate New Key
                    </button>
                  </div>
                  <div className="space-y-4">
                    <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-slate-900">Production API Key</span>
                        <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full">Active</span>
                      </div>
                      <code className="text-sm text-slate-600 font-mono">sk_prod_abc123...xyz789</code>
                      <p className="text-xs text-slate-500 mt-2">Created: Jan 10, 2025 • Last used: 2 hours ago</p>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-slate-900">Development API Key</span>
                        <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full">Active</span>
                      </div>
                      <code className="text-sm text-slate-600 font-mono">sk_dev_def456...uvw012</code>
                      <p className="text-xs text-slate-500 mt-2">Created: Jan 5, 2025 • Last used: 1 day ago</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Database Settings */}
              {activeTab === 'database' && (
                <div className="bg-white rounded-xl border border-slate-200 p-6">
                  <h3 className="text-lg font-semibold text-slate-900 mb-4">Database Configuration</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Database Type
                      </label>
                      <select className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500">
                        <option>PostgreSQL</option>
                        <option>MySQL</option>
                        <option>MongoDB</option>
                        <option>In-Memory (Development)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Connection String
                      </label>
                      <input
                        type="text"
                        defaultValue="postgresql://localhost:5432/sentinela"
                        className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                      />
                    </div>
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div>
                        <p className="font-medium text-slate-900">Connection Status</p>
                        <p className="text-sm text-slate-600">Database connection is healthy</p>
                      </div>
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                        Connected
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Save Button */}
              <div className="mt-8 flex justify-end">
                <button className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-500/25">
                  <Save className="h-4 w-4 mr-2" />
                  Save Changes
                </button>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
