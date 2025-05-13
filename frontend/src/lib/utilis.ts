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
