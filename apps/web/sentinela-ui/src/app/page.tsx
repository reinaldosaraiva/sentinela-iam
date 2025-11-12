'use client';

import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Dashboard from '../components/Dashboard';
import ProtectedRoute from '../components/ProtectedRoute';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <ProtectedRoute>
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
      <div className="flex">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 ease-in-out overflow-hidden`}>
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(!sidebarOpen)} />
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <Header 
            title="Sentinela IAM" 
            subtitle="Identity and Access Management System"
          />
          
          <main className="animate-fade-in">
            <Dashboard />
          </main>
        </div>
      </div>
    </div>
    </ProtectedRoute>
  );
}