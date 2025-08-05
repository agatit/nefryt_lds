import { GridCellProps } from "@progress/kendo-react-grid";
import React from "react";

const ColorGridCell = React.memo(function ColorGridCell(props: GridCellProps) {
  return (
    <td>
      <div
        className="color-grid-cell-line"
        style={{
          backgroundColor: props.dataItem[props.field!],
          height: "4px",
          borderRadius: "2px",
        }}
      />
    </td>
  );
});

export default ColorGridCell;
