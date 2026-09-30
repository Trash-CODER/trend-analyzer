import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';

function App() {
  const [healthStatus, setHealthStatus] = useState<string | null>(null);
  const [connectionState, setConnectionState] = useState<'loading' | 'connected' | 'error'>('loading');
  const [errorMsg, setErrorMsg] = useState<string>('');

  const checkHealth = async () => {
    setConnectionState('loading');
    setErrorMsg('');
    try {
      const response = await axios.get('http://localhost:8000/api/health');
      setHealthStatus(response.data.status);
      setConnectionState('connected');
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to connect to backend');
      setConnectionState('error');
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl space-y-6">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">Trend Analyzer</h1>
            <p className="text-sm text-slate-400">System Connection Status</p>
          </div>
        </div>

        <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800/80 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Backend Endpoint:</span>
            <code className="text-xs bg-slate-800 px-2 py-1 rounded text-indigo-300">
              http://localhost:8000/api/health
            </code>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Connection State:</span>
            <div className="flex items-center space-x-1.5">
              {connectionState === 'loading' && (
                <span className="flex items-center text-amber-400 text-sm font-medium">
                  <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> Connecting...
                </span>
              )}
              {connectionState === 'connected' && (
                <span className="flex items-center text-emerald-400 text-sm font-medium">
                  <CheckCircle2 className="w-4 h-4 mr-1" /> Connected
                </span>
              )}
              {connectionState === 'error' && (
                <span className="flex items-center text-rose-400 text-sm font-medium">
                  <AlertCircle className="w-4 h-4 mr-1" /> Error
                </span>
              )}
            </div>
          </div>

          <div className="flex justify-between items-center pt-2 border-t border-slate-800/60">
            <span className="text-sm text-slate-400">Response Status:</span>
            <span className="font-mono text-sm font-semibold text-slate-200">
              {healthStatus ? `"${healthStatus}"` : '—'}
            </span>
          </div>

          {errorMsg && (
            <div className="mt-2 p-3 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-300 text-xs">
              {errorMsg}
            </div>
          )}
        </div>

        <button
          onClick={checkHealth}
          className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-xl transition-colors duration-200 flex items-center justify-center space-x-2 shadow-lg shadow-indigo-600/20 cursor-pointer"
        >
          <RefreshCw className={`w-4 h-4 ${connectionState === 'loading' ? 'animate-spin' : ''}`} />
          <span>Test Connection</span>
        </button>
      </div>
    </div>
  );
}

export default App;
