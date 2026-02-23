import { memo, useState, useCallback } from "react";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { PipelineParam } from "../../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";

interface Props {
  params: PipelineParam[];
  selected: PipelineParam | null;
  enterAddMode: () => void;
  requestDelete: (value: PipelineParam) => void;
  onSelect: (value: PipelineParam) => void;
}

const PipelineParams = memo(function PipelineParams({
  params,
  selected,
  enterAddMode,
  requestDelete,
  onSelect,
}: Props) {
  const { t } = useTranslation(["common", "pipeline-page"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  const handleSelectionChange = useCallback(
    (e: GridSelectionChangeEvent) => {
      const item = e.endDataItem as PipelineParam;
      onSelect(item);
      setSelect(e.select);
    },
    [onSelect],
  );

  return (
    <Grid
      data={params}
      dataItemKey="PipelineParamDefID"
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={enterAddMode}>
            {t("pipeline-page:add_pipeline_param")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title="Name" />
      <GridColumn field="PipelineParamDefID" title="Param ID" />
      <GridColumn field="Value" title="Value" />
      <GridColumn field="DataType" title="Type" />
    </Grid>
  );
});

export default PipelineParams;
