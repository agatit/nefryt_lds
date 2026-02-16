import React from "react";
import {
  Grid,
  GridColumn,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { MethodParamDef, MethodDef } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { LDSContext } from "../../../../contexts/ldsContext";

type Props = {
  selected: MethodParamDef | null;
  setSelected: (value: MethodParamDef | null) => void;
};

const MethodParamDefs = React.memo(function MethodParamDefs({
  selected,
  setSelected,
}: Props) {
  const lds = React.useContext(LDSContext);
  if (!lds) return null;

  const { methodParamDefs } = lds;

  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item = (event.endDataItem ?? event.dataItem) as MethodParamDef;

      if (!item) return;

      setSelect(event.select);
      setSelected(item);
    },
    [setSelected],
  );

  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={methodParamDefs.map((d) => ({
        ...d,
        uniqueKey: `${d.ID}_${d.MethodDefID}`,
      }))}
      sortable={true}
      selectable={{ enabled: true, mode: "single" }}
      dataItemKey="uniqueKey"
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridColumn field="Name" title="Name" />
      <GridColumn field="DataType" title="DataType" />
      <GridColumn field="ID" title="Param ID" />
    </Grid>
  );
});

export default MethodParamDefs;
