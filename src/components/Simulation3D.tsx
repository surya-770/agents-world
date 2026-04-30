import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Grid, Html, Environment, MeshReflectorMaterial } from '@react-three/drei';
import { motion, AnimatePresence } from 'motion/react';
import * as THREE from 'three';
import { EffectComposer, Bloom, Vignette, Noise } from '@react-three/postprocessing';

const ROOMS = {
  Cafeteria: { position: new THREE.Vector3(0, 0, 0), description: "Central hub for meetings and eating." },
  MedBay: { position: new THREE.Vector3(-6, 0, -4), description: "Medical scanning and healing facility." },
  Electrical: { position: new THREE.Vector3(-6, 0, 4), description: "Power distribution and wiring nodes." },
  Storage: { position: new THREE.Vector3(0, 0, 6), description: "Supply crates and fuel storage." },
  Navigation: { position: new THREE.Vector3(8, 0, 0), description: "Star map and course plotting controls." },
  Shields: { position: new THREE.Vector3(6, 0, 5), description: "Defense mechanism routing and priming." },
  O2: { position: new THREE.Vector3(6, 0, -4), description: "Oxygen generation and life support." },
  Reactor: { position: new THREE.Vector3(-10, 0, 0), description: "Main engine core and vessel power." },
};

const AGENTS_DATA = [
  { id: 'A1', color: '#3b82f6', isDead: false, start: 'Cafeteria' }, // Blue
  { id: 'A2', color: '#ef4444', isDead: false, start: 'MedBay' },    // Red
  { id: 'A3', color: '#64748b', isDead: true,  start: 'Electrical' },// Gray (Dead)
  { id: 'A4', color: '#a855f7', isDead: false, start: 'Storage' },   // Purple
  { id: 'A5', color: '#22c55e', isDead: false, start: 'Navigation' },// Green
  { id: 'A6', color: '#eab308', isDead: false, start: 'Shields' },   // Yellow
  { id: 'A7', color: '#f97316', isDead: false, start: 'O2' },        // Orange
  { id: 'A8', color: '#f8fafc', isDead: false, start: 'Reactor' },   // White
];

