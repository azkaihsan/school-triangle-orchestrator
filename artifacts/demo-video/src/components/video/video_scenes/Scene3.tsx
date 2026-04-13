import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const endpoints = [
  { method: "POST", path: "/orchestrate", desc: "Triggers multi-agent workflow" },
  { method: "GET", path: "/students/{id}", desc: "Retrieves holistic profile" },
  { method: "POST", path: "/schedule", desc: "Books optimized meetings" }
];

export function Scene3() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 300),
      setTimeout(() => setPhase(2), 800), // title
      setTimeout(() => setPhase(3), 1200), // list
      setTimeout(() => setPhase(4), 3800), // exit
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div className="absolute inset-0 flex items-center justify-center overflow-hidden z-10"
      initial={{ clipPath: 'circle(0% at 50% 50%)' }}
      animate={{ clipPath: 'circle(150% at 50% 50%)' }}
      exit={{ opacity: 0, scale: 1.1 }}
      transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="flex w-full h-full">
        <div className="w-1/2 p-[10vw] flex flex-col justify-center">
          <motion.h2 className="text-[4vw] font-bold font-display text-white mb-8 leading-tight"
            initial={{ opacity: 0, x: -30 }}
            animate={phase >= 2 ? { opacity: 1, x: 0 } : { opacity: 0, x: -30 }}
            transition={{ duration: 0.8 }}
          >
            Powerful API<br/>
            <span className="text-gradient">Data Flows</span>
          </motion.h2>
          
          <div className="space-y-6">
            {endpoints.map((ep, i) => (
              <motion.div key={i} className="flex items-center gap-6"
                initial={{ opacity: 0, x: -50 }}
                animate={phase >= 3 ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
                transition={{ duration: 0.6, delay: phase >= 3 ? i * 0.2 : 0, type: 'spring' }}
              >
                <span className={`px-4 py-2 rounded font-mono text-[1.2vw] font-bold ${ep.method === 'POST' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>
                  {ep.method}
                </span>
                <div>
                  <div className="font-mono text-[1.5vw] text-white">{ep.path}</div>
                  <div className="font-body text-[1vw] text-text-secondary">{ep.desc}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
        
        <div className="w-1/2 relative flex items-center justify-center">
          {/* Animated data lines representation */}
          <svg className="w-full h-full absolute inset-0 opacity-50" viewBox="0 0 100 100" preserveAspectRatio="none">
            <motion.path 
              d="M 0,50 C 30,50 40,20 60,20 C 80,20 90,80 100,80" 
              fill="none" stroke="#38bdf8" strokeWidth="0.5"
              initial={{ pathLength: 0 }}
              animate={phase >= 2 ? { pathLength: 1, strokeDasharray: ["5 5", "10 10"] } : { pathLength: 0 }}
              transition={{ duration: 2, ease: "linear" }}
            />
            <motion.path 
              d="M 0,80 C 40,80 50,40 70,40 C 85,40 95,60 100,60" 
              fill="none" stroke="#818cf8" strokeWidth="0.5"
              initial={{ pathLength: 0 }}
              animate={phase >= 2 ? { pathLength: 1 } : { pathLength: 0 }}
              transition={{ duration: 2.5, ease: "linear", delay: 0.2 }}
            />
          </svg>
        </div>
      </div>
    </motion.div>
  );
}
