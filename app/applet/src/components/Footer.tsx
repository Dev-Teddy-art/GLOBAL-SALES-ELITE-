import React from 'react';

export function Footer() {
  return (
    <footer className="bg-white/80 dark:bg-[#0F172A]/80 backdrop-blur-md border-t border-gray-200 dark:border-white/10 py-6 mt-auto relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-gray-500 dark:text-gray-400 text-sm font-medium">
            &copy; {new Date().getFullYear()} Global Sales Elite. All rights reserved.
          </div>
          <div className="flex items-center gap-6 text-sm font-medium text-gray-500 dark:text-gray-400">
            <a href="#" className="hover:text-[#EF4444] transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-[#EF4444] transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-[#EF4444] transition-colors">Support</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
