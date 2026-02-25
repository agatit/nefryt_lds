import { memo, useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { Method } from "../../../../../../services/api";

interface Props {
  methods: Method[];
  selected: Method | null;
  onSelect: (value: Method | null) => void;
  onAdd: () => void;
  requestDelete: (value: Method) => void;
}

const Methods = memo(function Methods({
  methods,
  selected,
  onSelect,
  onAdd,
  requestDelete,
}: Props) {
  const { t } = useTranslation(["common", "methods-page"]);
  const [select, setSelect] = useState<SelectDescriptor>({});

  const handleSelectionChange = useCallback(
    (e: GridSelectionChangeEvent) => {
      const item = e.endDataItem as Method;
      onSelect(item);
      setSelect(e.select);
    },
    [onSelect],
  );

  useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={methods}
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
          <Button svgIcon={plusIcon} onClick={onAdd}>
            {t("methods-page:add_new_method")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="PipelineID" title={t("methods-page:pipeline_id")} />
      <GridColumn field="MethodDefID" title={t("methods-page:method_def_id")} />
      <GridColumn field="Name" title={t("methods-page:name")} />
    </Grid>
  );
});

export default Methods;
