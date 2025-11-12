'use client';

import { useState, useEffect } from 'react';
import { Users, Shield, FileText, Activity, TrendingUp, AlertTriangle, CheckCircle, Clock, BarChart3, PieChart, RefreshCw } from 'lucide-react';

interface DashboardStats {
  totalPolicies: number;
  activePolicies: number;
  totalUsers: number;
  activeUsers: number;
  totalGroups: number;
  authorizationRequests: number;
  successRate: number;
  avgResponseTime: number;
}

interface RecentActivity {
  id: string;
  type: 'authorization' | 'policy_change' | 'user_action';
  user: string;
  action: string;
  resource: string;
  result: 'allowed' | 'denied';
  timestamp: string;
}

interface TopPolicy {
  id: string;
  name: string;
  evaluations: number;
  successRate: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalPolicies: 12,
    activePolicies: 8,
    totalUsers: 45,
    activeUsers: 38,
    totalGroups: 6,
    authorizationRequests: 1247,
    successRate: 94.2,
    avgResponseTime: 23
  });

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([
    {
      id: '1',
      type: 'authorization',
      user: 'john.doe',
      action: 'read',
      resource: 'document-123',
      result: 'allowed',
      timestamp: '2 minutes ago'
    },
    {
      id: '2',
      type: 'authorization',
      user: 'jane.smith',
      action: 'write',
      resource: 'policy-456',
      result: 'denied',
      timestamp: '5 minutes ago'
    },
    {
      id: '3',
      type: 'policy_change',
      user: 'admin',
      action: 'updated',
      resource: 'document-access-policy',
      result: 'allowed',
      timestamp: '15 minutes ago'
    },
    {
      id: '4',
      type: 'authorization',
      user: 'bob.wilson',
      action: 'delete',
      resource: 'user-789',
      result: 'denied',
      timestamp: '1 hour ago'
    }
  ]);

  const [topPolicies, setTopPolicies] = useState<TopPolicy[]>([
    { id: '1', name: 'Document Access Policy', evaluations: 342, successRate: 96.5 },
    { id: '2', name: 'User Management Policy', evaluations: 256, successRate: 89.2 },
    { id: '3', name: 'Admin Access Policy', evaluations: 189, successRate: 99.1 },
    { id: '4', name: 'API Access Policy', evaluations: 145, successRate: 92.8 }
  ]);

  const [isLoading, setIsLoading] = useState(false);

  const refreshData = async () => {
    setIsLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsLoading(false);
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'authorization':
        return <Shield className="w-4 h-4" />;
      case 'policy_change':
        return <FileText className="w-4 h-4" />;
      case 'user_action':
        return <Users className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  const getResultColor = (result: string) => {
    return result === 'allowed' ? 'text-green-600' : 'text-red-600';
  };

  const getResultBg = (result: string) => {
    return result === 'allowed' ? 'bg-green-100' : 'bg-red-100';
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="animate-slide-up">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
            Dashboard
          </h2>
          <p className="text-slate-600 mt-2 text-lg">Real-time overview of your authorization system</p>
        </div>
        
        <button
          onClick={refreshData}
          disabled={isLoading}
          className="group flex items-center space-x-3 px-6 py-3 bg-white/80 backdrop-blur-sm border border-slate-200/60 text-slate-700 rounded-xl hover:bg-white hover:shadow-lg hover:shadow-slate-200/50 disabled:opacity-50 transition-all duration-200 hover:scale-[1.02]"
        >
          <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : 'group-hover:rotate-180'} transition-transform duration-500`} />
          <span className="font-medium">Refresh</span>
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8">
        <div className="group relative bg-gradient-to-br from-white to-blue-50/30 p-6 rounded-2xl border border-blue-100/50 hover:shadow-xl hover:shadow-blue-500/10 transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/25">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200">
              +12%
            </span>
          </div>
          <div className="relative">
            <p className="text-3xl font-bold text-slate-900">{stats.totalPolicies}</p>
            <p className="text-sm text-slate-600 font-medium mt-1">Total Policies</p>
          </div>
          <div className="relative mt-4 pt-4 border-t border-blue-100/50">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-600">Active</span>
              <span className="font-semibold text-emerald-600">{stats.activePolicies}</span>
            </div>
          </div>
        </div>

        <div className="group relative bg-gradient-to-br from-white to-emerald-50/30 p-6 rounded-2xl border border-emerald-100/50 hover:shadow-xl hover:shadow-emerald-500/10 transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl shadow-lg shadow-emerald-500/25">
              <Users className="w-6 h-6 text-white" />
            </div>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200">
              +8%
            </span>
          </div>
          <div className="relative">
            <p className="text-3xl font-bold text-slate-900">{stats.totalUsers}</p>
            <p className="text-sm text-slate-600 font-medium mt-1">Total Users</p>
          </div>
          <div className="relative mt-4 pt-4 border-t border-emerald-100/50">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-600">Active</span>
              <span className="font-semibold text-emerald-600">{stats.activeUsers}</span>
            </div>
          </div>
        </div>

        <div className="group relative bg-gradient-to-br from-white to-purple-50/30 p-6 rounded-2xl border border-purple-100/50 hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg shadow-purple-500/25">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200">
              +24%
            </span>
          </div>
          <div className="relative">
            <p className="text-3xl font-bold text-slate-900">{stats.authorizationRequests.toLocaleString()}</p>
            <p className="text-sm text-slate-600 font-medium mt-1">Auth Requests</p>
          </div>
          <div className="relative mt-4 pt-4 border-t border-purple-100/50">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-600">Success Rate</span>
              <span className="font-semibold text-emerald-600">{stats.successRate}%</span>
            </div>
          </div>
        </div>

        <div className="group relative bg-gradient-to-br from-white to-orange-50/30 p-6 rounded-2xl border border-orange-100/50 hover:shadow-xl hover:shadow-orange-500/10 transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg shadow-orange-500/25">
              <Clock className="w-6 h-6 text-white" />
            </div>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700 border border-red-200">
              -5%
            </span>
          </div>
          <div className="relative">
            <p className="text-3xl font-bold text-slate-900">{stats.avgResponseTime}ms</p>
            <p className="text-sm text-slate-600 font-medium mt-1">Avg Response Time</p>
          </div>
          <div className="relative mt-4 pt-4 border-t border-orange-100/50">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-600">Status</span>
              <span className="font-semibold text-emerald-600">Healthy</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/60 shadow-lg shadow-slate-900/5 hover:shadow-xl hover:shadow-slate-900/10 transition-all duration-300">
          <div className="p-6 border-b border-slate-200/60">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-slate-900">Recent Activity</h3>
                <p className="text-sm text-slate-600 mt-1">Latest authorization events and system changes</p>
              </div>
              <button className="group text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors flex items-center space-x-1">
                <span>View All</span>
                <TrendingUp className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          </div>
          
          <div className="divide-y divide-slate-200/60">
            {recentActivity.map((activity, index) => (
              <div key={activity.id} className={`p-4 hover:bg-slate-50/50 transition-all duration-200 ${index === 0 ? 'animate-slide-up' : ''}`} style={{ animationDelay: `${index * 100}ms` }}>
                <div className="flex items-start space-x-4">
                  <div className={`p-2.5 rounded-xl ${activity.result === 'allowed' ? 'bg-emerald-100' : 'bg-red-100'}`}>
                    <div className={activity.result === 'allowed' ? 'text-emerald-600' : 'text-red-600'}>
                      {getActivityIcon(activity.type)}
                    </div>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-semibold text-slate-900">
                        <span className="font-medium">{activity.user}</span>
                        <span className="text-slate-600 mx-1">→</span>
                        <span className="text-slate-700">{activity.action}</span>
                        <span className="text-slate-600 mx-1">on</span>
                        <span className="font-medium text-slate-900">{activity.resource}</span>
                      </p>
                      <span className={`inline-flex px-3 py-1 text-xs font-bold rounded-full border ${activity.result === 'allowed' ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 'bg-red-100 text-red-700 border-red-200'}`}>
                        {activity.result}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-2 flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{activity.timestamp}</span>
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Policies */}
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/60 shadow-lg shadow-slate-900/5 hover:shadow-xl hover:shadow-slate-900/10 transition-all duration-300">
          <div className="p-6 border-b border-slate-200/60">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-slate-900">Top Policies</h3>
                <p className="text-sm text-slate-600 mt-1">Most evaluated policies</p>
              </div>
              <div className="p-2 bg-blue-100 rounded-lg">
                <PieChart className="w-5 h-5 text-blue-600" />
              </div>
            </div>
          </div>
          
          <div className="p-6 space-y-4">
            {topPolicies.map((policy, index) => (
              <div key={policy.id} className="group flex items-center justify-between p-3 rounded-xl hover:bg-slate-50/50 transition-all duration-200">
                <div className="flex items-center space-x-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm ${
                    index === 0 ? 'bg-gradient-to-br from-yellow-400 to-orange-500 text-white' :
                    index === 1 ? 'bg-gradient-to-br from-slate-400 to-slate-500 text-white' :
                    index === 2 ? 'bg-gradient-to-br from-orange-400 to-orange-600 text-white' :
                    'bg-gradient-to-br from-slate-300 to-slate-400 text-white'
                  }`}>
                    {index + 1}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">{policy.name}</p>
                    <p className="text-xs text-slate-500">{policy.evaluations} evaluations</p>
                  </div>
                </div>
                
                <div className="text-right">
                  <p className="text-sm font-bold text-slate-900">{policy.successRate}%</p>
                  <div className="w-20 h-2 bg-slate-200 rounded-full mt-1.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        policy.successRate >= 95 ? 'bg-emerald-500' :
                        policy.successRate >= 85 ? 'bg-blue-500' :
                        policy.successRate >= 70 ? 'bg-orange-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${policy.successRate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 bg-gradient-to-br from-white/80 to-blue-50/20 backdrop-blur-sm rounded-2xl border border-slate-200/60 shadow-lg shadow-slate-900/5 p-8">
        <div className="mb-6">
          <h3 className="text-xl font-bold text-slate-900">Quick Actions</h3>
          <p className="text-sm text-slate-600 mt-1">Common tasks and system management</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
          <button className="group flex items-center space-x-4 p-5 bg-white/60 border border-slate-200/60 rounded-xl hover:bg-white hover:shadow-lg hover:shadow-blue-500/10 hover:scale-[1.02] hover:-translate-y-1 transition-all duration-200">
            <div className="p-2.5 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg group-hover:scale-110 transition-transform">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <div className="text-left">
              <span className="text-sm font-semibold text-slate-900">Create Policy</span>
              <p className="text-xs text-slate-500 mt-0.5">Add new authorization rule</p>
            </div>
          </button>
          
          <button className="group flex items-center space-x-4 p-5 bg-white/60 border border-slate-200/60 rounded-xl hover:bg-white hover:shadow-lg hover:shadow-emerald-500/10 hover:scale-[1.02] hover:-translate-y-1 transition-all duration-200">
            <div className="p-2.5 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg group-hover:scale-110 transition-transform">
              <Users className="w-5 h-5 text-white" />
            </div>
            <div className="text-left">
              <span className="text-sm font-semibold text-slate-900">Add User</span>
              <p className="text-xs text-slate-500 mt-0.5">Manage user accounts</p>
            </div>
          </button>
          
          <button className="group flex items-center space-x-4 p-5 bg-white/60 border border-slate-200/60 rounded-xl hover:bg-white hover:shadow-lg hover:shadow-purple-500/10 hover:scale-[1.02] hover:-translate-y-1 transition-all duration-200">
            <div className="p-2.5 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg group-hover:scale-110 transition-transform">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div className="text-left">
              <span className="text-sm font-semibold text-slate-900">Test Authorization</span>
              <p className="text-xs text-slate-500 mt-0.5">Validate access rules</p>
            </div>
          </button>
          
          <button className="group flex items-center space-x-4 p-5 bg-white/60 border border-slate-200/60 rounded-xl hover:bg-white hover:shadow-lg hover:shadow-orange-500/10 hover:scale-[1.02] hover:-translate-y-1 transition-all duration-200">
            <div className="p-2.5 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg group-hover:scale-110 transition-transform">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <div className="text-left">
              <span className="text-sm font-semibold text-slate-900">View Reports</span>
              <p className="text-xs text-slate-500 mt-0.5">Analytics & insights</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}