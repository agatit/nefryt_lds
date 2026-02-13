import React from "react";
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
import { plusIcon } from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";

interface Props {
  params: PipelineParam[];
  selected: PipelineParam | null;
  onSelect: (value: PipelineParam) => void;
  openDialog: () => void;
  pipelineID: number;
}

const PipelineParams = React.memo(function PipelineParamGrid({
  params,
  selected,
  onSelect,
  openDialog,
}: Props) {
  const { t } = useTranslation(["pipeline-page"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (e: GridSelectionChangeEvent) => {
      const item = e.endDataItem as PipelineParam;
      onSelect(item);
      setSelect(e.select);
    },
    [onSelect],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

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
          <Button svgIcon={plusIcon} onClick={openDialog}>
            {t("pipeline-page:add_pipeline_param")}
          </Button>
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
