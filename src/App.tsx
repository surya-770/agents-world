/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import Simulation3D from './components/Simulation3D';
import CustomCursor from './components/CustomCursor';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [activeTab, setActiveTab] = useState<'events' | 'chat'>('chat');
  const [chatMessages, setChatMessages] = useState([
    { id: 1, agent: "A1", color: "#3b82f6", time: "14:18:52", text: "Where was everyone?" },
    { id: 2, agent: "A4", color: "#a855f7", time: "14:19:05", text: "I was in Storage doing wires." },
    { id: 3, agent: "A2", color: "#ef4444", time: "14:19:12", text: "Alpha is acting kinda sus ngl" }
  ]);

  // Simulate incoming messages for effect
  useEffect(() => {
    const interval = setInterval(() => {
      const messages = [
        { agent: "A5", color: "#22c55e", text: "I can vouch for A4, I saw them." },
        { agent: "A6", color: "#eab308", text: "Skip for now?" },
        { agent: "A1", color: "#3b82f6", text: "I literally just scanned in MedBay!" },
        { agent: "A2", color: "#ef4444", text: "Cap." },
      ];
      
      if (Math.random() > 0.6 && chatMessages.length < 15) {
        const msg = messages[Math.floor(Math.random() * messages.length)];
        setChatMessages(prev => [...prev, {
          id: Date.now(),
          agent: msg.agent,
          color: msg.color,
          time: new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second:'2-digit' }),
          text: msg.text
        }]);
      }
    }, 4500);
    return () => clearInterval(interval);
  }, [chatMessages]);

  return (
    <div className="w-full h-screen bg-[#0A0B0E] text-slate-300 font-sans p-6 flex flex-col overflow-hidden">
      <CustomCursor />
      {/* Header: Simulation Stats */}
      <header className="flex items-center justify-between mb-6 border-b border-white/5 pb-4 shrink-0">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-blue-600 rounded flex items-center justify-center text-white font-bold">AW</div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight uppercase">Agents World <span className="text-blue-500 font-normal ml-2">v1.0.4-stable</span></h1>
            <p className="text-xs text-slate-500 font-mono uppercase tracking-widest hidden sm:block">Autonomous Multi-Agent Simulation Engine</p>
          </div>
        </div>
        <div className="hidden md:flex gap-8">
          <div className="text-right">
            <p className="text-[10px] text-slate-500 uppercase">Current Phase</p>
            <p className="text-sm font-semibold text-emerald-400">TASK_PHASE</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] text-slate-500 uppercase">Simulation Tick</p>
            <p className="text-sm font-mono text-white">0000428</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] text-slate-500 uppercase">LLM Backend</p>
            <p className="text-sm text-blue-400 font-semibold uppercase">Mistral-7B (Ollama)</p>
          </div>
        </div>
      </header>

      <main className="flex-1 grid grid-cols-1 md:grid-cols-12 gap-6 min-h-0">
        {/* Left Column: Agent Directory */}
        <aside className="md:col-span-3 flex flex-col gap-3 overflow-hidden">
          <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1 shrink-0">Active Agents (8)</h2>
          <div className="flex flex-col gap-2 overflow-y-auto pr-2 pb-2">
            <div className="bg-[#15171C] border border-white/5 p-3 rounded-lg flex items-center gap-3 border-l-2 border-l-blue-500 shadow-sm shrink-0">
              <div className="w-8 h-8 rounded-full bg-blue-900/30 border border-blue-500/50 flex items-center justify-center text-[10px] text-blue-400">A1</div>
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-white">Agent_Alpha</span>
                  <span className="text-[9px] px-1 bg-emerald-500/10 text-emerald-500 rounded border border-emerald-500/20">CREW</span>
                </div>
                <div className="w-full bg-white/5 h-1 mt-2 rounded-full overflow-hidden">
                  <div className="bg-blue-500 h-full w-[12%]"></div>
                </div>
              </div>
            </div>
            <div className="bg-[#15171C] border border-white/5 p-3 rounded-lg flex items-center gap-3 shadow-sm shrink-0">
              <div className="w-8 h-8 rounded-full bg-red-900/30 border border-red-500/50 flex items-center justify-center text-[10px] text-red-400">A2</div>
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-slate-400">Agent_Beta</span>
                  <span className="text-[9px] px-1 bg-red-500/10 text-red-500 rounded border border-red-500/20">IMP?</span>
                </div>
                <div className="w-full bg-white/5 h-1 mt-2 rounded-full overflow-hidden">
                  <div className="bg-red-500 h-full w-[88%]"></div>
                </div>
              </div>
            </div>
            <div className="bg-[#15171C] border border-white/5 p-3 rounded-lg flex items-center gap-3 opacity-50 grayscale shadow-sm shrink-0">
              <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] text-slate-500 line-through">A3</div>
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-slate-600">Agent_Gamma</span>
                  <span className="text-[9px] px-1 bg-slate-800 text-slate-600 rounded">DEAD</span>
                </div>
                <div className="w-full bg-white/5 h-1 mt-2 rounded-full"></div>
              </div>
            </div>
            <div className="bg-[#15171C] border border-white/5 p-3 rounded-lg flex items-center gap-3 shadow-sm shrink-0">
              <div className="w-8 h-8 rounded-full bg-purple-900/30 border border-purple-500/50 flex items-center justify-center text-[10px] text-purple-400">A4</div>
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-white">Agent_Delta</span>
                  <span className="text-[9px] px-1 bg-emerald-500/10 text-emerald-500 rounded border border-emerald-500/20">CREW</span>
                </div>
                <div className="w-full bg-white/5 h-1 mt-2 rounded-full overflow-hidden">
                  <div className="bg-purple-500 h-full w-[35%]"></div>
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* Center Content: Simulation Visualization */}
        <section className="md:col-span-6 flex flex-col gap-6 overflow-hidden">
          <div className="flex-1 bg-[#0A0B0E] border border-blue-500/20 rounded-xl relative overflow-hidden flex flex-col min-h-[300px] shadow-[0_0_15px_rgba(59,130,246,0.1)]">
            <div className="absolute top-4 left-4 z-10 pointer-events-none">
              <span className="px-2 py-1 bg-blue-500/80 text-white text-[10px] font-bold rounded uppercase tracking-tighter shadow-md backdrop-blur-sm">Live 3D Feed</span>
            </div>
            {/* 3D Canvas */}
            <div className="absolute inset-0 pointer-events-auto">
              <Simulation3D />
            </div>
          </div>
          <div className="h-48 shrink-0 bg-[#15171C] border border-white/5 rounded-xl p-4 flex flex-col">
            <h3 className="text-[10px] font-bold text-slate-500 uppercase mb-3 flex justify-between shrink-0">
              <span>LLM Inference Stream</span>
              <span className="text-blue-500">LATENCY: 1240ms</span>
            </h3>
            <div className="flex-1 bg-black/40 rounded p-3 font-mono text-[11px] text-slate-400 overflow-y-auto leading-relaxed">
              <p className="text-blue-400 mb-1">[DECIDE] Agent_Alpha invoking mistral:decide.txt</p>
              <p className="pl-4 italic mb-1 text-slate-300">"I am currently in the MedBay completing the 'Scan' task. I observed Agent_Beta entering from the cafeteria. Suspicion level for Beta is 0.45. My next action should be moving to Electrical to check the lights."</p>
              <p className="text-emerald-400 mt-2">[ACTION] Agent_Alpha performing: MOVE_TO(Electrical)</p>
            </div>
          </div>
        </section>

        {/* Right Column: System Logs & Chat */}
        <aside className="md:col-span-3 flex flex-col gap-4 overflow-hidden">
          <div className="flex-1 bg-[#15171C] border border-white/5 rounded-xl flex flex-col overflow-hidden shadow-lg">
            
            {/* Tabs Header */}
            <div className="flex border-b border-white/5 shrink-0 bg-black/20">
              <button 
                onClick={() => setActiveTab('events')}
                className={`flex-1 py-3 text-[10px] font-bold uppercase tracking-widest transition-colors ${activeTab === 'events' ? 'text-blue-400 border-b-2 border-blue-500 bg-blue-500/5' : 'text-slate-500 hover:text-slate-300'}`}
              >
                Event Log
              </button>
              <button 
                onClick={() => setActiveTab('chat')}
                className={`flex-1 py-3 text-[10px] font-bold uppercase tracking-widest transition-colors ${activeTab === 'chat' ? 'text-amber-400 border-b-2 border-amber-500 bg-amber-500/5' : 'text-slate-500 hover:text-slate-300'}`}
              >
                Agent Chat
              </button>
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-hidden relative">
              <AnimatePresence mode="wait">
                {activeTab === 'events' ? (
                  <motion.div 
                    key="events"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 10 }}
                    className="absolute inset-0 p-4 overflow-y-auto space-y-4"
                  >
                    <div className="flex gap-3 items-start">
                      <div className="w-1 h-1 rounded-full bg-slate-500 mt-2 shrink-0"></div>
                      <div className="text-[11px]">
                        <p className="text-slate-500 font-mono">14:20:01</p>
                        <p className="text-white">Agent_Alpha finished task <span className="text-emerald-400 font-bold">WIRING</span></p>
                      </div>
                    </div>
                    <div className="flex gap-3 items-start">
                      <div className="w-1 h-1 rounded-full bg-red-500 mt-2 shrink-0"></div>
                      <div className="text-[11px]">
                        <p className="text-slate-500 font-mono">14:19:42</p>
                        <p className="text-white">Agent_Beta reported <span className="text-red-400 font-bold">BODY_FOUND</span> in Cafeteria</p>
                      </div>
                    </div>
                    <div className="flex gap-3 items-start">
                      <div className="w-1 h-1 rounded-full bg-slate-500 mt-2 shrink-0"></div>
                      <div className="text-[11px]">
                        <p className="text-slate-500 font-mono">14:19:15</p>
                        <p className="text-white">Agent_Gamma state set to <span className="text-slate-500 italic">DECEASED</span></p>
                      </div>
                    </div>
                    <div className="flex gap-3 items-start">
                       <div className="w-1 h-1 rounded-full bg-blue-500 mt-2 shrink-0"></div>
                       <div className="text-[11px]">
                         <p className="text-slate-500 font-mono">14:18:50</p>
                         <p className="text-white">Global Phase transition: <span className="text-blue-400">TASK</span> &rarr; <span className="text-amber-400">DISCUSSION</span></p>
                       </div>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div 
                    key="chat"
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                    className="absolute inset-0 p-4 overflow-y-auto flex flex-col gap-3"
                  >
                    <AnimatePresence>
                      {chatMessages.map((msg) => (
                        <motion.div 
                          key={msg.id}
                          initial={{ opacity: 0, scale: 0.9, y: 10 }}
                          animate={{ opacity: 1, scale: 1, y: 0 }}
                          layout
                          className="bg-black/30 border border-white/5 rounded-lg p-2.5 pb-3 shadow-md"
                        >
                          <div className="flex items-center justify-between mb-1">
                            <div className="flex items-center gap-1.5">
                              <div className="w-3 h-3 rounded-full shadow-sm" style={{ backgroundColor: msg.color }}></div>
                              <span className="text-xs font-bold" style={{ color: msg.color }}>{msg.agent}</span>
                            </div>
                            <span className="text-[9px] text-slate-500 font-mono">{msg.time}</span>
                          </div>
                          <p className="text-slate-300 text-[11px] leading-relaxed ml-4.5">{msg.text}</p>
                        </motion.div>
                      ))}
                      {/* Fake typing indicator */}
                      <motion.div 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: [0.5, 1, 0.5] }}
                        transition={{ repeat: Infinity, duration: 1.5 }}
                        className="text-[10px] text-slate-500 italic pl-4"
                      >
                        Agents are discussing...
                      </motion.div>
                    </AnimatePresence>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
          <div className="h-32 shrink-0 bg-blue-600/10 border border-blue-500/20 rounded-xl p-4 flex flex-col justify-center items-center text-center">
            <p className="text-[10px] text-blue-400 font-bold uppercase tracking-widest mb-1">Simulation Goal</p>
            <p className="text-xs text-white leading-tight">Crewmates must finish all tasks or identify the impostor before the total agent count drops to 2.</p>
          </div>
        </aside>
      </main>

      {/* Footer: System Health */}
      <footer className="mt-auto pt-4 flex justify-between items-center text-[10px] text-slate-500 font-mono shrink-0 border-t border-white/5">
        <div className="flex gap-4">
          <span>CPU: 42%</span>
          <span>MEM: 2.1GB / 16GB</span>
          <span className="hidden sm:inline">OLLAMA: CONNECTED</span>
        </div>
        <div className="flex gap-4">
          <span className="text-emerald-500">● STABLE</span>
          <span>SESS_20231027_0041</span>
        </div>
      </footer>
    </div>
  );
}
