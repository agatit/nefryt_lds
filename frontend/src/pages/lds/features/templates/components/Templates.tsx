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
import { Template } from "../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";
import { GridCellProps } from "@progress/kendo-react-grid";
import { Axis } from "../../../../../services/api";

interface TemplatesProps {
  templates: Template[];
  selected: Template | null;
  onSelectTemplate: (value: Template) => void;
  openAddDialog: () => void;
}

const Templates = React.memo(function TemplatesGrid({
  templates,
  selected,
  onSelectTemplate,
  openAddDialog,
}: TemplatesProps) {
  const { t } = useTranslation(["template-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item = event.endDataItem as Template;
      onSelectTemplate(item);
      setSelect(event.select);
    },
    [onSelectTemplate],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={templates}
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
            {t("template-page:add_new_template")}
          </Button>
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title="Name" />
      <GridColumn field="ID" title="ID" />
      <GridColumn
        field="Axes"
        title="Axes"
        cells={{
          data: (props: GridCellProps) => {
            const axes = props.dataItem.Axes;

            return (
              <td>
                {axes?.length ? axes.map((a: Axis) => a.Title).join(", ") : "-"}
              </td>
            );
          },
        }}
      />
    </Grid>
  );
});

export default Templates;
