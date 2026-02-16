import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import React from "react";
import { MethodDef } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { AppContext } from "../../../../../../contexts/appContext";

export interface Props {
  methodDefs: MethodDef[];
  selected: MethodDef | null;
  setSelected: (value: MethodDef | null) => void;
}

const MethodDefs = React.memo(function EventsDef({
  selected,
  setSelected,
  methodDefs,
}: Props) {
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: MethodDef = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  return (
    <>
      <Grid
        data={methodDefs}
        dataItemKey="ID"
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
        </GridToolbar>

        <GridColumn field="ID" title="ID" />
        <GridColumn field="Name" title="Name" />
      </Grid>
    </>
  );
});

export default MethodDefs;
