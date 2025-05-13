import React, { ComponentPropsWithoutRef } from "react";
import "../styles/components/cursorBubble.scss";
import { Typography } from "@progress/kendo-react-common";

export interface CursorBubbleProps extends ComponentPropsWithoutRef<"div"> {
  text: string;
}

export default function CursorBubble({ text, ...divProps }: CursorBubbleProps) {
  const [cursorPosition, setCursorPosition] = React.useState({ x: 0, y: 0 });

  function handleMouse(event: MouseEvent) {
    setCursorPosition({ x: event.clientX, y: event.clientY });
  }
  React.useEffect(() => {
    window.addEventListener("mousemove", handleMouse);

    return () => {
      window.removeEventListener("mousemove", handleMouse);
    };
  }, []);

  return (
    <div
      {...divProps}
      className={`cursor-bubble ${divProps.className || ""}`}
      style={{
        top: cursorPosition.y + 10,
        left: cursorPosition.x + 15,
        ...divProps.style,
      }}
    >
      <Typography.p margin={0}>{text}</Typography.p>
    </div>
  );
}
