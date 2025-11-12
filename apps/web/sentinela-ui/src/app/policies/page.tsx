'use client';

import { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import PolicyEditor from '../../components/PolicyEditor';

interface Policy {
  id: string;
  name: string;
  description: string;
  content: string;
  status: 'active' | 'inactive' | 'draft';
  created_at: string;
  updated_at: string;
}

export default function PoliciesPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | undefined>();

  const handleSavePolicy = (policyData: Partial<Policy>) => {
    console.log('Saving policy:', policyData);
    // TODO: Implement API call to save policy
  };

  const handleTestPolicy = async (policyContent: string) => {
    console.log('Testing policy:', policyContent);
    // TODO: Implement API call to test policy
    return {
      results: [
        {
          principal: 'user:john',
          action: 'read',
          resource: 'document:123',
          allowed: true
        },
        {
          principal: 'user:jane',
          action: 'write',
          resource: 'document:456',
          allowed: false
        }
      ]
    };
  };

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