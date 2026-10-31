import React from 'react';
import { Bell, User } from 'lucide-react';

export default function Header() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center space-x-2">
        <span className="text-sm font-semibold text-slate-700 bg-slate-100 px-3 py-1 rounded-full border border-slate-200">
          Environment: Local Native (FastAPI + PostgreSQL)
        </span>
      </div>
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-3 border-l pl-4 border-slate-200">
          <div className="w-9 h-9 bg-indigo-100 rounded-full flex items-center text-indigo-700 font-bold justify-center">
            AS
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-slate-800">Asaduzzaman Shihab</p>
            <p className="text-xs text-slate-500">System Admin</p>
          </div>
        </div>
      </div>
    </header>
  );
}