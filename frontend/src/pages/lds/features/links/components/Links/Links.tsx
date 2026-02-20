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
import { Link } from "../../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";

interface LinksProps {
  links: Link[];
  selected: Link | null;
  onSelectLink: (value: Link) => void;
  openAddPanel: () => void;
  requestDelete: (value: Link) => void;
}

const Links = React.memo(function LinksGrid({
  links,
  selected,
  onSelectLink,
  openAddPanel,
  requestDelete,
}: LinksProps) {
  const { t } = useTranslation(["common", "links-page"]);
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
          <Button svgIcon={plusIcon} onClick={openAddPanel}>
            {t("links-page:add_new_link")}
          </Button>
          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="BeginNodeID" title={t("links-page:begin_node")} />
      <GridColumn field="EndNodeID" title={t("links-page:end_node")} />
      <GridColumn field="Length" title={t("links-page:length")} />
    </Grid>
  );
});

export default Links;
