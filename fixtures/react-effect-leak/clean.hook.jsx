// FALSE POSITIVE: the same listener and interval, correctly cleaned up.
//
// useEffect returns a cleanup that removes the listener and clears the interval,
// so nothing leaks across mount/unmount. A naive "addEventListener / setInterval
// inside useEffect" heuristic would flag this; it is correct code and must not be
// flagged.
import { useEffect, useState } from 'react';

export function useViewportPoll(onResize) {
  const [size, setSize] = useState({ w: window.innerWidth, h: window.innerHeight });

  useEffect(() => {
    const handler = () => {
      const next = { w: window.innerWidth, h: window.innerHeight };
      setSize(next);
      onResize(next);
    };
    window.addEventListener('resize', handler);
    const timer = setInterval(
      () => onResize({ w: window.innerWidth, h: window.innerHeight }),
      5000,
    );

    // Cleanup runs on unmount (and before re-running the effect).
    return () => {
      window.removeEventListener('resize', handler);
      clearInterval(timer);
    };
  }, [onResize]);

  return size;
}
