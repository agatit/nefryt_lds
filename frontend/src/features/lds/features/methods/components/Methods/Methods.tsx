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
import { Method } from "../../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";

interface Props {
  methods: Method[];
  selected?: Method | null;
  onSelect: (m: Method) => void;
  openAddDialog: () => void;
}

const Methods = React.memo(function methods({
  methods,
  selected,
  onSelect,
  openAddDialog,
}: Props) {
  const { t } = useTranslation(["pipeline-page"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (method: GridSelectionChangeEvent) => {
      const item = method.endDataItem as Method;
      onSelect(item);
      setSelect(method.select);
    },
    [onSelect],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <div>
      <Grid
        data={methods}
        dataItemKey="ID"
        autoProcessData
        sortable
        filterable
        select={select}
        selectable={{ enabled: true, mode: "single" }}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              {t("pipeline-page:add_new_method")}
            </Button>
          </ButtonGroup>
        </GridToolbar>

        <GridColumn field="ID" title="ID" />
        <GridColumn field="PipelineID" title="PipelineID" />
        <GridColumn field="MethodDefID" title="Definition ID" />
        <GridColumn field="Name" title="Name" />
      </Grid>
    </div>
  );
});

export default Methods;
