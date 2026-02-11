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
import { Node } from "../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";

interface NodesProps {
  nodes: Node[];
  selected: Node | null;
  onSelectNode: (value: Node) => void;
  openAddDialog: () => void;
}

const Nodes = React.memo(function LinksGrid({
  nodes,
  selected,
  onSelectNode,
  openAddDialog,
}: NodesProps) {
  const { t } = useTranslation(["node-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  const handleSelectionChange = React.useCallback(
    (node: GridSelectionChangeEvent) => {
      const item = node.endDataItem as Node;
      onSelectNode(item);
      setSelect(node.select);
    },
    [onSelectNode],
  );

  return (
    <Grid
      data={nodes}
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
            {t("link-page:add_new_node")}
          </Button>
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Type" title={t("node-page:type")} />
      <GridColumn field="Name" title={t("node-page:name")} />
      <GridColumn field="EditorParams" title={t("node-page:EditorParams")} />
      <GridColumn field="TrendID" title={t("node-page:TrendID")} />
      <GridColumn field="ID" title={t("node-page:ID")} />
    </Grid>
  );
});

export default Nodes;
