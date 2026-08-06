import React from 'react';
import { Check } from 'lucide-react';

const AVATARS = [
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Felix&backgroundColor=e2e8f0',
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Max&backgroundColor=e2e8f0',
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Jude&backgroundColor=e2e8f0',
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Aidan&backgroundColor=e2e8f0',
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Ryker&backgroundColor=e2e8f0',
  'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Rowan&backgroundColor=e2e8f0',
];

export function AvatarSelector({ value, onChange }: { value: string, onChange: (val: string) => void }) {
  return (
    <div className="flex flex-col gap-3">
      <label className="text-sm font-bold text-gray-700 dark:text-gray-300">Select Profile Avatar</label>
      <div className="flex flex-wrap gap-4">
        {AVATARS.map((url) => (
          <button
            key={url}
            type="button"
            onClick={() => onChange(url)}
            className={`relative w-16 h-16 rounded-full overflow-hidden border-4 transition-all ${
              value === url ? 'border-[#EF4444] scale-110 shadow-lg' : 'border-transparent hover:border-[#EF4444]/50 hover:scale-105'
            }`}
          >
            <img src={url} alt="Avatar option" className="w-full h-full object-cover" />
            {value === url && (
              <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                <Check className="text-white drop-shadow-md" size={24} />
              </div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}
