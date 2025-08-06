type AnyFn = (...args: any[]) => void;

export function throttle<F extends AnyFn>(fn: F, waitMs: number): F {
  let lastCallTime = 0;
  let timer: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: any[] | null = null;

  const throttled = function (this: any, ...args: any[]) {
    const now = Date.now();
    const elapsed = now - lastCallTime;
    lastArgs = args;

    if (elapsed >= waitMs) {
      lastCallTime = now;
      fn.apply(this, args);
    } else if (!timer) {
      timer = setTimeout(() => {
        lastCallTime = Date.now();
        timer = null;
        if (lastArgs) fn.apply(this, lastArgs);
        lastArgs = null;
      }, waitMs - elapsed);
    }
  };

  return throttled as F;
}

export function rgbaToHex(rgbaStr: string): string | null {
  const regex = /rgba?\s*\(\s*(\d+),\s*(\d+),\s*(\d+),?\s*([01]?\.?\d*)?\s*\)/i;
  const result = regex.exec(rgbaStr);
  if (!result) return null;

  const r = parseInt(result[1], 10);
  const g = parseInt(result[2], 10);
  const b = parseInt(result[3], 10);
  const a = result[4] !== undefined ? parseFloat(result[4]) : 1;

  const toHex = (n: number): string => n.toString(16).padStart(2, "0");

  return `#${toHex(r)}${toHex(g)}${toHex(b)}${toHex(Math.round(a * 255))}`;
}
