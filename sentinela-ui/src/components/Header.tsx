'use client';

import { useState } from 'react';
import { Bell, Search, User, Settings, LogOut } from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  const [showProfile, setShowProfile] = useState(false);

  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 px-8 py-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{title}</h1>
          {subtitle && (
            <p className="text-slate-600 mt-2 text-lg">{subtitle}</p>
          )}
        </div>

        <div className="flex items-center space-x-6">
          {/* Search */}
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5 group-focus-within:text-blue-500 transition-colors" />
            <input
              type="text"
              placeholder="Search policies, users, groups..."
              className="pl-12 pr-6 py-3 bg-slate-50/50 border border-slate-200/60 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-96 hover:bg-white hover:shadow-md hover:shadow-slate-200/50 transition-all duration-200 placeholder-slate-500"
            />
          </div>

          {/* Notifications */}
          <button className="relative group p-3 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-all duration-200 hover:scale-105">
            <Bell className="w-5 h-5" />
            <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse"></span>
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
          </button>

          {/* Profile */}
          <div className="relative">
            <button
              onClick={() => setShowProfile(!showProfile)}
              className="group flex items-center space-x-3 p-3 hover:bg-slate-100 rounded-xl transition-all duration-200 hover:scale-105"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-xl group-hover:shadow-blue-500/30 transition-all">
                <User className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <span className="text-sm font-semibold text-slate-900 block">Admin User</span>
                <span className="text-xs text-slate-500">Administrator</span>
              </div>
            </button>

            {showProfile && (
              <div className="absolute right-0 mt-3 w-56 bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl shadow-slate-900/10 border border-slate-200/60 py-2 z-50 animate-slide-up">
                <button className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center space-x-3 transition-colors">
                  <div className="p-1.5 bg-slate-100 rounded-lg">
                    <User className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="font-medium">Profile</span>
                    <p className="text-xs text-slate-500">Account settings</p>
                  </div>
                </button>
                <button className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center space-x-3 transition-colors">
                  <div className="p-1.5 bg-slate-100 rounded-lg">
                    <Settings className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="font-medium">Settings</span>
                    <p className="text-xs text-slate-500">Preferences</p>
                  </div>
                </button>
                <hr className="my-2 border-slate-200/60" />
                <button className="w-full px-4 py-3 text-left text-sm text-red-600 hover:bg-red-50 flex items-center space-x-3 transition-colors">
                  <div className="p-1.5 bg-red-100 rounded-lg">
                    <LogOut className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="font-medium">Logout</span>
                    <p className="text-xs text-red-500">Sign out of account</p>
                  </div>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}