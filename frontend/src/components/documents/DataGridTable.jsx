import React from 'react';

export default function DataGridTable({ lineItems }) {
  if (!lineItems || lineItems.length === 0) return null;

  return (
    <div className="mt-4 overflow-x-auto border border-slate-200 rounded-lg">
      <table className="w-full text-left border-collapse text-xs">
        <thead>
          <tr className="bg-slate-100 text-slate-600 border-b border-slate-200">
            <th className="py-2.5 px-3 font-semibold">Description / Item</th>
            <th className="py-2.5 px-3 font-semibold text-center">Qty</th>
            <th className="py-2.5 px-3 font-semibold text-right">Unit Price</th>
            <th className="py-2.5 px-3 font-semibold text-right">Total</th>
          </tr>
        </thead>
        <tbody>
          {lineItems.map((item, idx) => (
            <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50">
              <td className="py-2 px-3 text-slate-800 font-medium">{item.description || item.item_name || 'Item'}</td>
              <td className="py-2 px-3 text-slate-600 text-center">{item.quantity || 1}</td>
              <td className="py-2 px-3 text-slate-600 text-right">{item.unit_price ? item.unit_price.toLocaleString() : '0.00'}</td>
              <td className="py-2 px-3 text-slate-800 font-semibold text-right">{item.total_price || item.total ? (item.total_price || item.total).toLocaleString() : '0.00'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}