import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

export function Scene5() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 500),
      setTimeout(() => setPhase(2), 1500),
      setTimeout(() => setPhase(3), 2500),
      setTimeout(() => setPhase(4), 4000), // exit
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div className="absolute inset-0 flex flex-col items-center justify-center overflow-hidden z-10 bg-black"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
    >
      <motion.div className="absolute inset-0"
        initial={{ opacity: 0 }}
        animate={phase >= 1 ? { opacity: 0.3 } : { opacity: 0 }}
        transition={{ duration: 2 }}
      >
        <img 
          src={`${import.meta.env.BASE_URL}images/gemini-spark.png`} 
          alt="Gemini Spark" 
          className="w-full h-full object-cover mix-blend-screen" 
        />
      </motion.div>

      <motion.div className="z-10 text-center"
        initial={{ opacity: 0, scale: 0.8, y: 20 }}
        animate={phase >= 2 ? { opacity: 1, scale: 1, y: 0 } : { opacity: 0, scale: 0.8, y: 20 }}
        transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
      >
        <h1 className="text-[6vw] font-bold font-display text-white tracking-tight mb-4">
          School Triangle<br/>
          <span className="text-gradient">Orchestrator</span>
        </h1>
        
        <motion.div className="mt-8 pt-8 border-t border-white/10"
          initial={{ opacity: 0, y: 10 }}
          animate={phase >= 3 ? { opacity: 1, y: 0 } : { opacity: 0, y: 10 }}
          transition={{ duration: 0.8 }}
        >
          <p className="text-[1.5vw] text-text-secondary font-body uppercase tracking-widest">
            Google Cloud Gen AI Academy APAC
          </p>
          <p className="text-[1.2vw] text-accent mt-2 font-mono">
            Team Pastilulus
          </p>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
