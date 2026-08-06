import React, { useState, useEffect } from 'react';

const TARGET_DATE = new Date('2026-08-09T00:00:00');

export function Countdown() {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft().timeLeft);
  const [isExpired, setIsExpired] = useState(calculateTimeLeft().expired);

  function calculateTimeLeft() {
    const difference = +TARGET_DATE - +new Date();
    let timeLeft = {
      days: 0,
      hours: 0,
      minutes: 0,
      seconds: 0,
    };

    if (difference > 0) {
      timeLeft = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return { timeLeft, expired: difference <= 0 };
  }

  useEffect(() => {
    const timer = setInterval(() => {
      const { timeLeft: newTime, expired } = calculateTimeLeft();
      setTimeLeft(newTime);
      setIsExpired(expired);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  if (isExpired) {
    return (
      <div className="mb-8 py-4 px-6 bg-white/10 backdrop-blur-md rounded-lg border border-white/20 shadow-xl inline-block">
        <h3 className="text-white font-black text-xl md:text-2xl tracking-tight uppercase">
          "APP" is getting ready to be launched.
        </h3>
        <p className="text-white/90 text-md md:text-lg font-medium mt-1">
          Stay tuned.
        </p>
      </div>
    );
  }

  return (
    <div className="flex gap-3 md:gap-4 mb-8">
      {Object.entries(timeLeft).map(([unit, value]) => (
        <div key={unit} className="flex flex-col items-center">
          <div className="bg-white/10 backdrop-blur-md rounded-lg w-14 h-14 md:w-20 md:h-20 flex items-center justify-center border border-white/20 shadow-xl">
            <span className="text-white font-black text-xl md:text-3xl tracking-tighter">
              {value.toString().padStart(2, '0')}
            </span>
          </div>
          <span className="text-white/80 text-[10px] md:text-xs font-bold uppercase tracking-widest mt-2">
            {unit}
          </span>
        </div>
      ))}
    </div>
  );
}
