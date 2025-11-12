'use client';

import { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import UserManagement from '../../components/UserManagement';

export default function UsersPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

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
            title="User Management" 
            subtitle="Manage users, groups, and access permissions"
          />
          
          <main>
            <UserManagement />
          </main>
        </div>
      </div>
    </div>
  );
}