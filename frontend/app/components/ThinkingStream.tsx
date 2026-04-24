"use client";

import { motion } from "framer-motion";
import { BrainCircuit } from "lucide-react";
import { useEffect, useState } from "react";

export function ThinkingStream({ isThinking }: { isThinking: boolean }) {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    if (!isThinking) {
      setLogs([]);
      return;
    }
    
    const phrases = [
      "Scanning intelligence feeds...",
      "Analyzing global signals...",
      "Cross-referencing global knowledge base...",
      "Synthesizing information...",
      "Aligning neural pathways..."
    ];
    
    let i = 0;
    const interval = setInterval(() => {
      setLogs(prev => [...prev.slice(-4), phrases[i % phrases.length]]);
      i++;
    }, 800);
    
    return () => clearInterval(interval);
  }, [isThinking]);

  if (!isThinking) return null;

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="absolute top-4 left-1/2 -translate-x-1/2 flex items-center gap-2 bg-black/60 px-4 py-2 rounded-full border border-skynet-glow text-xs font-mono text-skynet-glow"
    >
      <BrainCircuit size={14} className="animate-pulse" />
      <span className="animate-pulse">{logs[logs.length - 1] || "Initializing thought process..."}</span>
    </motion.div>
  );
}
