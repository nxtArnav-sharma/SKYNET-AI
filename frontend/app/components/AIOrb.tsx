"use client";

import { motion } from "framer-motion";

export function AIOrb({ isSpeaking, isListening }: { isSpeaking: boolean, isListening: boolean }) {
  // Determine the core visual state
  let scale = 1;
  let pulseDuration = 4;
  let glowIntensity = "0 0 40px var(--color-skynet-glow)";
  
  if (isListening) {
    scale = 1.1;
    pulseDuration = 1.5;
    glowIntensity = "0 0 60px var(--color-skynet-glow), 0 0 100px var(--color-skynet-red)";
  } else if (isSpeaking) {
    scale = 1.2;
    pulseDuration = 0.5;
    glowIntensity = "0 0 80px var(--color-skynet-glow), 0 0 150px var(--color-skynet-red)";
  }

  return (
    <div className="relative flex items-center justify-center w-64 h-64">
      {/* Outer rotating ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
        className="absolute w-full h-full border-2 border-skynet-red rounded-full opacity-30 border-t-skynet-glow"
        style={{ borderStyle: 'dashed' }}
      />
      
      {/* Inner counter-rotating ring */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
        className="absolute w-48 h-48 border-2 border-skynet-glow rounded-full opacity-40 border-b-transparent"
      />

      {/* The Core Orb */}
      <motion.div
        animate={{ 
          scale: [scale, scale * 1.05, scale],
          boxShadow: glowIntensity
        }}
        transition={{ 
          duration: pulseDuration, 
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="relative w-32 h-32 rounded-full bg-gradient-to-br from-skynet-glow to-skynet-dark z-10"
      >
        <div className="absolute inset-0 rounded-full bg-skynet-red mix-blend-overlay opacity-50 blur-sm"></div>
      </motion.div>
    </div>
  );
}
