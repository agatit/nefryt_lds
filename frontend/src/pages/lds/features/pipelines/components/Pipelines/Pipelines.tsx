import { memo, useState } from "react";
import {
  Grid,
  GridColumn,
  GridToolbar,
  GridSearchBox,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useTranslation } from "react-i18next";
import { Pipeline } from "../../../../../../services/api";

interface Props {
  pipelines: Pipeline[];
  selected: Pipeline | null;
  setSelected: (value: Pipeline | null) => void;
  enterAddNewPipeline: () => void;
  requestDelete: (value: Pipeline) => void;
}

const Pipelines = memo(function Pipelines({
  pipelines,
  selected,
  setSelected,
  enterAddNewPipeline,
  requestDelete,
}: Props) {
  const { t } = useTranslation(["common", "pipelines-page"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  const handleSelectionChange = (e: GridSelectionChangeEvent) => {
    setSelected(e.endDataItem);
    setSelect(e.select);
  };

  return (
    <Grid
      data={pipelines}
      dataItemKey="ID"
      autoProcessData
      sortable
      filterable
      selectable={{ mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />

        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={enterAddNewPipeline}>
            {t("pipelines-page:add_new_pipeline")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title={t("pipelines-page:name")} />
    </Grid>
  );
});

export default Pipelines;
