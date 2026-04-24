"use client";

import { motion } from "framer-motion";

export function VoiceWaveform({ state }: { state: 'idle' | 'listening' | 'thinking' | 'responding' }) {
  const bars = 20;

  return (
    <div className="flex items-end justify-center h-16 gap-1 overflow-hidden p-2 glow-border rounded w-full max-w-lg mx-auto">
      {Array.from({ length: bars }).map((_, i) => {
        let height = "10%";
        let duration = 1.5;
        let delay = i * 0.1;

        if (state === 'listening') {
          height = `${Math.random() * 60 + 20}%`;
          duration = 0.4;
          delay = Math.random() * 0.2;
        } else if (state === 'thinking') {
          height = `${Math.sin(i) * 30 + 40}%`;
          duration = 1;
          delay = i * 0.05;
        } else if (state === 'responding') {
          height = `${Math.random() * 80 + 20}%`;
          duration = 0.2;
          delay = Math.random() * 0.1;
        }

        return (
          <motion.div
            key={i}
            animate={{ height: [height, "10%", height] }}
            transition={{
              duration,
              delay,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className={`w-2 rounded-t-sm ${
              state === 'idle' ? 'bg-skynet-red opacity-30' : 'bg-skynet-glow shadow-[0_0_8px_#ff4040]'
            }`}
            style={{ height: '10%' }}
          />
        );
      })}
    </div>
  );
}
