import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const agents = [
  { title: "Student Insight", desc: "Monitors progress and learning styles", color: "from-blue-400 to-blue-600" },
  { title: "Teacher Action", desc: "Generates tailored interventions", color: "from-indigo-400 to-indigo-600" },
  { title: "Parent Comm", desc: "Translates updates for engagement", color: "from-purple-400 to-purple-600" },
  { title: "Scheduling", desc: "Coordinates cross-party meetings", color: "from-cyan-400 to-cyan-600" }
];

export function Scene2() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),
      setTimeout(() => setPhase(2), 600), // title
      setTimeout(() => setPhase(3), 1000), // cards start
      setTimeout(() => setPhase(4), 4300), // exit
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div className="absolute inset-0 flex flex-col items-center justify-center overflow-hidden z-10 px-[10vw]"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -50, filter: 'blur(10px)' }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
    >
      <motion.h2 className="text-[3.5vw] font-bold font-display text-white mb-16 text-center"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={phase >= 2 ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.9 }}
        transition={{ duration: 0.8 }}
      >
        Four specialized <span className="text-gradient-gold">Gemini Agents</span>
      </motion.h2>

      <div className="grid grid-cols-2 gap-8 w-full max-w-5xl">
        {agents.map((agent, i) => (
          <motion.div key={i}
            className="glass-panel p-8 rounded-2xl relative overflow-hidden"
            initial={{ opacity: 0, y: 30, rotateX: 20 }}
            animate={phase >= 3 ? { opacity: 1, y: 0, rotateX: 0 } : { opacity: 0, y: 30, rotateX: 20 }}
            transition={{ duration: 0.8, delay: phase >= 3 ? i * 0.15 : 0, type: 'spring', bounce: 0.4 }}
          >
            <div className={`absolute top-0 left-0 w-2 h-full bg-gradient-to-b ${agent.color}`} />
            <h3 className="text-[2vw] font-bold text-white mb-2 font-display">{agent.title}</h3>
            <p className="text-[1.2vw] text-text-secondary font-body">{agent.desc}</p>
          </motion.div>
        ))}
      </div>
      
      <motion.div className="absolute right-[5vw] top-[10vh] opacity-20 w-[30vw] pointer-events-none"
        animate={{ rotate: 360 }}
        transition={{ duration: 40, repeat: Infinity, ease: 'linear' }}
      >
        <img src={`${import.meta.env.BASE_URL}images/ai-brain.png`} alt="" className="w-full h-full object-contain" />
      </motion.div>
    </motion.div>
  );
}
