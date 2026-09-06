// TRUE POSITIVE: a useEffect subscription with no cleanup.
//
// The resize listener and the interval are registered on mount but never
// removed: useEffect returns nothing. Each mount (repeated navigation, a list
// row remounting) leaks another listener and timer. Confirm with a heap
// snapshot / retained-listener count across repeated mount/unmount — reading the
// code only makes it a Candidate.
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

    // Timer keeps firing after the component unmounts.
    setInterval(() => onResize({ w: window.innerWidth, h: window.innerHeight }), 5000);

    // No return: the listener and interval are never cleaned up.
  }, [onResize]);

  return size;
}
