import React from "react";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useTranslation } from "react-i18next";
import { Pipeline } from "../../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";

interface PipelinesProps {
  pipelines: Pipeline[];
  selected: Pipeline | null;
  onSelectPipeline: (value: Pipeline) => void;
  openAddDialog: () => void;
}

const Pipelines = React.memo(function Pipelines({
  pipelines,
  selected,
  onSelectPipeline,
  openAddDialog,
}: PipelinesProps) {
  const { t } = useTranslation(["pipeline-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (pipeline: GridSelectionChangeEvent) => {
      const item = pipeline.endDataItem as Pipeline;
      onSelectPipeline(item);
      setSelect(pipeline.select);
    },
    [onSelectPipeline],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={pipelines}
      dataItemKey="ID"
      autoProcessData
      sortable
      filterable
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={openAddDialog}>
            {t("pipeline-page:add_new_pipeline")}
          </Button>
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title={t("pipeline-page:name")} />
      <GridColumn field="ID" title="ID" />
    </Grid>
  );
});

export default Pipelines;
