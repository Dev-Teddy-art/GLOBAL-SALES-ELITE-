import React, { useState } from 'react';
import { Calculator } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export const CommissionCalculator: React.FC = () => {
  const { profile } = useAuth();
  const [saleAmount, setSaleAmount] = useState<number | ''>(5000000);
  const [tier, setTier] = useState<'direct' | 'level1' | 'level2' | 'level3'>('direct');

  const isAdmin = profile?.isAdmin || profile?.role === 'admin';

  const getCommissionRate = () => {
    switch (tier) {
      case 'direct':
        return 0.15; // 15% Personal Direct Sale
      case 'level1':
        return 0.15; // 15% Level 1 Referral Sale
      case 'level2':
        return 0.03; // 3% Level 2 Referral Sale
      case 'level3':
        return 0.04; // 4% Level 3 Referral Sale (Admin only)
      default:
        return 0.15;
    }
  };

  const currentAmount = typeof saleAmount === 'number' ? saleAmount : 0;
  const rate = getCommissionRate();
  const calculatedCommission = currentAmount * rate;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 text-white space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 bg-red-500/10 text-[#EF4444] rounded-2xl">
          <Calculator className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-xl font-black tracking-tight">Commission Calculator</h3>
          <p className="text-slate-400 text-sm font-medium">Calculate your payout for a single property sale</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider">
              Property Sale Amount (₦)
            </label>
            <input
              type="number"
              value={saleAmount}
              onChange={(e) => setSaleAmount(e.target.value === '' ? '' : Number(e.target.value))}
              placeholder="e.g. 5000000"
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white font-mono focus:outline-none focus:border-[#EF4444] transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider">
              Sale Type / Tier
            </label>
            <div className={`grid gap-2 ${isAdmin ? 'grid-cols-4' : 'grid-cols-3'}`}>
              <button
                type="button"
                onClick={() => setTier('direct')}
                className={`py-2.5 px-2 text-center rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  tier === 'direct'
                    ? 'bg-[#EF4444] text-white shadow-lg'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                Personal (15%)
              </button>
              <button
                type="button"
                onClick={() => setTier('level1')}
                className={`py-2.5 px-2 text-center rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  tier === 'level1'
                    ? 'bg-[#EF4444] text-white shadow-lg'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                Level 1 (15%)
              </button>
              <button
                type="button"
                onClick={() => setTier('level2')}
                className={`py-2.5 px-2 text-center rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  tier === 'level2'
                    ? 'bg-[#EF4444] text-white shadow-lg'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                Level 2 (3%)
              </button>
              {isAdmin && (
                <button
                  type="button"
                  onClick={() => setTier('level3')}
                  className={`py-2.5 px-2 text-center rounded-xl text-xs font-bold transition-all cursor-pointer ${
                    tier === 'level3'
                      ? 'bg-[#EF4444] text-white shadow-lg'
                      : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                  }`}
                >
                  Level 3 (4%)
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-6 text-center space-y-2">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-widest block">
            ESTIMATED EARNINGS
          </span>
          <div className="text-3xl lg:text-4xl font-black text-white font-mono tracking-tight">
            ₦{calculatedCommission.toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
          <p className="text-xs text-slate-400">
            Based on a {(rate * 100).toFixed(0)}% commission rate on a single sale of ₦{currentAmount.toLocaleString()}.
          </p>
        </div>
      </div>
    </div>
  );
};