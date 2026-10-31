import React from 'react';
import { FileText, CheckCircle, AlertTriangle, Trash2, Calendar, User, DollarSign } from 'lucide-react';
import ErrorReviewer from './ErrorReviewer';
import DataGridTable from './DataGridTable';

export default function DocumentCard({ doc, onDelete }) {
  const data = doc.extracted_data || {};
  const lineItems = data.line_items || data.items || [];
  
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow relative">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
            <FileText size={24} />
          </div>
          <div>
            <h3 className="font-bold text-slate-800 text-lg">{doc.filename}</h3>
            <p className="text-xs text-slate-500">Document ID: #{doc.id} • Uploaded on {new Date(doc.created_at).toLocaleDateString()}</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center space-x-1 ${
            doc.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' :
            doc.status === 'FLAGGED' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800 animate-pulse'
          }`}>
            {doc.status === 'COMPLETED' && <CheckCircle size={14} className="mr-1" />}
            {doc.status === 'FLAGGED' && <AlertTriangle size={14} className="mr-1" />}
            <span>{doc.status}</span>
          </span>
          <button 
            onClick={() => onDelete(doc.id)} 
            className="text-slate-400 hover:text-rose-600 p-2 rounded-lg hover:bg-rose-50 transition-colors"
            title="Delete Document"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      {/* Human-Readable Extracted Data Grid */}
      {doc.status !== 'PROCESSING' && data.invoice_number ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-100">
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase">Invoice Number</span>
              <p className="text-sm font-bold text-slate-800">{data.invoice_number}</p>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase flex items-center"><Calendar size={12} className="mr-1"/> Date</span>
              <p className="text-sm font-medium text-slate-700">{data.invoice_date || 'N/A'}</p>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase flex items-center"><User size={12} className="mr-1"/> Supplier</span>
              <p className="text-sm font-medium text-slate-700">{data.supplier_name || 'N/A'}</p>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase flex items-center"><DollarSign size={12} className="mr-1"/> Total Amount</span>
              <p className="text-sm font-bold text-emerald-600">{data.currency || '$'} {data.total ? data.total.toLocaleString() : '0.00'}</p>
            </div>
          </div>

          {/* Line Items Data Grid Table */}
          <DataGridTable lineItems={lineItems} />
        </div>
      ) : doc.status === 'PROCESSING' ? (
        <div className="bg-blue-50 text-blue-700 p-4 rounded-lg text-sm font-medium flex items-center justify-center space-x-2 my-2">
          <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <span>Gemini AI is currently extracting and analyzing document contents...</span>
        </div>
      ) : null}

      {/* Validation Errors via ErrorReviewer Component */}
      <ErrorReviewer errors={doc.validation_errors} />
    </div>
  );
}