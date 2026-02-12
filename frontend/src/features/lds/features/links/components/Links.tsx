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
import { Link } from "../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";

interface LinksProps {
  links: Link[];
  selected: Link | null;
  onSelectLink: (value: Link) => void;
  openAddDialog: () => void;
}

const Links = React.memo(function LinksGrid({
  links,
  selected,
  onSelectLink,
  openAddDialog,
}: LinksProps) {
  const { t } = useTranslation(["link-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (link: GridSelectionChangeEvent) => {
      const item = link.endDataItem as Link;
      onSelectLink(item);
      setSelect(link.select);
    },
    [onSelectLink],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={links}
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
            {t("link-page:add_new_link")}
          </Button>
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="BeginNodeID" title={t("link-page:begin_node")} />
      <GridColumn field="EndNodeID" title={t("link-page:end_node")} />
      <GridColumn field="Length" title={t("link-page:length")} />
    </Grid>
  );
});

export default Links;
