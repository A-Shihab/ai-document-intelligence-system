import React from 'react';
import { Search as SearchIcon, Filter } from 'lucide-react';

export default function SearchFilterBar({ searchQuery, setSearchQuery, selectedStatus, setSelectedStatus, onSearch }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
      <h1 className="text-2xl font-bold text-slate-800">Smart Document Search & Filters</h1>
      <p className="text-slate-600 text-sm">Query across document content, invoice numbers, and supplier names.</p>
      
      <form onSubmit={onSearch} className="flex flex-col md:flex-row gap-3">
        <div className="flex-1 relative flex items-center">
          <SearchIcon size={18} className="absolute left-3 text-slate-400" />
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Type keyword e.g. Northstar, laptops, INV-2026..." 
            className="w-full border border-slate-300 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" 
          />
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-slate-500 text-xs font-semibold px-2">
            <Filter size={14} />
            <span>Status:</span>
          </div>
          <select 
            value={selectedStatus} 
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="COMPLETED">Completed</option>
            <option value="FLAGGED">Flagged</option>
            <option value="PROCESSING">Processing</option>
          </select>

          <button type="submit" className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition-colors text-sm">
            Search
          </button>
        </div>
      </form>
    </div>
  );
}