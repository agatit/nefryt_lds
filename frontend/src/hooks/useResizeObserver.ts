import { useEffect, useRef } from "react";

export function useResizeObserver<T extends HTMLElement>(
  callback: (size: { width: number; height: number }) => void
) {
  const ref = useRef<T | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      callback({ width, height });
    });

    observer.observe(ref.current);

    return () => observer.disconnect();
  }, [callback]);

  return ref;
}
