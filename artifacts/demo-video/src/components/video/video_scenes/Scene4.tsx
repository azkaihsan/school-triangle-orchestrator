import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const techStack = [
  "Python", "FastAPI", "Gemini 2.5 Flash", "PostgreSQL"
];

export function Scene4() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),
      setTimeout(() => setPhase(2), 600),
      setTimeout(() => setPhase(3), 1200), // items
      setTimeout(() => setPhase(4), 3300), // exit
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div className="absolute inset-0 flex flex-col items-center justify-center overflow-hidden z-10"
      initial={{ filter: 'blur(20px)', opacity: 0 }}
      animate={{ filter: 'blur(0px)', opacity: 1 }}
      exit={{ scale: 1.5, opacity: 0 }}
      transition={{ duration: 0.8 }}
    >
      <motion.div className="absolute w-[60vw] h-[60vw] border border-accent/20 rounded-full"
        animate={{ rotate: 360, scale: [1, 1.05, 1] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
      />
      <motion.div className="absolute w-[40vw] h-[40vw] border border-accent-alt/20 rounded-full"
        animate={{ rotate: -360, scale: [1, 0.95, 1] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
      />

      <motion.h2 className="text-[3vw] font-bold font-display text-white mb-12"
        initial={{ opacity: 0, y: -20 }}
        animate={phase >= 2 ? { opacity: 1, y: 0 } : { opacity: 0, y: -20 }}
        transition={{ duration: 0.6 }}
      >
        Built on modern infrastructure
      </motion.h2>

      <div className="flex flex-wrap justify-center gap-6 max-w-4xl z-10">
        {techStack.map((tech, i) => (
          <motion.div key={i}
            className="px-8 py-4 glass-panel rounded-full text-[2vw] font-mono text-white border-accent/30"
            initial={{ opacity: 0, scale: 0.5, y: 20 }}
            animate={phase >= 3 ? { opacity: 1, scale: 1, y: 0 } : { opacity: 0, scale: 0.5, y: 20 }}
            transition={{ duration: 0.5, delay: phase >= 3 ? i * 0.15 : 0, type: 'spring' }}
            whileHover={{ scale: 1.05, borderColor: 'rgba(56, 189, 248, 0.8)' }} // Just visual for demo
          >
            {tech}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
