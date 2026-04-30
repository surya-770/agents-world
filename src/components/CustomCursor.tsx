import { useState, useEffect } from 'react';
import { motion } from 'motion/react';

export default function CustomCursor() {
  const [mousePos, setMousePos] = useState({ x: -100, y: -100 });
  const [isHovering, setIsHovering] = useState(false);
  const [isClicking, setIsClicking] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY });
      if (!isVisible) setIsVisible(true);
    };

    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      // Detect interactable elements
      const isClickable = target.closest('button') || target.closest('a') || target.tagName === 'INPUT' || window.getComputedStyle(target).cursor === 'pointer';
      setIsHovering(!!isClickable);
    };

    const handleMouseDown = () => setIsClicking(true);
    const handleMouseUp = () => setIsClicking(false);
    const handleMouseLeave = () => setIsVisible(false);

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseover', handleMouseOver);
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseover', handleMouseOver);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <>
      {/* Outer target ring */}
      <motion.div
        className="fixed top-0 left-0 w-8 h-8 rounded-full border border-blue-400 pointer-events-none z-[99999]"
        animate={{
          x: mousePos.x - 16,
          y: mousePos.y - 16,
          scale: isClicking ? 0.7 : isHovering ? 1.5 : 1,
          opacity: isHovering ? 0.3 : 0.8,
          rotate: isHovering ? 45 : 0,
        }}
        transition={{ type: 'spring', stiffness: 350, damping: 25, mass: 0.5 }}
      >
        {/* Sci-fi crosshair tick marks */}
        <div className="absolute -top-1 left-1/2 w-0.5 h-2 bg-blue-500 -translate-x-1/2"></div>
        <div className="absolute -bottom-1 left-1/2 w-0.5 h-2 bg-blue-500 -translate-x-1/2"></div>
        <div className="absolute top-1/2 -left-1 w-2 h-0.5 bg-blue-500 -translate-y-1/2"></div>
        <div className="absolute top-1/2 -right-1 w-2 h-0.5 bg-blue-500 -translate-y-1/2"></div>
      </motion.div>
      
      {/* Inner precise dot */}
      <motion.div
        className="fixed top-0 left-0 w-1.5 h-1.5 rounded-full bg-cyan-300 pointer-events-none z-[100000] shadow-[0_0_10px_rgba(34,211,238,1)]"
        animate={{
          x: mousePos.x - 3,
          y: mousePos.y - 3,
          scale: isClicking ? 0.5 : isHovering ? 1.5 : 1,
        }}
        transition={{ type: 'spring', stiffness: 1000, damping: 28, mass: 0.1 }}
      />
    </>
  );
}
