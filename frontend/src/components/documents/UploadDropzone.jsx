import React, { useState } from 'react';
import {
  UploadCloud,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react';

// FIXED: Correct relative path to src/services/api.js
import { uploadDocument } from '../../services/api';

export default function UploadDropzone({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
      setMessage(null);
    }
  };

  const handleUpload = async () => {
    if (!file || loading) return;

    setLoading(true);
    setMessage(null);

    try {
      const res = await uploadDocument(file);

      setMessage({
        type: 'success',
        text: `Upload successful! Document ID: ${
          res.document_id ?? res.id ?? 'received'
        }.`
      });

      setFile(null);

      // Refresh the dashboard after uploading.
      if (onUploadSuccess) {
        await onUploadSuccess();
      }
    } catch (err) {
      console.error(
        'Document upload failed:',
        err.response?.data || err.message
      );

      setMessage({
        type: 'error',
        text:
          err.response?.data?.detail ||
          'Upload failed. Check that the backend is running and the API endpoint is correct.'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-bold text-slate-800 mb-4">
        Upload Document for AI Intelligence
      </h2>

      <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors bg-slate-50">
        <UploadCloud className="mx-auto h-12 w-12 text-indigo-500 mb-3" />

        <input
          type="file"
          accept=".pdf,.xlsx,.xls,.csv,.png,.jpg,.jpeg"
          onChange={handleFileChange}
          disabled={loading}
          className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer mb-2"
        />

        <p className="text-xs text-slate-500">
          Supports PDF, Excel (.xlsx, .xls), CSV and images if enabled by the backend.
        </p>

        {file && (
          <p className="mt-3 text-sm font-semibold text-slate-700">
            Selected: {file.name}
          </p>
        )}
      </div>

      {file && (
        <button
          onClick={handleUpload}
          disabled={loading}
          className="mt-4 w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-60 transition-colors flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span>Processing...</span>
            </>
          ) : (
            <span>Process Document</span>
          )}
        </button>
      )}

      {message && (
        <div
          role="status"
          className={`mt-4 p-3 rounded-lg text-sm flex items-center space-x-2 ${
            message.type === 'success'
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              : 'bg-rose-50 text-rose-700 border border-rose-200'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle size={18} />
          ) : (
            <AlertCircle size={18} />
          )}

          <span>{message.text}</span>
        </div>
      )}
    </div>
  );
}