"use client";

import { useState, useRef, useEffect } from "react";
import { Activity, Shield } from "lucide-react";
import { AIOrb } from "./components/AIOrb";
import { VoiceWaveform } from "./components/VoiceWaveform";
import { Console, ConsoleMessage } from "./components/Console";
import { TelemetryPanel } from "./components/TelemetryPanel";
import { ThinkingStream } from "./components/ThinkingStream";
import { WorldMonitor } from "./components/WorldMonitor";

export default function Home() {
  const [status, setStatus] = useState("System Offline");
  const [messages, setMessages] = useState<ConsoleMessage[]>([
    { type: 'system', content: 'INITIALIZING SKYNET CORE...' },
    { type: 'system', content: 'ESTABLISHING NEURAL LINK...' }
  ]);
  const [agentState, setAgentState] = useState<'idle' | 'listening' | 'thinking' | 'responding'>('idle');
  const [systemTools, setSystemTools] = useState<string[]>([]);
  const [isBrowser, setIsBrowser] = useState(false);
  const [isScanningWorld, setIsScanningWorld] = useState(false);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    if (typeof navigator !== "undefined") setIsBrowser(true);
    
    fetch("http://127.0.0.1:8001/health")
      .then(r => r.json())
      .then(d => {
        setStatus(`SKYNET Core: ${d.status.toUpperCase()}`);
        setMessages(prev => [...prev, { type: 'system', content: 'BACKEND CONNECTION ESTABLISHED.' }]);
      })
      .catch(() => setStatus("SKYNET Core: OFFLINE"));
      
    fetch("http://127.0.0.1:8001/tools")
      .then(r => r.json())
      .then(d => setSystemTools(d.tools))
      .catch(() => setSystemTools([]));
  }, []);

  const handleStartRecording = async () => {
    if (!navigator || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error("Microphone API not supported.");
      alert("Microphone not available. Use HTTPS or localhost.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");

        setAgentState('thinking');
        setMessages(prev => [...prev, { type: 'system', content: '[SKYNET] Voice received' }]);
        
        const logTimeouts = [
          setTimeout(() => setMessages(prev => [...prev, { type: 'system', content: '[SKYNET] Transcribing audio' }]), 800),
          setTimeout(() => setMessages(prev => [...prev, { type: 'system', content: '[SKYNET] Searching global intelligence grid' }]), 2500),
          setTimeout(() => setMessages(prev => [...prev, { type: 'system', content: '[SKYNET] Synthesizing response' }]), 4500)
        ];
        
        try {
          const res = await fetch("http://127.0.0.1:8001/voice", {
            method: "POST",
            body: formData,
          });
          
          if (res.ok) {
            setAgentState('responding');
            
            if (res.headers.get("x-tool-activated") === "world_monitor") {
              setIsScanningWorld(true);
              setMessages(prev => [...prev, { type: 'system', content: '[GLOBAL INTELLIGENCE FEED ACTIVATED]' }]);
            } else {
              setIsScanningWorld(false);
            }
            
            const blob = await res.blob();
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.onended = () => setAgentState('idle');
            audio.play();
            setMessages(prev => [...prev, { type: 'skynet', content: '[AUDIO RESPONSE PLAYING]' }]);
          } else {
            setAgentState('idle');
            setMessages(prev => [...prev, { type: 'system', content: 'Connection to SKYNET backend lost.' }]);
          }
        } catch (e) {
          console.error(e);
          setAgentState('idle');
          setMessages(prev => [...prev, { type: 'system', content: 'Connection to SKYNET backend lost.' }]);
        } finally {
          logTimeouts.forEach(clearTimeout);
        }
      };

      recorder.start();
      setAgentState('listening');
      
    } catch (error) {
      console.error("Microphone permission denied:", error);
      setMessages(prev => [...prev, { type: 'system', content: 'MICROPHONE ACCESS DENIED.' }]);
    }
  };

  const handleStopRecording = () => {
    if (mediaRecorderRef.current && agentState === 'listening') {
      mediaRecorderRef.current.stop();
    }
  };

  return (
    <>
      <div className="scanlines" />
      <div className="grid-bg" />
      
      <div className="h-screen flex flex-col p-6 z-10 relative pointer-events-auto">
        <header className="flex justify-between items-center border-b-2 border-skynet-red pb-4 mb-4">
          <div className="flex items-center gap-4">
            <Shield className="text-skynet-glow drop-shadow-[0_0_10px_#ff4040]" size={40} />
            <div>
              <h1 className="text-4xl font-black text-skynet-glow glow-text tracking-[0.3em]">SKYNET</h1>
              <div className="text-xs tracking-[0.5em] text-skynet-red">GLOBAL DEFENSE NETWORK</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Activity className="text-skynet-glow animate-pulse" size={24} />
            <div className="text-sm font-mono glow-text text-skynet-glow uppercase">{status}</div>
          </div>
        </header>

        <div className="flex-1 flex gap-6 overflow-hidden">
          <div className="w-1/4 min-w-[300px]">
            <Console messages={messages} />
          </div>

          <div className="flex-1 flex flex-col relative justify-center items-center">
            <ThinkingStream isThinking={agentState === 'thinking'} />
            <div 
              className="cursor-pointer"
              onMouseDown={isBrowser ? handleStartRecording : undefined}
              onMouseUp={isBrowser ? handleStopRecording : undefined}
              onTouchStart={isBrowser ? handleStartRecording : undefined}
              onTouchEnd={isBrowser ? handleStopRecording : undefined}
            >
              <AIOrb isSpeaking={agentState === 'responding'} isListening={agentState === 'listening'} />
            </div>
            
            <div className="mt-12 text-center text-sm font-mono text-skynet-red tracking-widest opacity-80">
              {agentState === 'idle' && "HOLD CORE TO INITIATE VOICE OVERRIDE"}
              {agentState === 'listening' && "Listening..."}
              {agentState === 'thinking' && "Processing audio..."}
              {agentState === 'responding' && "TRANSMITTING..."}
            </div>
          </div>

          <div className="w-1/4 min-w-[300px] flex flex-col">
            <TelemetryPanel toolsCount={systemTools.length} backendStatus={status} />
            <WorldMonitor isScanning={isScanningWorld} />
          </div>
        </div>

        <div className="mt-4">
          <VoiceWaveform state={agentState} />
        </div>
      </div>
    </>
  );
}
