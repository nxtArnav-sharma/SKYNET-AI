"use client";

import { Activity, Cpu, HardDrive, Network, ShieldAlert } from "lucide-react";
import { useEffect, useState } from "react";

export function TelemetryPanel({ toolsCount, backendStatus }: { toolsCount: number, backendStatus: string }) {
  const [cpu, setCpu] = useState(0);
  const [ram, setRam] = useState(0);
  const [net, setNet] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCpu(Math.floor(Math.random() * 20) + 10);
      setRam(Math.floor(Math.random() * 10) + 40);
      setNet(Math.floor(Math.random() * 50) + 10);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col h-full glow-border p-4 rounded bg-black/80 font-mono text-xs text-skynet-text relative">
      <div className="flex items-center gap-2 mb-4 text-skynet-glow border-b border-skynet-red pb-2">
        <Activity size={16} />
        <span className="text-sm">SYSTEM TELEMETRY</span>
      </div>

      <div className="space-y-4 flex-1">
        <div>
          <div className="flex justify-between text-skynet-red mb-1">
            <span className="flex items-center gap-1"><Cpu size={12} /> CPU USAGE</span>
            <span>{cpu}%</span>
          </div>
          <div className="w-full bg-skynet-dark h-2 rounded overflow-hidden">
            <div className="bg-skynet-glow h-full" style={{ width: `${cpu}%` }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-skynet-red mb-1">
            <span className="flex items-center gap-1"><HardDrive size={12} /> RAM ALLOCATION</span>
            <span>{ram}%</span>
          </div>
          <div className="w-full bg-skynet-dark h-2 rounded overflow-hidden">
            <div className="bg-skynet-glow h-full" style={{ width: `${ram}%` }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-skynet-red mb-1">
            <span className="flex items-center gap-1"><Network size={12} /> NET UPLINK</span>
            <span>{net} MB/s</span>
          </div>
        </div>

        <div className="pt-4 border-t border-skynet-dark">
          <div className="flex justify-between mb-2">
            <span className="text-gray-500">BACKEND STATE</span>
            <span className={backendStatus.includes('online') ? 'text-green-500' : 'text-skynet-glow'}>{backendStatus.toUpperCase()}</span>
          </div>
          <div className="flex justify-between mb-2">
            <span className="text-gray-500">LOADED MODULES</span>
            <span className="text-skynet-text">{toolsCount} ACTIVE</span>
          </div>
          <div className="flex items-center gap-2 mt-4 text-skynet-glow animate-pulse">
            <ShieldAlert size={14} />
            <span>CORE PROTECTION ACTIVE</span>
          </div>
        </div>
      </div>
    </div>
  );
}
