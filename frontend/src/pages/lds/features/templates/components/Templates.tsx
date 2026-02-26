import { memo, useEffect, useState } from "react";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useTranslation } from "react-i18next";
import { Template, Axis } from "../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";

interface TemplatesProps {
  templates: Template[];
  selected: Template | null;
  onSelectTemplate: (value: Template | null) => void;
  openAddPanel: () => void;
  requestDelete: (value: Template) => void;
}

const Templates = memo(function TemplatesGrid({
  templates,
  selected,
  onSelectTemplate,
  openAddPanel,
  requestDelete,
}: TemplatesProps) {
  const { t } = useTranslation(["templates-page"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  const handleSelectionChange = (event: GridSelectionChangeEvent) => {
    const item = event.endDataItem as Template;
    onSelectTemplate(item);
    setSelect(event.select);
  };

  useEffect(() => {
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
          <Button svgIcon={plusIcon} onClick={openAddPanel}>
            {t("templates-page:add_new_template")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title={t("templates-page:add_new_template")} />
      <GridColumn
        field="Axes"
        title={t("templates-page:axes")}
        cells={{
          data: (props) => {
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
