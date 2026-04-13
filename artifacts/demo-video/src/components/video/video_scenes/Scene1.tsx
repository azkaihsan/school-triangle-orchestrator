import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

export function Scene1() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),
      setTimeout(() => setPhase(2), 1000),
      setTimeout(() => setPhase(3), 1800),
      setTimeout(() => setPhase(4), 2600),
      setTimeout(() => setPhase(5), 3800), // exit
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div className="absolute inset-0 flex items-center justify-center overflow-hidden z-10"
      initial={{ opacity: 0, scale: 1.1 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="absolute left-[10vw] top-[30vh] w-[40vw]">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: phase >= 1 ? '3rem' : 0 }}
          className="h-1 bg-accent mb-6"
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
        
        <motion.h1 className="text-[5vw] font-bold leading-[1.1] font-display text-white"
          initial={{ opacity: 0, y: 30 }}
          animate={phase >= 2 ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          Unifying the<br/>
          <span className="text-gradient">School Triangle</span>
        </motion.h1>
        
        <motion.p className="text-[1.8vw] text-text-secondary mt-6 font-body max-w-lg"
          initial={{ opacity: 0 }}
          animate={phase >= 3 ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 0.8 }}
        >
          AI-powered orchestration for Students, Teachers, and Parents.
        </motion.p>
      </div>

      <motion.div className="absolute right-[10vw] top-[20vh] w-[40vw] h-[60vh] flex items-center justify-center"
        initial={{ opacity: 0, x: 50 }}
        animate={phase >= 4 ? { opacity: 1, x: 0 } : { opacity: 0, x: 50 }}
        transition={{ duration: 1, type: 'spring', bounce: 0.3 }}
      >
        <img 
          src={`${import.meta.env.BASE_URL}images/triangle-nodes.png`} 
          alt="Triangle Nodes" 
          className="w-full h-full object-contain drop-shadow-[0_0_30px_rgba(56,189,248,0.3)]" 
        />
      </motion.div>
    </motion.div>
  );
}