function Agent({ data }: { data: any }) {
  const group = useRef<THREE.Group>(null);
  const [target, setTarget] = useState(ROOMS[data.start as keyof typeof ROOMS].position.clone());
  const position = useRef(ROOMS[data.start as keyof typeof ROOMS].position.clone());
  const [isTasking, setIsTasking] = useState(false);
  const taskProgress = useRef(0);
  const [speech, setSpeech] = useState<string | null>(null);

  useFrame((state, delta) => {
    if (data.isDead) return;

    // Random speech popups
    if (!speech && Math.random() < 0.005) {
      const phrases = [
        "Where is everyone?",
        "Doing wires...",
        "I saw red near MedBay.",
        "Just swiping card.",
        "Wait, who is following me?",
        "Going to check reactor.",
        "Anyone in Electrical?"
      ];
      setSpeech(phrases[Math.floor(Math.random() * phrases.length)]);
      setTimeout(() => setSpeech(null), 3000);
    }

    if (isTasking) {
      taskProgress.current += delta * 0.5; // Complete task in 2 seconds
      
      // Wobble animation while doing task
      if (group.current) {
        group.current.rotation.z = Math.sin(state.clock.elapsedTime * 15) * 0.1;
      }

      if (taskProgress.current >= 1) {
        setIsTasking(false);
        taskProgress.current = 0;
        
        // Pick new room after task
        const roomKeys = Object.keys(ROOMS);
        const randomRoom = roomKeys[Math.floor(Math.random() * roomKeys.length)];
        setTarget(ROOMS[randomRoom as keyof typeof ROOMS].position.clone().add(new THREE.Vector3((Math.random() - 0.5) * 2, 0, (Math.random() - 0.5) * 2))); // Add slight offset so they don't stack directly
        if (group.current) group.current.rotation.z = 0;
      }
      return;
    }

    const distance = position.current.distanceTo(target);
    if (distance > 0.1) {
      const dir = target.clone().sub(position.current).normalize();
      position.current.add(dir.multiplyScalar(delta * 2.5)); // Move speed
      position.current.y = Math.abs(Math.sin(state.clock.elapsedTime * 10)) * 0.2; // Bounce
      
      if (group.current) {
        // Smooth rotation towards target
        const targetRotation = Math.atan2(target.x - position.current.x, target.z - position.current.z);
        const diff = targetRotation - group.current.rotation.y;
        const shortestDiff = ((diff + Math.PI) % (Math.PI * 2)) - Math.PI;
        group.current.rotation.y += shortestDiff * delta * 8;
      }
    } else {
      position.current.y = 0;
      // Reached destination, maybe start a task
      if (Math.random() < 0.2) {
        setIsTasking(true);
      } else if (Math.random() < 0.05) {
        const roomKeys = Object.keys(ROOMS);
        const randomRoom = roomKeys[Math.floor(Math.random() * roomKeys.length)];
        setTarget(ROOMS[randomRoom as keyof typeof ROOMS].position.clone().add(new THREE.Vector3((Math.random() - 0.5) * 2, 0, (Math.random() - 0.5) * 2)));
      }
    }

    if (group.current) {
      group.current.position.copy(position.current);
    }
  });

  return (
    <group ref={group} position={position.current}>
      {data.isDead ? (
        <group position={[0, 0.15, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <mesh>
            <capsuleGeometry args={[0.3, 0.5, 32, 32]} />
            <meshStandardMaterial color={data.color} roughness={0.4} metalness={0.2} />
          </mesh>
          <mesh position={[0, 0, 0.2]} rotation={[Math.PI / 2, 0, 0]} castShadow>
            {/* Visor */}
            <boxGeometry args={[0.4, 0.2, 0.3]} />
            <meshPhysicalMaterial color="#111" metalness={1} roughness={0} clearcoat={1} clearcoatRoughness={0.1} />
          </mesh>
          {/* Bone sticking out */}
          <mesh position={[0, 0.4, 0]}>
            <cylinderGeometry args={[0.08, 0.08, 0.3]} />
            <meshStandardMaterial color="#f8fafc" roughness={0.8} />
          </mesh>
        </group>
      ) : (
        <group position={[0, 0.4, 0]} castShadow>
          <mesh castShadow receiveShadow>
            <capsuleGeometry args={[0.3, 0.5, 32, 32]} />
            <meshStandardMaterial color={data.color} roughness={0.4} metalness={0.2} />
          </mesh>
          <mesh position={[0, 0.2, 0.25]} castShadow>
            {/* Visor */}
            <boxGeometry args={[0.45, 0.25, 0.2]} />
            <meshPhysicalMaterial color="#111" metalness={1} roughness={0} clearcoat={1} clearcoatRoughness={0.1} />
          </mesh>
          <mesh position={[0, -0.1, -0.3]} castShadow>
            {/* Backpack */}
            <boxGeometry args={[0.4, 0.45, 0.25]} />
            <meshStandardMaterial color={data.color} roughness={0.5} metalness={0.2} />
          </mesh>
        </group>
      )}
      
      {/* Shadow/Base */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
        <circleGeometry args={[0.4, 16]} />
        <meshBasicMaterial color="#000000" transparent opacity={0.3} />
      </mesh>
      
      {/* Name Label */}
      <Text
        position={[0, data.isDead ? 0.6 : 1.2, 0]}
        fontSize={0.25}
        color="white"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.03}
        outlineColor="#000000"
      >
        {data.id}
      </Text>

      {/* Speech Bubble */}
      <Html position={[0, data.isDead ? 1.0 : 1.8, 0]} center zIndexRange={[100, 0]}>
        <AnimatePresence>
          {speech && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5, y: 5 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.5, y: -5 }}
              transition={{ type: 'spring', stiffness: 400, damping: 20 }}
              className="bg-slate-800 text-white px-2.5 py-1 rounded shadow-[0_4px_12px_rgba(0,0,0,0.5)] border border-slate-600 whitespace-nowrap"
            >
              <span className="text-[10px] font-bold tracking-tight">{speech}</span>
              <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-slate-800 border-b border-r border-slate-600 rotate-45"></div>
            </motion.div>
          )}
        </AnimatePresence>
      </Html>

      {/* Task indicator */}
      {isTasking && !data.isDead && (
        <group position={[0, 1.6, 0]}>
          <mesh rotation={[0, 0, 0]}>
            <sphereGeometry args={[0.1, 8, 8]} />
            <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={2} toneMapped={false} />
          </mesh>
          <Text
            position={[0, 0.2, 0]}
            fontSize={0.15}
            color="#10b981"
            anchorX="center"
            anchorY="middle"
          >
            TASKING...
          </Text>
        </group>
      )}
    </group>
  );
}

