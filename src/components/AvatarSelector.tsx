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
      <label className="text-sm font-bold text-slate-200">Select Profile Avatar</label>
      <div className="flex flex-wrap gap-4">
        {AVATARS.map((url) => {
          const isSelected = value === url;
          return (
            <button
              key={url}
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onChange(url);
              }}
              className={`relative w-14 h-14 rounded-full overflow-hidden border-2 transition-all cursor-pointer ${
                isSelected ? 'border-[#EF4444] scale-105 shadow-md' : 'border-slate-700 hover:border-[#EF4444]/50'
              }`}
            >
              <img src={url} alt="Avatar option" className="w-full h-full object-cover pointer-events-none" />
              {isSelected && (
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center pointer-events-none">
                  <Check className="text-white drop-shadow-md" size={20} />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
