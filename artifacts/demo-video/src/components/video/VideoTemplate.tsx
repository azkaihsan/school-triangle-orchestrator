import { motion, AnimatePresence } from 'framer-motion';
import { useVideoPlayer } from '@/lib/video';
import { Scene1 } from './video_scenes/Scene1';
import { Scene2 } from './video_scenes/Scene2';
import { Scene3 } from './video_scenes/Scene3';
import { Scene4 } from './video_scenes/Scene4';
import { Scene5 } from './video_scenes/Scene5';

const SCENE_DURATIONS = {
  concept: 4500,
  agents: 5000,
  endpoints: 4500,
  techstack: 4000,
  close: 5000,
};

const bgColors = [
  '#020617', // concept
  '#0f172a', // agents
  '#020617', // endpoints
  '#1e1b4b', // techstack
  '#000000', // close
];

export default function VideoTemplate() {
  const { currentScene } = useVideoPlayer({
    durations: SCENE_DURATIONS,
  });

  return (
    <motion.div
      className="w-full h-screen overflow-hidden relative"
      animate={{ backgroundColor: bgColors[currentScene] }}
      transition={{ duration: 1.5, ease: 'easeInOut' }}
    >
      {/* Persistent background layers */}
      <div className="absolute inset-0 z-0">
        <video 
          src={`${import.meta.env.BASE_URL}videos/bg-network.mp4`}
          className="absolute inset-0 w-full h-full object-cover opacity-20 mix-blend-screen"
          autoPlay muted loop playsInline
        />
        <div className="absolute inset-0 bg-black/40" />
      </div>

      <motion.div 
        className="absolute w-[800px] h-[800px] rounded-full opacity-10 blur-3xl"
        style={{ background: 'radial-gradient(circle, #38bdf8, transparent)' }}
        animate={{ 
          x: currentScene % 2 === 0 ? '-20%' : '50%', 
          y: currentScene % 2 === 0 ? '10%' : '-30%',
          scale: [1, 1.2, 0.8, 1][currentScene % 4]
        }}
        transition={{ duration: 8, ease: 'easeInOut' }}
      />

      <AnimatePresence mode="popLayout">
        {currentScene === 0 && <Scene1 key="concept" />}
        {currentScene === 1 && <Scene2 key="agents" />}
        {currentScene === 2 && <Scene3 key="endpoints" />}
        {currentScene === 3 && <Scene4 key="techstack" />}
        {currentScene === 4 && <Scene5 key="close" />}
      </AnimatePresence>
    </motion.div>
  );
}
