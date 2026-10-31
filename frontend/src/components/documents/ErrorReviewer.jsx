import React from 'react';
import { AlertTriangle } from 'lucide-react';

export default function ErrorReviewer({ errors }) {
  if (!errors || errors.length === 0) return null;

  return (
    <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mt-3">
      <div className="flex items-center space-x-2 text-amber-800 font-bold text-sm mb-2">
        <AlertTriangle size={16} />
        <span>Validation Warnings & Discrepancies</span>
      </div>
      <div className="space-y-2">
        {errors.map((err, idx) => (
          <div key={idx} className="bg-white p-2.5 rounded border border-amber-100 text-xs text-amber-900 flex justify-between items-center">
            <div>
              <span className="font-bold uppercase tracking-wider text-amber-700 mr-2">[{err.field}]</span>
              <span>{err.error}</span>
            </div>
            <span className="bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-semibold text-[10px]">Action Needed</span>
          </div>
        ))}
      </div>
    </div>
  );
}