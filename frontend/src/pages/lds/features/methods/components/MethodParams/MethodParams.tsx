import { memo, useCallback, useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { MethodParam, Method } from "../../../../../../services/api";

type Props = {
  methodParams: MethodParam[];
  selectedMethod: Method | null;
  selectedParam: MethodParam | null;
  openDialog: () => void;
  setSelectedParam: (p: MethodParam | null) => void;
  requestDelete: (value: MethodParam) => void;
};

const MethodParams = memo(function MethodParams({
  selectedMethod,
  selectedParam,
  methodParams,
  setSelectedParam,
  openDialog,
  requestDelete,
}: Props) {
  if (!selectedMethod) return null;
  const [select, setSelect] = useState<SelectDescriptor>({});
  const { t } = useTranslation(["method-page"]);

  const handleSelectionChange = useCallback(
    (event: GridSelectionChangeEvent) => {
      const item = (event.endDataItem ?? event.dataItem) as MethodParam;

      if (!item) return;

      setSelect(event.select);
      setSelectedParam(item);
    },
    [setSelectedParam],
  );

  useEffect(() => {
    if (!selectedParam) {
      setSelect({});
    }
  }, [selectedParam]);

  return (
    <Grid
      data={methodParams}
      dataItemKey="MethodParamDefID"
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={openDialog}>
            {t("method-page:add_method_param")}
          </Button>

          {selectedParam && (
            <Button
              svgIcon={trashIcon}
              onClick={() => requestDelete(selectedParam)}
            >
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title="Name" />
      <GridColumn field="Value" title="Value" />
      <GridColumn field="DataType" title="DataType" />
      <GridColumn field="MethodParamDefID" title="MethodParamDefID" />
    </Grid>
  );
});

export default MethodParams;
