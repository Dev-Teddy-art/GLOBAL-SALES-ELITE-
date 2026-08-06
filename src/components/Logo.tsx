import React from 'react';

export function Logo({ className = '' }: { className?: string }) {
  return (
    <div className={`flex items-center ${className || 'h-16 md:h-20'}`}>
      <img src="/GSE2.png" alt="Global Sales Elite Logo" className="h-full max-h-24 w-auto object-contain drop-shadow-md" />
    </div>
  );
}

