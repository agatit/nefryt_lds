import { useContext, useCallback, useState, memo, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { MethodDef } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { AppContext } from "../../../../../../contexts/appContext";

export interface Props {
  methodDefs: MethodDef[];
  selected: MethodDef | null;
  setSelected: (value: MethodDef | null) => void;
}

const MethodDefs = memo(function EventsDef({
  selected,
  setSelected,
  methodDefs,
}: Props) {
  const { t } = useTranslation(["methods-page"]);
  const appContext = useContext(AppContext);
  if (!appContext) return null;

  const [select, setSelect] = useState<SelectDescriptor>();

  const handleSelectionChange = useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: MethodDef = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  useEffect(() => {
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

        <GridColumn field="ID" title={t("methods-page:id")} />
        <GridColumn field="Name" title={t("methods-page:name")} />
      </Grid>
    </>
  );
});

export default MethodDefs;
