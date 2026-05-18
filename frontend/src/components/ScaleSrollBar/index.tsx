import React from "react";
import "./scaleScrollBar.scss";
import { throttle } from "../../lib/utilis";

type ScaleScrollBarValueType = {
  start: number;
  end: number;
};

enum Dragged {
  Scroll,
  Start,
  End,
}

export interface ScaleScrollBarChangeEvent {
  value: ScaleScrollBarValueType;
}

export interface ScaleScrollBarProps extends Omit<
  React.ComponentPropsWithoutRef<"div">,
  "onChange"
> {
  value: ScaleScrollBarValueType;
  min: number;
  max: number;
  vertical?: boolean;
  onChange?: (event: ScaleScrollBarChangeEvent) => void;
}

export default function ScaleScrollBar({
  value,
  min,
  max,
  vertical = false,
  onChange,
  ...divProps
}: ScaleScrollBarProps) {
  const range = React.useMemo(() => {
    return max - min;
  }, [max, min]);
  const [startPercentage, setStartPercentage] = React.useState<number>(
    ((value.start - min) / range) * 100,
  );
  const [endPercentage, setEndPercentage] = React.useState<number>(
    ((value.end - min) / range) * 100,
  );

  const valueRef = React.useRef<ScaleScrollBarValueType>(value);

  React.useEffect(() => {
    if (dragging !== null) return;
    setStartPercentage(((value.start - min) / range) * 100);
    setEndPercentage(((value.end - min) / range) * 100);
    valueRef.current = value;
  }, [min, max, value]);

  const [dragging, setIsDragging] = React.useState<Dragged | null>(null);
  const trackRef = React.useRef<HTMLDivElement>(null);
  const perPixelStep = React.useRef<number | null>(null);
  const startingPosition = React.useRef<{ x: number; y: number } | null>(null);
  const startingStartPercentage = React.useRef<number>(startPercentage);
  const startingEndPercentage = React.useRef<number>(endPercentage);
  const startingValue = React.useRef<ScaleScrollBarValueType>(value);
  const edgeControlTop = React.useRef<number>(0);
  const edgeControlBot = React.useRef<number>(0);

  React.useEffect(() => {
    if (trackRef.current)
      perPixelStep.current = vertical
        ? range / trackRef.current.getBoundingClientRect().height
        : range / trackRef.current.getBoundingClientRect().width;
  });

  function handleMouseDown(
    event: React.MouseEvent<HTMLSpanElement, MouseEvent>,
    clickedOn: Dragged,
  ) {
    setIsDragging(clickedOn);
    // document.addEventListener("mousemove", handleMouseMove);
    startingPosition.current = { x: event.clientX, y: event.clientY };
    startingStartPercentage.current = startPercentage;
    startingEndPercentage.current = endPercentage;
    startingValue.current = valueRef.current;
  }

  React.useEffect(() => {
    function handleMouseUp(this: Document, event: MouseEvent) {
      setIsDragging(null);
    }

    function handleMouseMove(event: MouseEvent) {
      if (dragging == null) return;

      const pixelShift = vertical
        ? startingPosition.current!.y - event.clientY
        : startingPosition.current!.x - event.clientX;
      const shift = pixelShift * perPixelStep.current!;

      let newStartPercentage = vertical
        ? ((startingValue.current.start + shift - min) / range) * 100
        : startingStartPercentage.current - ((shift - min) / range) * 100;
      let newEndPercentage = vertical
        ? ((startingValue.current.end + shift - min) / range) * 100
        : startingEndPercentage.current - ((shift - min) / range) * 100;

      let newStartValue = startingValue.current.start + shift;
      let newEndValue = startingValue.current.end + shift;

      if (newStartPercentage < 0) {
        newStartPercentage = 0;
        newStartValue = min;
        edgeControlBot.current++;
      } else edgeControlBot.current = 0;
      if (newStartPercentage >= startingEndPercentage.current) {
        newStartPercentage = startingEndPercentage.current;
        newStartValue = startingValue.current.start;
      }

      if (newEndPercentage > 100) {
        newEndPercentage = 100;
        newEndValue = max;
        edgeControlTop.current++;
      } else edgeControlTop.current = 0;
      if (newEndPercentage <= startingStartPercentage.current) {
        newEndPercentage = startingStartPercentage.current;
        newEndValue = startingValue.current.end;
      }

      switch (dragging!) {
        case Dragged.Start:
          if (edgeControlBot.current > 1) return;

          setStartPercentage(newStartPercentage);
          if (onChange)
            onChange({
              value: {
                start: newStartValue,
                end: startingValue.current.end,
              },
            });
          valueRef.current = {
            start: newStartValue,
            end: startingValue.current.end,
          };

          break;
        case Dragged.End:
          if (edgeControlTop.current > 1) return;

          setEndPercentage(newEndPercentage);
          if (onChange)
            onChange({
              value: {
                start: startingValue.current.start,
                end: newEndValue,
              },
            });
          valueRef.current = {
            start: startingValue.current.start,
            end: newEndValue,
          };

          break;
        case Dragged.Scroll:
          if (edgeControlBot.current > 1 || edgeControlTop.current > 1) return;

          setStartPercentage(newStartPercentage);
          setEndPercentage(newEndPercentage);
          if (onChange)
            onChange({
              value: {
                start: newStartValue,
                end: newEndValue,
              },
            });
          valueRef.current = {
            start: newStartValue,
            end: newEndValue,
          };

          break;
      }
    }

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragging]);

  return (
    <div
      {...divProps}
      className={`scale-scroll-bar ${divProps.className || ""} ${
        vertical ? "vertical" : "horizontal"
      }`}
      style={{
        ...divProps.style,
      }}
      onDragStart={(e) => {
        e.preventDefault();
      }}
    >
      <div
        className={`container ${vertical ? "vertical" : "horizontal"}`}
        onDragStart={(e) => {
          e.preventDefault();
        }}
      >
        <div
          className={`slider-track ${vertical ? "vertical" : "horizontal"}`}
          ref={trackRef}
          onDragStart={(e) => {
            e.preventDefault();
          }}
        >
          <div
            className={`slider-selection ${
              vertical ? "vertical" : "horizontal"
            }`}
            style={
              vertical
                ? {
                    bottom: `${startPercentage}%`,
                    height: `${endPercentage - startPercentage}%`,
                  }
                : {
                    left: `${startPercentage}%`,
                    width: `${endPercentage - startPercentage}%`,
                  }
            }
            onMouseDown={(e) => handleMouseDown(e, Dragged.Scroll)}
            onDragStart={(e) => {
              e.preventDefault();
            }}
          />
          <span
            className={`draghandle ${vertical ? "vertical" : "horizontal"}`}
            style={
              vertical
                ? {
                    bottom: `${startPercentage}%`,
                  }
                : {
                    left: `${startPercentage}%`,
                  }
            }
            onMouseDown={(e) => handleMouseDown(e, Dragged.Start)}
            onDragStart={(e) => {
              e.preventDefault();
            }}
          />
          <span
            className={`draghandle ${vertical ? "vertical" : "horizontal"}`}
            style={
              vertical
                ? {
                    bottom: `${endPercentage}%`,
                  }
                : {
                    left: `${endPercentage}%`,
                  }
            }
            onMouseDown={(e) => handleMouseDown(e, Dragged.End)}
            onDragStart={(e) => {
              e.preventDefault();
            }}
          />
        </div>
      </div>
    </div>
  );
}
