import React, { useState, memo, useEffect } from "react";
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
import { Node } from "../../../../../../services/api";

interface NodesProps {
  nodes: Node[];
  selected: Node | null;
  onSelectNode: (value: Node) => void;
  onAdd: () => void;
  requestDelete: (value: Node) => void;
}

const Nodes = memo(function LinksGrid({
  nodes,
  selected,
  onSelectNode,
  onAdd,
  requestDelete,
}: NodesProps) {
  const { t } = useTranslation(["nodes-page", "common"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  useEffect(() => {
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
          <Button svgIcon={plusIcon} onClick={onAdd}>
            {t("nodes-page:add_new_node")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Type" title={t("nodes-page:type")} />
      <GridColumn field="Name" title={t("nodes-page:name")} />
      <GridColumn
        title={t("nodes-page:pos_x")}
        cells={{
          data: (props) => <td>{props.dataItem.EditorParams?.PosX ?? ""}</td>,
        }}
      />

      <GridColumn
        title={t("nodes-page:pos_y")}
        cells={{
          data: (props) => <td>{props.dataItem.EditorParams?.PosY ?? ""}</td>,
        }}
      />
    </Grid>
  );
});

export default Nodes;
