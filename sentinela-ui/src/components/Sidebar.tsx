'use client'

import { useState, useEffect } from 'react'
import { Shield, Users, FileText, Activity, Settings, LogOut, Menu, X, Boxes, Database, Key } from 'lucide-react'
import { cn } from '../lib/utils'
import apiClient from '../lib/api'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: Shield },
  { name: 'Applications', href: '/applications', icon: Boxes },
  { name: 'Resources', href: '/resources', icon: Database },
  { name: 'Actions', href: '/actions', icon: Key },
  { name: 'Policies', href: '/policies', icon: FileText },
  { name: 'Users', href: '/users', icon: Users },
  { name: 'Groups', href: '/groups', icon: Users },
  { name: 'Audit', href: '/audit', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const [activeItem, setActiveItem] = useState('Dashboard')

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-gradient-to-b from-slate-900 to-slate-800 border-r border-slate-700/50 transform transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}>
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-6 border-b border-slate-700/50">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/25">
                <Shield className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-white">Sentinela</h1>
                <p className="text-xs text-slate-400">IAM Platform</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-2 rounded-lg hover:bg-slate-700/50 transition-colors"
            >
              <X className="h-4 w-4 text-slate-400" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-6">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <a
                  key={item.name}
                  href={item.href}
                  onClick={() => setActiveItem(item.name)}
                  className={cn(
                    "group flex items-center space-x-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200",
                    activeItem === item.name
                      ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/25"
                      : "text-slate-400 hover:bg-slate-700/50 hover:text-white hover:translate-x-1"
                  )}
                >
                  <Icon className={cn(
                    "h-5 w-5 transition-transform duration-200",
                    activeItem === item.name ? "scale-110" : "group-hover:scale-110"
                  )} />
                  <span>{item.name}</span>
                  {activeItem === item.name && (
                    <div className="ml-auto w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  )}
                </a>
              )
            })}
          </nav>

          {/* User section */}
          <div className="border-t border-slate-700/50 p-4">
            <div className="flex items-center space-x-3 p-3 rounded-xl bg-slate-800/50 backdrop-blur-sm">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/25">
                <span className="text-sm font-bold text-white">A</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-white truncate">Alice Admin</p>
                <p className="text-xs text-slate-400 truncate">alice@company.com</p>
              </div>
              <button
                onClick={() => {
                  localStorage.removeItem('sentinela_token');
                  apiClient.setToken('');
                  window.location.href = '/login';
                }}
                className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors group"
                title="Logout"
              >
                <LogOut className="h-4 w-4 text-slate-400 group-hover:text-white transition-colors" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}