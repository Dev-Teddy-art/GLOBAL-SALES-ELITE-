import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add Check to lucide-react imports
content = content.replace("Banknote } from 'lucide-react';", "Banknote, Check } from 'lucide-react';")

# Add SuccessAnimation component and motion/react import (motion is already imported, we might need AnimatePresence)
if 'AnimatePresence' not in content:
    content = content.replace("import { motion } from 'motion/react';", "import { motion, AnimatePresence } from 'motion/react';")

success_animation_code = """
const confettiParticles = Array.from({ length: 50 }).map((_, i) => ({
  id: i,
  color: ['bg-[#10B981]', 'bg-[#EF4444]', 'bg-blue-500', 'bg-yellow-400', 'bg-purple-500'][Math.floor(Math.random() * 5)],
  angle: Math.random() * Math.PI * 2,
  velocity: 15 + Math.random() * 30,
  size: 6 + Math.random() * 8
}));

function SuccessAnimation({ show, message }: { show: boolean, message?: string }) {
  return (
    <AnimatePresence>
      {show && (
        <div className="fixed inset-0 pointer-events-none z-[200] flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.5, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className="absolute bg-white dark:bg-[#1E293B] px-8 py-5 rounded-2xl shadow-2xl flex items-center gap-4 border border-[#10B981]/20 z-10"
          >
            <div className="bg-[#10B981] p-2 rounded-full text-white shadow-md">
              <Check size={24} />
            </div>
            <span className="font-bold text-lg text-gray-900 dark:text-white">{message || "Success!"}</span>
          </motion.div>
          {confettiParticles.map((p) => (
            <motion.div
              key={p.id}
              initial={{ opacity: 1, x: 0, y: 0, scale: 0 }}
              animate={{
                opacity: 0,
                x: Math.cos(p.angle) * p.velocity * 15,
                y: Math.sin(p.angle) * p.velocity * 15 + 150,
                scale: 1,
                rotate: Math.random() * 360
              }}
              transition={{ duration: 2, ease: "easeOut" }}
              className={`absolute rounded-sm shadow-sm ${p.color}`}
              style={{ width: p.size, height: p.size }}
            />
          ))}
        </div>
      )}
    </AnimatePresence>
  );
}

function SalesLogger() {"""

content = content.replace('function SalesLogger() {', success_animation_code)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)

