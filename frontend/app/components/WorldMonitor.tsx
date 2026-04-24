"use client";

import { motion } from "framer-motion";
import { Globe } from "lucide-react";

export function WorldMonitor({ isScanning = false }: { isScanning: boolean }) {
  return (
    <div className="flex flex-col h-full glow-border p-4 rounded bg-black/80 font-mono text-xs text-skynet-text relative mt-6">
      <div className="flex items-center gap-2 mb-4 text-skynet-glow border-b border-skynet-red pb-2">
        <Globe size={16} />
        <span className="text-sm">WORLD MONITOR</span>
      </div>

      <div className="flex-1 flex flex-col justify-center items-center relative py-4">
        {/* Radar Base */}
        <div className="relative w-full aspect-square max-w-[150px] mx-auto rounded-full overflow-hidden bg-skynet-dark border border-skynet-red flex items-center justify-center shadow-[0_0_15px_#ff4040]">
          {/* Grid circles */}
          <div className="absolute w-[80%] h-[80%] rounded-full border border-skynet-red opacity-30" />
          <div className="absolute w-[60%] h-[60%] rounded-full border border-skynet-red opacity-30" />
          <div className="absolute w-[40%] h-[40%] rounded-full border border-skynet-red opacity-30" />
          <div className="absolute w-[20%] h-[20%] rounded-full border border-skynet-red opacity-30" />
          
          {/* Crosshairs */}
          <div className="absolute w-full h-[1px] bg-skynet-red opacity-40" />
          <div className="absolute h-full w-[1px] bg-skynet-red opacity-40" />

          {/* Sweep animation */}
          {isScanning && (
            <motion.div
              className="absolute w-1/2 h-1/2 origin-bottom-right"
              style={{ 
                background: "conic-gradient(from 0deg, rgba(255, 64, 64, 0.4) 0deg, transparent 60deg)",
                left: 0,
                top: 0
              }}
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            />
          )}
          
          {/* Center blip */}
          <div className="absolute w-2 h-2 rounded-full bg-skynet-glow shadow-[0_0_8px_#ff4040]" />
          
          {/* Active scanning blips */}
          {isScanning && (
            <>
              <motion.div 
                className="absolute w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_5px_#fff]"
                style={{ top: '25%', left: '30%' }}
                animate={{ opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 2, delay: 0.5 }}
              />
              <motion.div 
                className="absolute w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_5px_#fff]"
                style={{ top: '65%', left: '75%' }}
                animate={{ opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 2, delay: 1.2 }}
              />
              <motion.div 
                className="absolute w-1 h-1 rounded-full bg-white shadow-[0_0_5px_#fff]"
                style={{ top: '80%', left: '40%' }}
                animate={{ opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 2, delay: 1.8 }}
              />
            </>
          )}
        </div>

        <div className="mt-4 text-center">
          {isScanning ? (
            <span className="text-skynet-glow animate-pulse">INTELLIGENCE FEED ACTIVE</span>
          ) : (
            <span className="text-gray-500">STANDBY MODE</span>
          )}
        </div>
      </div>
    </div>
  );
}
