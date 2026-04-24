"use client";

import { useEffect, useRef } from "react";
import { TerminalSquare } from "lucide-react";

export type ConsoleMessage = {
  type: 'user' | 'skynet' | 'tool' | 'system';
  content: string;
};

export function Console({ messages }: { messages: ConsoleMessage[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full glow-border p-4 rounded bg-black/80 font-mono text-sm relative overflow-hidden">
      <div className="flex items-center gap-2 mb-4 text-skynet-glow border-b border-skynet-red pb-2">
        <TerminalSquare size={16} />
        <span>COMMAND CONSOLE</span>
      </div>
      
      <div className="flex-1 overflow-y-auto scroll-hide space-y-2 pr-2">
        {messages.map((msg, idx) => (
          <div key={idx} className="flex flex-col">
            <span className={`opacity-80 ${
              msg.type === 'user' ? 'text-blue-400' :
              msg.type === 'tool' ? 'text-yellow-400' :
              msg.type === 'system' ? 'text-gray-400' :
              'text-skynet-glow glow-text'
            }`}>
              &gt; {msg.type.toUpperCase()}: {msg.content}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
