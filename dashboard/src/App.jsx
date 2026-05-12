import React, { useState, useEffect } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import { MapContainer, TileLayer, Polygon, Tooltip as MapTooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

import TRANSLATIONS from './translations.json';

const API = "http://localhost:5000/api";

const PARAM_LABELS = {
  nitrogen: "Nitrogen (mg/kg)",
  phosphorus: "Phosphorus (mg/kg)",
  potassium: "Potassium (mg/kg)",
  ph: "Soil pH",
  ec: "EC (µS/cm)",
  temperature: "Temperature (°C)",
  humidity: "Soil Moisture (%)"
};

// const SCIENTIFIC_DISCLAIMER = "Decision Support Only: This AI system provides monitoring insights based on real-time sensor patterns and CRI Advisory circulars. For final fertilizer application, professional CRI laboratory leaf/soil analysis is mandatory.";

const DiagnosticCard = ({ label, value, sub, icon, status }) => (
  <div className="bg-white p-5 rounded-[1.5rem] border border-slate-100 shadow-lg shadow-slate-200/40 flex flex-col gap-3 relative overflow-hidden group hover:scale-[1.02] transition-all">
    <div className="flex items-center gap-3">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl shadow-inner ${status === 'success' ? 'bg-emerald-50 text-emerald-600' : status === 'warning' ? 'bg-amber-50 text-amber-600' : 'bg-rose-50 text-rose-600'
        }`}>
        {icon}
      </div>
      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-tight">{label}</p>
    </div>
    <div>
      <p className="text-xl font-black text-slate-800">{value}</p>
      <p className={`text-[9px] font-bold uppercase mt-1 ${status === 'success' ? 'text-emerald-500' : status === 'warning' ? 'text-amber-500' : 'text-rose-500'
        }`}>{sub}</p>
    </div>
  </div>
);

const StatusBadge = ({ text, type }) => (
  <span className={`px-3 py-1 rounded-lg text-[9px] font-black uppercase ${type === 'success' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' :
    type === 'warning' ? 'bg-amber-50 text-amber-600 border border-amber-100' :
      'bg-rose-50 text-rose-600 border border-rose-100'
    }`}>
    {text}
  </span>
);

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [zones, setZones] = useState([]);
  const [samples, setSamples] = useState([]);
  const [selectedZone, setSelectedZone] = useState({});
  const [lang, setLang] = useState('EN');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [viewingZoneSamples, setViewingZoneSamples] = useState('A');

  const t = (key) => TRANSLATIONS[lang][key] || key;

  useEffect(() => {
    fetchStats();
    fetchZones();
    fetchSamples();

    // Reset or Re-fetch active results to prevent language mixing
    if (analysisResult) {
      setAnalysisResult(null); // Clear manual analysis to force re-run if needed, or keep it simple
    }
  }, [lang]);

  const fetchStats = () => {
    fetch(`${API}/stats?lang=${lang}`).then(res => res.json()).then(setStats);
  };

  const fetchSamples = () => {
    fetch(`${API}/samples?lang=${lang}`)
      .then(res => res.json())
      .then(data => {
        setSamples(data);
        // Sync the currently viewed sample with its newly localized version
        if (selectedZone) {
          const updated = data.find(s => s.sample_id === selectedZone.sample_id);
          if (updated) setSelectedZone(updated);
        }
      })
      .catch(e => console.error("Sample fetch error:", e));
  };

  const fetchZones = () => {
    fetch(`${API}/zones`).then(res => res.json()).then(setZones);
  };

  const runAnalysis = (sampleData) => {
    setAnalyzing(true);
    fetch(`${API}/analyze?lang=${lang}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sampleData)
    })
      .then(res => res.json())
      .then(data => {
        setAnalysisResult(data);
        setAnalyzing(false);
        fetchStats();
      });
  };

  const getRadarData = () => {
    if (!stats) return [];
    return [
      { subject: 'Nitrogen', A: 60, fullMark: 100 },
      { subject: 'Phosphorus', A: 45, fullMark: 100 },
      { subject: 'Potassium', A: 80, fullMark: 100 },
      { subject: 'pH', A: 70, fullMark: 100 },
      { subject: 'EC', A: 30, fullMark: 100 },
      { subject: 'Moisture', A: 65, fullMark: 100 },
    ];
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] font-sans text-slate-900">
      {/* Disclaimer Banner */}
      {/* <div className="bg-[#1e5631] text-white py-2 px-4 text-[10px] font-bold text-center tracking-wide">
        {SCIENTIFIC_DISCLAIMER}
      </div> */}


      {/* CocoCastAI Header */}
      <header className="bg-white/80 backdrop-blur-xl border-b border-slate-100 sticky top-0 z-[2000] px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-[#1e5631] rounded-xl flex items-center justify-center shadow-lg shadow-emerald-200">
            <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8a9 9 0 0 1-9 9Z"></path>
              <path d="M11 20c-1.2 0-2 0-2-1"></path>
              <path d="M11 20c0-1.2.1-2.5 1.2-3.7 1.4-1.4 4.3-2 5.8-3.3"></path>
            </svg>
          </div>
          <h1 className="text-2xl font-black tracking-tighter text-[#1e5631]">
            CocoCast<span className="text-emerald-500">AI</span>
          </h1>
        </div>

        <nav className="hidden lg:flex items-center gap-8 ml-12">
          {['Overview', 'Zone Analytics', 'Soil Health'].map(link => {
            const keyMap = { 'Overview': 'overview', 'Zone Analytics': 'zones', 'Soil Health': 'monitoring' };
            const tabMap = { 'Overview': 'dashboard', 'Zone Analytics': 'zones', 'Soil Health': 'monitoring' };
            const currentTab = tabMap[link];
            return (
              <button
                key={link}
                onClick={() => setActiveTab(currentTab)}
                className={`text-sm font-black transition-all ${activeTab === currentTab ? 'text-[#1e5631] underline underline-offset-8 decoration-4' : 'text-slate-400 hover:text-slate-600'
                  }`}
              >
                {t(keyMap[link])}
              </button>
            );
          })}
        </nav>

        <div className="flex items-center gap-4">
          <div className="bg-slate-50 border border-slate-100 rounded-full pl-3 pr-1 py-1 flex items-center gap-4">
            <div className="flex items-center bg-white rounded-full p-0.5 border border-slate-100 gap-1">
              {[{ l: 'සිං', v: 'SI' }, { l: 'தமிழ்', v: 'TA' }, { l: 'EN', v: 'EN' }].map(language => (
                <button
                  key={language.v}
                  onClick={() => setLang(language.v)}
                  className={`px-3 py-1 rounded-full text-[9px] font-black transition-all ${lang === language.v ? 'bg-[#1e5631] text-white' : 'text-slate-400 hover:text-slate-600'}`}
                >
                  {language.l}
                </button>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8">
        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && (
            <motion.div key="dash" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              {/* Top Analytics Cards - Row 1 */}
              <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
                <DiagnosticCard
                  label={t('stability')}
                  value={stats?.total_stability === 'Stable' ? t('stable') : t('unstable')}
                  sub={t('ml_trend')}
                  icon="🛡️"
                  status={stats?.total_stability === 'Stable' ? 'success' : 'danger'}
                />
                <DiagnosticCard
                  label={t('balance')}
                  value={stats?.avg_balance === 'Balanced' ? t('balanced') : t('imbalance')}
                  sub={t('sci_baseline')}
                  icon="⚖️"
                  status={stats?.avg_balance === 'Balanced' ? 'success' : 'warning'}
                />
                <DiagnosticCard
                  label={t('ph')}
                  value={`${stats?.avg_ph || '0.0'}`}
                  sub={t(stats?.ph_trend?.toLowerCase() || 'optimal')}
                  icon="💧"
                  status={stats?.avg_ph < 5.5 ? 'danger' : 'success'}
                />
                <DiagnosticCard
                  label={t('ec')}
                  value={`${stats?.avg_ec || '0.00'} dS/m`}
                  sub={t('normal')}
                  icon="⚡"
                  status={stats?.avg_ec > 0.8 ? 'warning' : 'success'}
                />
                <DiagnosticCard
                  label={t('moisture')}
                  value={`${stats?.avg_moisture || '0.0'}%`}
                  sub={t('normal')}
                  icon="🌊"
                  status={stats?.avg_moisture < 20 ? 'warning' : 'success'}
                />
                <DiagnosticCard
                  label={t('temp')}
                  value={`${stats?.avg_temp || '0.0'} °C`}
                  sub={t('normal')}
                  icon="🌡️"
                  status="success"
                />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                {/* Plantation Map Card */}
                <div className="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/40 relative">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-black text-slate-800">{t('map')}</h3>
                  </div>
                  <div className="h-[400px] rounded-2xl overflow-hidden border border-slate-100 relative">
                    <MapContainer center={[6.0585, 80.2255]} zoom={18} className="h-full w-full">
                      <TileLayer
                        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                        attribution='&copy; ESRI'
                      />
                      {zones.map((zone, idx) => (
                        <Polygon
                          key={idx}
                          positions={zone.polygon}
                          pathOptions={{
                            color: zone.id === 'A' ? '#10b981' : zone.id === 'B' ? '#f59e0b' : zone.id === 'C' ? '#ef4444' : zone.id === 'D' ? '#8b5cf6' : '#3b82f6',
                            fillOpacity: 0.4,
                            weight: 3
                          }}
                        >
                          <MapTooltip sticky>
                            <div className="p-1 font-black text-[10px]">{zone.name}</div>
                          </MapTooltip>
                        </Polygon>
                      ))}
                    </MapContainer>
                  </div>
                </div>

                {/* Zone Comparison Table Card */}
                <div className="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/40">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-black text-slate-800">{t('comparison')}</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left">
                      <thead>
                        <tr className="border-b border-slate-50">
                          <th className="pb-4 text-[10px] font-black text-slate-400 uppercase">Zone</th>
                          <th className="pb-4 text-[10px] font-black text-slate-400 uppercase">{t('stability')}</th>
                          <th className="pb-4 text-[10px] font-black text-slate-400 uppercase">{t('balance')}</th>
                          <th className="pb-4 text-[10px] font-black text-slate-400 uppercase">pH</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-50">
                        {zones.map(zone => {
                          const zStats = stats?.zone_stats?.[zone.id] || {};
                          return (
                            <tr key={zone.id} className="hover:bg-slate-50/50 transition-colors">
                              <td className="py-4 text-xs font-black text-slate-800">{zone.name}</td>
                              <td className="py-4">
                                <StatusBadge text={zStats.unstable > zStats.stable ? t('unstable') : t('stable')} type={zStats.unstable > zStats.stable ? 'danger' : 'success'} />
                              </td>
                              <td className="py-4">
                                <StatusBadge text={zStats.imbalance ? t('imbalance') : t('balanced')} type={zStats.imbalance ? 'warning' : 'success'} />
                              </td>
                              <td className={`py-4 text-xs font-bold ${zStats.avg_ph < 5.5 ? 'text-rose-500' : 'text-emerald-500'}`}>{zStats.avg_ph?.toFixed(1) || '0.0'}</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* CRI Reference Standards Panel */}
              <div className="bg-[#1e5631] text-white p-8 rounded-[2.5rem] shadow-2xl shadow-emerald-900/20 flex flex-col md:flex-row items-center justify-between gap-8 relative overflow-hidden">
                <div className="relative z-10">
                  <h3 className="text-xl font-black mb-1">CRI Reference Baseline</h3>
                  <p className="text-[10px] font-bold text-emerald-300 uppercase tracking-widest mb-4">Official Sri Lankan Soil Standards</p>
                  <div className="flex flex-wrap gap-4">
                    {[
                      { l: 'Nitrogen', v: '30-60' }, { l: 'Phosphorus', v: '15-30' }, { l: 'Potassium', v: '40-80' }, { l: 'pH', v: '5.5-7.0' }
                    ].map(i => (
                      <div key={i.l} className="bg-white/10 px-4 py-2 rounded-2xl border border-white/5">
                        <p className="text-[8px] font-black uppercase text-emerald-200">{i.l}</p>
                        <p className="text-sm font-black">{i.v} <span className="text-[10px] opacity-60">mg/kg</span></p>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="relative z-10 text-right">
                  <p className="text-[10px] font-black uppercase text-emerald-300 mb-2">System Accuracy Calibration</p>
                  <div className="flex items-center gap-4">
                    <div className="text-center">
                      <p className="text-2xl font-black">68%</p>
                      <p className="text-[8px] font-bold opacity-60">Imbalance Model</p>
                    </div>
                    <div className="w-[2px] h-10 bg-white/10"></div>
                    <div className="text-center">
                      <p className="text-2xl font-black">78%</p>
                      <p className="text-[8px] font-bold opacity-60">Stability Model</p>
                    </div>
                  </div>
                </div>
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -mr-32 -mt-32"></div>
              </div>
            </motion.div>
          )}

          {activeTab === 'zones' && (
            <motion.div key="zones" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              {/* Zone Navigation Bar */}
              <div className="bg-white p-4 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/20 overflow-x-auto scrollbar-hide">
                <div className="flex items-center gap-4 min-w-max px-4">
                  {zones.map((zone) => (
                    <button
                      key={zone.id}
                      onClick={() => setViewingZoneSamples(zone.id)}
                      className={`px-8 py-4 rounded-[1.5rem] text-sm font-black transition-all ${viewingZoneSamples === zone.id
                        ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-200 scale-105'
                        : 'bg-slate-50 text-slate-400 hover:bg-slate-100'
                        }`}
                    >
                      {zone.name}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: Soil Samples List */}
                <div className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-xl shadow-slate-200/30">
                  <div className="flex items-center justify-between mb-8">
                    <h3 className="text-xl font-black text-slate-800">{t('samples')}</h3>
                    <button className="w-8 h-8 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center font-bold hover:bg-emerald-100 transition-all">+</button>
                  </div>

                  <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2">
                    {samples.filter(s => (s.zone_id === viewingZoneSamples || s.zone === viewingZoneSamples)).length > 0 ? (
                      samples.filter(s => (s.zone_id === viewingZoneSamples || s.zone === viewingZoneSamples)).map((sample, idx) => (
                        <button
                          key={idx}
                          onClick={() => setSelectedZone(sample)}
                          className={`w-full p-5 rounded-2xl border text-left transition-all ${selectedZone?.sample_id === sample.sample_id
                            ? 'border-emerald-500 bg-emerald-50/30'
                            : 'border-slate-50 hover:bg-slate-50'
                            }`}
                        >
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs font-black text-slate-700">{sample.sample_id}</span>
                            <StatusBadge text={sample.status === 'Stable' ? t('stable') : t('unstable')} type={sample.status === 'Stable' ? 'success' : 'danger'} />
                          </div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{sample.monitoring_insight}</p>
                        </button>
                      ))
                    ) : (
                      <div className="py-20 text-center">
                        <p className="text-sm font-bold text-slate-300 uppercase tracking-widest">No sensor data for this zone.</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Right: Analysis Result Area */}
                <div className="lg:col-span-2 bg-white p-10 rounded-[2.5rem] border border-slate-100 shadow-2xl relative min-h-[600px] flex flex-col items-center justify-center">
                  {selectedZone?.sample_id ? (
                    <div className="w-full h-full animate-in fade-in duration-500">
                      <div className="flex items-center gap-6 mb-10 border-b border-slate-50 pb-8">
                        <div className={`w-16 h-16 rounded-[1.5rem] flex items-center justify-center text-3xl ${selectedZone.status === 'Stable' ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'
                          }`}>
                          {selectedZone.status === 'Stable' ? '🍃' : '⚠️'}
                        </div>
                        <div>
                          <h4 className="text-2xl font-black text-slate-800">{t('result')}</h4>
                          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{t('diagnostic_id')}: {selectedZone.sample_id}</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                        {[
                          { l: 'Nitrogen', v: selectedZone.nitrogen, u: 'mg/kg' },
                          { l: 'Phosphorus', v: selectedZone.phosphorus, u: 'mg/kg' },
                          { l: 'Potassium', v: selectedZone.potassium, u: 'mg/kg' },
                          { l: 'pH Level', v: selectedZone.ph, u: '' }
                        ].map((i, idx) => (
                          <div key={idx} className="bg-slate-50 p-4 rounded-2xl">
                            <p className="text-[10px] font-black text-slate-400 uppercase mb-1">{i.l}</p>
                            <p className="text-xl font-black text-slate-800">{i.v} <span className="text-[10px] opacity-40">{i.u}</span></p>
                          </div>
                        ))}
                      </div>

                      <div className="space-y-6">
                        <div className="p-6 bg-slate-50 rounded-[2rem] border border-slate-100">
                          <p className="text-xs font-black text-slate-400 uppercase mb-2">{t('insight')}</p>
                          <p className="text-base font-black text-slate-700 leading-relaxed">{selectedZone.monitoring_insight}</p>
                        </div>

                        {selectedZone.status === 'Unstable' && (
                          <div className="p-6 bg-emerald-50 rounded-[2rem] border border-emerald-100">
                            <p className="text-xs font-black text-emerald-900 mb-3 uppercase">{t('recovery')}</p>
                            <ul className="space-y-2">
                              {selectedZone.alerts.map((alert, i) => (
                                <li key={i} className="flex items-center gap-3 text-sm font-bold text-emerald-800">
                                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                  {alert}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {(selectedZone.actions || []).length > 0 && (
                          <div className="mt-8 pt-8 border-t border-emerald-100">
                            <h4 className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-4">{t('treatment')}</h4>
                            <ul className="space-y-3">
                              {selectedZone.actions.map((action, i) => (
                                <li key={i} className="flex items-start gap-3 text-sm font-bold text-emerald-900 bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100/50">
                                  <span className="text-emerald-500 mt-0.5">✔</span>
                                  {action}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="text-center opacity-40">
                      <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center text-4xl mx-auto mb-6">📉</div>
                      <h4 className="text-xl font-black text-slate-300 uppercase tracking-tighter">{t('result')}</h4>
                      <p className="text-sm font-bold text-slate-300 uppercase mt-2">{t('select_sample')}</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'monitoring' && (
            <motion.div key="monitor" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                <div className="lg:col-span-1 bg-white p-10 rounded-[3rem] border border-slate-100 shadow-2xl">
                  <h3 className="text-xl font-black text-slate-800 mb-8">Manual Node Entry</h3>
                  <div className="space-y-6">
                    {Object.keys(PARAM_LABELS).map(key => (
                      <div key={key}>
                        <label className="text-[10px] font-black text-slate-400 uppercase mb-2 block">{PARAM_LABELS[key]}</label>
                        <input type="number" step="0.1" className="w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-4 text-sm font-bold focus:ring-4 focus:ring-emerald-500/10 outline-none transition-all" onChange={(e) => setSelectedZone(prev => ({ ...prev, [key]: parseFloat(e.target.value) }))} />
                      </div>
                    ))}
                    <button onClick={() => runAnalysis(selectedZone)} disabled={analyzing} className="w-full bg-[#1e5631] text-white font-black py-5 rounded-[2rem] shadow-2xl shadow-emerald-900/20 active:scale-95 transition-all disabled:opacity-50">RUN SCIENTIFIC ANALYSIS</button>
                  </div>
                </div>

                <div className="lg:col-span-2 space-y-8">
                  {analysisResult ? (
                    <div className="bg-white p-12 rounded-[3.5rem] border border-slate-100 shadow-2xl relative overflow-hidden">
                      <div className={`absolute top-0 right-0 px-10 py-3 font-black text-xs uppercase ${analysisResult.status === 'Stable' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>{analysisResult.status} Detection</div>
                      <div className="mb-10">
                        <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">{t('ml_insight')}</h4>
                        <p className="text-4xl font-black text-slate-800 tracking-tight leading-tight">{analysisResult.monitoring_insight}</p>
                      </div>
                      <div className="space-y-4 mb-10">
                        {analysisResult.alerts.map((alert, i) => (
                          <div key={i} className="flex items-center gap-4 bg-slate-50 p-6 rounded-[2rem] border border-slate-100"><span className="text-emerald-500 text-2xl">◈</span><p className="text-sm font-black text-slate-700">{alert}</p></div>
                        ))}
                      </div>
                      {(analysisResult.actions || []).length > 0 && (
                        <div className="p-8 bg-emerald-50 rounded-[3rem] border border-emerald-100 mt-8">
                          <p className="text-xs font-black text-emerald-900 mb-6 uppercase tracking-widest">{t('treatment')}</p>
                          <div className="grid grid-cols-1 gap-4">
                            {analysisResult.actions.map((action, i) => (
                              <div key={i} className="flex items-center gap-4 bg-white p-5 rounded-2xl border border-emerald-200/50 shadow-sm">
                                <span className="text-emerald-600 text-xl font-bold">✔</span>
                                <p className="text-sm font-black text-emerald-800">{action}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      <p className="mt-10 pt-8 border-t border-slate-100 text-[10px] text-slate-400 font-medium leading-relaxed">{analysisResult.disclaimer}</p>
                    </div>
                  ) : (
                    <div className="h-full bg-white rounded-[3.5rem] border-4 border-dashed border-slate-100 flex flex-col items-center justify-center p-20 text-center">
                      <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center text-4xl mb-6">🔬</div>
                      <h4 className="text-2xl font-black text-slate-300 uppercase">Awaiting Scientific Feed</h4>
                      <p className="text-sm text-slate-300 max-w-xs mt-4 font-bold uppercase tracking-widest">Input sensor data to activate ML model inference</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="bg-slate-900 text-slate-500 py-16 px-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center text-2xl">🍃</div>
            <div>
              <p className="text-white font-black text-xl tracking-tight">CocoCast<span className="text-emerald-500">AI</span> System</p>
              <p className="text-[10px] font-bold uppercase tracking-widest text-slate-600">Precision Agriculture v2.5 | Galle Research Prototype</p>
            </div>
          </div>
          <div className="text-center md:text-right">
            <p className="text-[10px] font-black uppercase tracking-widest mb-4 text-slate-400">Scientific Reference</p>
            <p className="text-sm font-bold text-slate-300">CRI Advisory Services - Soils & Nutrition Division</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
