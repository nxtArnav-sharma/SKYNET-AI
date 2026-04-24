"use client";

import { useEffect, useState, useRef } from "react";
import { Activity, Shield, Globe, Mic, Brain, Server } from "lucide-react";
import { motion } from "framer-motion";

export default function Dashboard() {
  const [logs, setLogs] = useState<string[]>([]);
  const [status, setStatus] = useState("System Offline");
  const [agentState, setAgentState] = useState("IDLE");
  const [activeTool, setActiveTool] = useState("NONE");
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect WebSocket
    const ws = new WebSocket("ws://127.0.0.1:8001/ws/events");
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("SKYNET Core: ONLINE");
      setLogs(prev => [...prev, "[SYSTEM] WebSocket Connected"]);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.event === "voice_received") {
          setAgentState("LISTENING");
          setLogs(prev => [...prev, "[AUDIO] Voice packet received"]);
        } else if (data.event === "transcribing") {
          setAgentState("TRANSCRIBING");
          setLogs(prev => [...prev, "[STT] Processing audio waveform..."]);
        } else if (data.event === "thinking") {
          setAgentState("THINKING");
          setLogs(prev => [...prev, `[LLM] Query: ${data.query}`]);
        } else if (data.event === "tool_called") {
          setActiveTool(data.tool);
          setLogs(prev => [...prev, `[MCP] Activating tool: ${data.tool}`]);
        } else if (data.event === "speaking") {
          setAgentState("SPEAKING");
          setActiveTool("NONE");
          setLogs(prev => [...prev, "[TTS] Synthesizing output stream..."]);
        }
      } catch (e) {
        console.error("WebSocket message error:", e);
      }
    };

    ws.onclose = () => {
      setStatus("SKYNET Core: OFFLINE");
      setLogs(prev => [...prev, "[SYSTEM] WebSocket Disconnected"]);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="min-h-screen bg-[#050b14] text-cyan-400 font-mono p-6 relative overflow-hidden">
      {/* Holographic background effects */}
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20 pointer-events-none" />
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-cyan-900/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-900/20 blur-[120px] rounded-full pointer-events-none" />

      <header className="flex justify-between items-center border-b border-cyan-500/30 pb-4 mb-6 relative z-10">
        <div className="flex items-center gap-4">
          <Shield className="text-cyan-400 drop-shadow-[0_0_8px_#22d3ee]" size={36} />
          <div>
            <h1 className="text-3xl font-black tracking-[0.2em] drop-shadow-[0_0_8px_#22d3ee]">SKYNET</h1>
            <div className="text-xs tracking-[0.4em] text-cyan-600">COMMAND CENTER</div>
          </div>
        </div>
        <div className="flex items-center gap-3 bg-cyan-950/40 px-4 py-2 rounded border border-cyan-800/50">
          <Activity className="animate-pulse" size={18} />
          <span className="text-sm tracking-widest">{status}</span>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-6 relative z-10 h-[calc(100vh-120px)]">
        
        {/* Left Column */}
        <div className="col-span-3 flex flex-col gap-6">
          <div className="bg-cyan-950/20 border border-cyan-500/20 rounded-lg p-4 backdrop-blur-md flex-1">
            <h2 className="text-xs tracking-widest text-cyan-600 mb-4 flex items-center gap-2 border-b border-cyan-800/50 pb-2">
              <Mic size={14} /> AUDIO INTERFACE
            </h2>
            <div className="flex flex-col items-center justify-center h-[200px]">
              <motion.div 
                animate={{ 
                  scale: agentState === "LISTENING" ? [1, 1.2, 1] : 1,
                  opacity: agentState === "LISTENING" ? 1 : 0.5
                }}
                transition={{ repeat: Infinity, duration: 1.5 }}
                className="w-24 h-24 rounded-full border-2 border-cyan-500/50 flex items-center justify-center shadow-[0_0_20px_rgba(34,211,238,0.2)]"
              >
                <Mic size={32} className={agentState === "LISTENING" ? "text-cyan-300" : "text-cyan-700"} />
              </motion.div>
              <div className="mt-6 text-sm tracking-widest">{agentState === "LISTENING" ? "RECEIVING SIGNAL" : "AWAITING INPUT"}</div>
            </div>
          </div>

          <div className="bg-cyan-950/20 border border-cyan-500/20 rounded-lg p-4 backdrop-blur-md flex-1">
            <h2 className="text-xs tracking-widest text-cyan-600 mb-4 flex items-center gap-2 border-b border-cyan-800/50 pb-2">
              <Brain size={14} /> NEURAL CORE
            </h2>
            <div className="flex flex-col items-center justify-center h-[200px]">
               <motion.div 
                animate={{ 
                  rotate: agentState === "THINKING" ? 360 : 0
                }}
                transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
                className="relative w-24 h-24"
              >
                <div className={`absolute inset-0 rounded-full border-2 border-dashed ${agentState === "THINKING" ? "border-cyan-400" : "border-cyan-800"}`}></div>
                <div className="absolute inset-2 rounded-full border-2 border-cyan-700/50"></div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <Brain size={28} className={agentState === "THINKING" ? "text-cyan-300 animate-pulse" : "text-cyan-800"} />
                </div>
              </motion.div>
              <div className="mt-6 text-sm tracking-widest">{agentState === "THINKING" ? "PROCESSING" : "STANDBY"}</div>
            </div>
          </div>
        </div>

        {/* Center Column */}
        <div className="col-span-6 flex flex-col gap-6">
          <div className="bg-cyan-950/20 border border-cyan-500/20 rounded-lg p-4 backdrop-blur-md h-2/3 flex flex-col">
            <h2 className="text-xs tracking-widest text-cyan-600 mb-4 flex items-center gap-2 border-b border-cyan-800/50 pb-2">
              <Globe size={14} /> GLOBAL INTELLIGENCE GRID
            </h2>
            <div className="flex-1 relative overflow-hidden flex items-center justify-center bg-cyan-950/30 rounded border border-cyan-800/30">
              {/* Radar effect */}
              <div className="absolute w-[400px] h-[400px] border border-cyan-500/20 rounded-full"></div>
              <div className="absolute w-[300px] h-[300px] border border-cyan-500/30 rounded-full"></div>
              <div className="absolute w-[200px] h-[200px] border border-cyan-500/40 rounded-full"></div>
              <div className="absolute w-[100px] h-[100px] border border-cyan-500/50 rounded-full"></div>
              <motion.div 
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
                className="absolute w-[400px] h-[400px]"
                style={{
                  background: 'conic-gradient(from 0deg, transparent 0deg, transparent 270deg, rgba(34,211,238,0.2) 360deg)',
                  borderRadius: '50%'
                }}
              />
              <div className="absolute flex items-center justify-center">
                {activeTool !== "NONE" ? (
                  <div className="bg-cyan-900/80 px-6 py-3 rounded border border-cyan-400 drop-shadow-[0_0_10px_#22d3ee] flex flex-col items-center">
                    <span className="text-xs tracking-widest text-cyan-200 mb-1">TOOL ACTIVATED</span>
                    <span className="text-lg font-bold">{activeTool}</span>
                  </div>
                ) : (
                  <div className="text-cyan-700 tracking-widest text-xs">MONITORING</div>
                )}
              </div>
            </div>
          </div>
          
          <div className="bg-cyan-950/20 border border-cyan-500/20 rounded-lg p-4 backdrop-blur-md h-1/3 flex flex-col">
            <h2 className="text-xs tracking-widest text-cyan-600 mb-2 flex items-center gap-2 border-b border-cyan-800/50 pb-2">
              <Server size={14} /> LIVE LOGS
            </h2>
            <div className="flex-1 overflow-y-auto text-xs space-y-2 font-mono mt-2 pr-2 custom-scrollbar">
              {logs.map((log, i) => (
                <div key={i} className="text-cyan-400/80 break-words border-l-2 border-cyan-500/30 pl-2 py-1">
                  {log}
                </div>
              ))}
              <div className="animate-pulse">_</div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="col-span-3 flex flex-col gap-6">
          <div className="bg-cyan-950/20 border border-cyan-500/20 rounded-lg p-4 backdrop-blur-md flex-1 overflow-hidden flex flex-col">
            <h2 className="text-xs tracking-widest text-cyan-600 mb-4 flex items-center gap-2 border-b border-cyan-800/50 pb-2">
               NEWS FEED
            </h2>
            <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-4">
              <div className="p-3 bg-cyan-900/10 border border-cyan-800/50 rounded">
                <div className="text-xs text-cyan-500 mb-1">GLOBAL EVENT</div>
                <div className="text-sm text-cyan-100">Live intelligence feed standing by...</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
