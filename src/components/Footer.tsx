import React from 'react';
import { Logo } from './Logo';

export function Footer() {
  return (
<footer className="relative z-10 border-t border-gray-200 dark:border-white/10 bg-white dark:bg-[#070b14] pt-20 pb-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start gap-12">
          <div>
            <Logo className="mb-4" />
            <p className="text-gray-600 dark:text-gray-400 max-w-sm text-sm">Empowering the next generation of sales professionals with transparent, high-yield network marketing infrastructure.</p>
          </div>
          <div className="flex gap-16">
            <div>
              <h4 className="text-gray-900 dark:text-white font-bold mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">How it works</a></li>
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">Compensation Plan</a></li>
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">Matrix Mechanics</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-gray-900 dark:text-white font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-gray-900 dark:text-white transition-colors">Privacy</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-16 pt-8 border-t border-gray-100 dark:border-white/5 text-center text-sm text-gray-600 dark:text-gray-400 dark:text-gray-600">
          © {new Date().getFullYear()} Global Sales Elite. All rights reserved.
        </div>
      </footer>
  );
}
