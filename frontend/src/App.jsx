import React, { useState, useEffect } from 'react';
import MainLayout from './layouts/MainLayout';
import UploadDropzone from './components/documents/UploadDropzone';
import DocumentCard from './components/documents/DocumentCard';
import SearchFilterBar from './components/documents/SearchFilterBar';
import { fetchDocuments, searchDocuments, deleteDocument } from './services/api';
import { FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [documents, setDocuments] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [searchResults, setSearchResults] = useState([]);

  const loadDocuments = async () => {
    try {
      const data = await fetchDocuments();
      setDocuments(data);
    } catch (e) {
      console.error("Failed to load documents", e);
    }
  };

  useEffect(() => {
    loadDocuments();
    const interval = setInterval(() => {
      setDocuments(prevDocs => {
        if (prevDocs.some(d => d.status === 'PROCESSING')) {
          loadDocuments();
        }
        return prevDocs;
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const res = await searchDocuments(searchQuery);
      const filtered = selectedStatus === 'ALL' 
        ? res 
        : res.filter(d => d.status === selectedStatus);
      setSearchResults(filtered);
    } catch (err) {
      console.error("Search failed", err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm(`Are you sure you want to delete document ID ${id}?`)) {
      try {
        await deleteDocument(id);
        loadDocuments();
        setSearchResults(searchResults.filter(doc => doc.id !== id));
      } catch (err) {
        console.error("Delete failed", err);
      }
    }
  };

  return (
    <MainLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          <h1 className="text-2xl font-bold text-slate-800">Document Intelligence Dashboard</h1>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">Total Documents</p>
                <p className="text-3xl font-bold text-slate-800">{documents.length}</p>
              </div>
              <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg"><FileText size={24} /></div>
            </div>
            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">Successfully Processed</p>
                <p className="text-3xl font-bold text-emerald-600">{documents.filter(d => d.status === 'COMPLETED').length}</p>
              </div>
              <div className="p-3 bg-emerald-50 text-emerald-600 rounded-lg"><CheckCircle size={24} /></div>
            </div>
            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">Flagged / Review Needed</p>
                <p className="text-3xl font-bold text-amber-600">{documents.filter(d => d.status === 'FLAGGED').length}</p>
              </div>
              <div className="p-3 bg-amber-50 text-amber-600 rounded-lg"><AlertTriangle size={24} /></div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <UploadDropzone onUploadSuccess={loadDocuments} />
            </div>
            <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-slate-800">Recent Ingested Documents</h2>
                <button onClick={loadDocuments} className="text-xs text-indigo-600 font-semibold hover:underline">Refresh List</button>
              </div>
              <div className="space-y-4">
                {documents.map((doc) => (
                  <DocumentCard key={doc.id} doc={doc} onDelete={handleDelete} />
                ))}
                {documents.length === 0 && (
                  <div className="py-12 text-center text-slate-400">No documents uploaded yet.</div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'documents' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div>
              <h1 className="text-2xl font-bold text-slate-800">All Documents & Extractions</h1>
              <p className="text-slate-600 text-sm">Review full business details and line items.</p>
            </div>
            <button onClick={loadDocuments} className="bg-indigo-50 text-indigo-600 font-semibold px-4 py-2 rounded-lg text-sm hover:bg-indigo-100 transition-colors">Refresh List</button>
          </div>
          <div className="space-y-4">
            {documents.map(doc => (
              <DocumentCard key={doc.id} doc={doc} onDelete={handleDelete} />
            ))}
            {documents.length === 0 && (
              <div className="bg-white p-12 rounded-xl text-center text-slate-400 border border-slate-200">No documents found.</div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'search' && (
        <div className="space-y-6">
          <SearchFilterBar 
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            selectedStatus={selectedStatus}
            setSelectedStatus={setSelectedStatus}
            onSearch={handleSearch}
          />

          {searchResults.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-slate-800">Search Results ({searchResults.length})</h2>
              {searchResults.map(doc => (
                <DocumentCard key={doc.id} doc={doc} onDelete={handleDelete} />
              ))}
            </div>
          )}
        </div>
      )}
    </MainLayout>
  );
}