function MapEnvironment() {
  const points = useMemo(() => {
    const p = [];
    for (let i = 0; i < 500; i++) {
       p.push(
         (Math.random() - 0.5) * 100,
         (Math.random() - 0.5) * 50 - 10,
         (Math.random() - 0.5) * 100
       );
    }
    return new Float32Array(p);
  }, []);

  return (
    <group>
      {/* Starfield */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" count={points.length / 3} array={points} itemSize={3} />
        </bufferGeometry>
        <pointsMaterial size={0.15} color="#ffffff" transparent opacity={0.8} />
      </points>

      {/* Main Floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.05, 0]} receiveShadow>
        <planeGeometry args={[60, 60]} />
        <MeshReflectorMaterial
          blur={[300, 100]}
          resolution={1024}
          mixBlur={1}
          mixStrength={80}
          roughness={0.7}
          depthScale={1.2}
          minDepthThreshold={0.4}
          maxDepthThreshold={1.4}
          color="#15171e"
          metalness={0.6}
          mirror={0.6}
        />
      </mesh>
      
      {/* Hex Grid Overlay */}
      <Grid infiniteGrid fadeDistance={40} sectionColor="#1e293b" cellColor="#0f172a" position={[0, 0, 0]} />

      {/* Ship layout boundary outline (abstract) */}
      <mesh position={[0, -0.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[42, 32]} />
        <meshBasicMaterial color="#3b82f6" transparent opacity={0.15} />
      </mesh>

      {/* Rooms Markers and Task Stations */}
      {Object.entries(ROOMS).map(([name, { position: pos, description }]) => (
        <group key={name} position={[pos.x, 0.02, pos.z]}>
          <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
            <planeGeometry args={[4.5, 4.5]} />
            <meshStandardMaterial color="#1e2430" roughness={0.9} />
          </mesh>
          
          {/* Room Borders */}
          <group position={[0, 0.25, 0]}>
            {[
              { pos: [0, 0, -2.25], args: [4.5, 0.5, 0.2] },
              { pos: [0, 0, 2.25], args: [4.5, 0.5, 0.2] },
              { pos: [-2.25, 0, -1.5], args: [0.2, 0.5, 1.5] },
              { pos: [-2.25, 0, 1.5], args: [0.2, 0.5, 1.5] },
              { pos: [2.25, 0, -1.5], args: [0.2, 0.5, 1.5] },
              { pos: [2.25, 0, 1.5], args: [0.2, 0.5, 1.5] },
            ].map((edge, i) => (
              <mesh key={i} position={edge.pos as [number, number, number]} castShadow receiveShadow>
                <boxGeometry args={edge.args as [number, number, number]} />
                <meshStandardMaterial color="#334155" metalness={0.6} roughness={0.4} />
              </mesh>
            ))}
          </group>

          <mesh rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[1.9, 2, 32]} />
            <meshBasicMaterial color="#3a82f6" transparent opacity={0.2} toneMapped={false} />
          </mesh>
          
          {/* Task Console Mockup */}
          <group position={[1.5, 0, 1.5]}>
            <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
              <boxGeometry args={[0.6, 0.5, 0.6]} />
              <meshStandardMaterial color="#1e293b" metalness={0.8} roughness={0.2} />
            </mesh>
            <mesh position={[0, 0.55, 0]} rotation={[-0.2, 0, 0]}>
              <planeGeometry args={[0.5, 0.3]} />
              <meshStandardMaterial color="#0ea5e9" emissive="#0ea5e9" emissiveIntensity={2} toneMapped={false} />
            </mesh>
          </group>

          {/* Emergency Button in Cafeteria only */}
          {name === 'Cafeteria' && (
            <group position={[0, 0, 0]}>
              <mesh position={[0, 0.2, 0]} castShadow receiveShadow>
                 <cylinderGeometry args={[0.4, 0.5, 0.4]} />
                 <meshStandardMaterial color="#1e293b" metalness={0.7} roughness={0.3} />
              </mesh>
              <mesh position={[0, 0.45, 0]} castShadow>
                 <cylinderGeometry args={[0.2, 0.3, 0.1]} />
                 <meshStandardMaterial color="#ef4444" emissive="#ef4444" emissiveIntensity={3} toneMapped={false} />
              </mesh>
            </group>
          )}

          <Text
            position={[0, 0.1, 0]}
            rotation={[-Math.PI / 2, 0, 0]}
            fontSize={0.4}
            color="#64748b"
            fontWeight="bold"
          >
            {name.toUpperCase()}
          </Text>
          <Text
            position={[0, 0.1, 0.4]}
            rotation={[-Math.PI / 2, 0, 0]}
            fontSize={0.15}
            color="#475569"
            maxWidth={3.5}
            textAlign="center"
          >
            {description}
          </Text>
        </group>
      ))}
    </group>
  );
}

export default function Simulation3D() {
  return (
    <Canvas shadows camera={{ position: [0, 15, 12], fov: 45 }} gl={{ antialias: false }}>
      <color attach="background" args={['#020408']} />
      <ambientLight intensity={0.2} />
      <directionalLight position={[10, 20, 5]} intensity={2} castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0001} />
      <pointLight position={[0, 8, 0]} intensity={3} color="#3b82f6" distance={30} decay={2} />
      
      <Environment preset="city" />
      
      <MapEnvironment />
      {AGENTS_DATA.map((agent) => (
        <Agent key={agent.id} data={agent} />
      ))}
      <OrbitControls 
        minDistance={5} 
        maxDistance={40} 
        maxPolarAngle={Math.PI / 2 - 0.05} // Prevent going below ground
        target={[0, 0, 0]}
      />
      <EffectComposer disableNormalPass>
        <Bloom luminanceThreshold={1} mipmapBlur intensity={1.2} />
        <Noise opacity={0.035} />
        <Vignette eskil={false} offset={0.1} darkness={1.1} />
      </EffectComposer>
    </Canvas>
  );
}
