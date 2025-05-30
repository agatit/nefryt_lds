import { Button } from "@progress/kendo-react-buttons";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  ItemRenderProps,
  processTreeViewItems,
  TreeView,
  TreeViewDragAnalyzer,
  TreeViewExpandChangeEvent,
  TreeViewItemDragEndEvent,
  TreeViewItemDragOverEvent,
  TreeViewItemDragStartEvent,
  TreeViewOperationDescriptor,
} from "@progress/kendo-react-treeview";
import React from "react";
import { useTranslation } from "react-i18next";
import { AxisType, MockupTrendType, TreeViewDataItem } from "./TrendsPage";
import { Trend } from "../../../../services/api";
import CursorBubble from "../../../../components/CursorBubble";

export interface ChartEditDialogProps {
  trendsTree: TreeViewDataItem[];
  TrendsTreeCustomItem: React.ComponentType<ItemRenderProps>;
  AxisTreeCustomItem: React.ComponentType<ItemRenderProps>;
  axisTreeRef: React.RefObject<any>;
  axisTree: TreeViewDataItem[];
  onCancelButtonClick: React.MouseEventHandler<HTMLButtonElement>;
  onSaveButtonClick: React.MouseEventHandler<HTMLButtonElement>;
  trendsState: Trend[] | MockupTrendType[];
  axesState: AxisType[];
  onAxesStateChange: (value: AxisType[]) => void;
  onShowCursorBubbleChange: (value: boolean) => void;
  onCursorBubbleTextChange: (value: string) => void;
}

const ChartEditDialog = React.memo(function ChartEditDialog({
  trendsTree,
  TrendsTreeCustomItem,
  AxisTreeCustomItem,
  axisTreeRef,
  axisTree,
  onCancelButtonClick,
  onSaveButtonClick,
  trendsState,
  axesState,
  onAxesStateChange,
  onShowCursorBubbleChange,
  onCursorBubbleTextChange,
}: ChartEditDialogProps) {
  const { t } = useTranslation(["common", "trends-page"]);

  const [expandTrendsTree, setExpandTrendsTree] =
    React.useState<TreeViewOperationDescriptor>({
      ids: [1, 2, 3, 4, 5, 6],
      idField: "id",
    });

  const handleExpandTrendsTreeChange = React.useCallback(
    (event: TreeViewExpandChangeEvent) => {
      const ids: string[] = expandTrendsTree.ids
        ? expandTrendsTree.ids.slice()
        : [];
      const index: number = ids.indexOf(event.item.id);

      index === -1 ? ids.push(event.item.id) : ids.splice(index, 1);
      setExpandTrendsTree({ ids, idField: "id" });
    },
    [expandTrendsTree]
  );

  const [expandAxesTree, setExpandAxesTree] =
    React.useState<TreeViewOperationDescriptor>({
      ids: ["Ciśnienie pomiary MPa"],
      idField: "text",
    });

  const handleExpandAxesTreeChange = React.useCallback(
    (event: TreeViewExpandChangeEvent) => {
      const ids: string[] = expandAxesTree.ids
        ? expandAxesTree.ids.slice()
        : [];
      const index: number = ids.indexOf(event.item.text);

      index === -1 ? ids.push(event.item.text) : ids.splice(index, 1);
      setExpandAxesTree({ ids, idField: "text" });
    },
    [expandAxesTree]
  );

  // DRAG STUFF

  const mouseOverCreateNewAxisArea = React.useRef<boolean>(false);

  const handleMouseEnterCreateNewAxisArea = React.useCallback(() => {
    mouseOverCreateNewAxisArea.current = true;
  }, []);
  const handleMouseLeaveCreateNewAxisArea = React.useCallback(() => {
    mouseOverCreateNewAxisArea.current = false;
  }, []);

  const [newAxisName, setNewAxisName] = React.useState<string>("");
  const draggedTrend = React.useRef<Trend | MockupTrendType>(null);

  const handleAxisNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    if (e.value) setNewAxisName(e.value.toString());
  }, []);

  const createNewAxis = React.useCallback(() => {
    const unit = (
      trendsState.find(
        (trend) => trend.ID == draggedTrend.current?.ID
      ) as MockupTrendType
    ).Unit;
    onAxesStateChange([
      ...axesState,
      {
        Name: newAxisName,
        Unit: unit,
        TrendIDs: [draggedTrend.current?.ID!],
        ScaleMax: 0,
        ScaleMin: 0,
      },
    ]);
    setShowCreateAxisDialog(false);
  }, [trendsState, axesState, newAxisName]);

  const handleTreeItemDragStart = React.useCallback(
    (e: TreeViewItemDragStartEvent) => {
      draggedTrend.current = trendsState.find(
        (trend) => trend.ID == e.item.id
      )!;
      onShowCursorBubbleChange(true);
    },
    []
  );

  const handleTreeItemDragOver = React.useCallback(
    (e: TreeViewItemDragOverEvent) => {
      if (mouseOverCreateNewAxisArea.current) {
        onCursorBubbleTextChange(t("trends-page:add_to_new_axis"));
        return;
      }

      const eventAnalyzer = new TreeViewDragAnalyzer(e).init();
      if (
        eventAnalyzer.destinationMeta.treeViewGuid.split("-")[0] !==
        axisTreeRef.current.props.id
      ) {
        onCursorBubbleTextChange(e.item.text);

        return;
      }

      onCursorBubbleTextChange(
        t("trends-page:add_to") +
          ": " +
          axesState[
            parseInt(
              eventAnalyzer.destinationMeta.itemHierarchicalIndex.split("_")[0]
            )
          ].Name
      );
    },
    []
  );

  const handleTreeItemDragEnd = React.useCallback(
    (e: TreeViewItemDragEndEvent) => {
      onShowCursorBubbleChange(false);

      if (mouseOverCreateNewAxisArea.current) {
        setShowCreateAxisDialog(true);
        setNewAxisName(
          (
            trendsState.find(
              (trend) => trend.ID == e.item.id
            )! as MockupTrendType
          ).Unit
        );

        return;
      }

      const eventAnalyzer = new TreeViewDragAnalyzer(e).init();
      if (
        eventAnalyzer.destinationMeta.treeViewGuid.split("-")[0] !==
        axisTreeRef.current.props.id
      )
        return;

      const indexArray =
        eventAnalyzer.destinationMeta.itemHierarchicalIndex.split("_");

      const axisIndex = parseInt(indexArray[0]);
      const trendIndex = parseInt(indexArray[1]);

      onAxesStateChange(
        axesState.map((axis: AxisType, i) => {
          if (i !== axisIndex) return axis;
          if (axis.TrendIDs.includes(e.item.id)) return axis;

          if (indexArray.length < 2)
            return {
              ...axis,
              TrendIDs: [...axis.TrendIDs, e.item.id],
            };

          const newArr = axis.TrendIDs;
          switch (eventAnalyzer.getDropOperation()) {
            case "before":
              newArr.splice(trendIndex, 0, e.item.id);
              return {
                ...axis,
                TrendIDs: newArr,
              };
              break;
            default:
              newArr.splice(trendIndex + 1, 0, e.item.id);
              return {
                ...axis,
                TrendIDs: newArr,
              };
          }
        })
      );
    },
    [axesState]
  );

  const [showCreateAxisDialog, setShowCreateAxisDialog] =
    React.useState<boolean>(false);

  const toggleAxisDialog = React.useCallback(() => {
    setShowCreateAxisDialog(!showCreateAxisDialog);
  }, [showCreateAxisDialog]);

  return (
    <React.Fragment>
      <Dialog>
        <div className="chart-edit-container">
          <div className="segregated-trends">
            <TreeView
              draggable={true}
              data={processTreeViewItems(trendsTree, {
                expand: expandTrendsTree,
              })}
              expandIcons={true}
              onItemDragStart={handleTreeItemDragStart}
              onItemDragOver={handleTreeItemDragOver}
              onItemDragEnd={handleTreeItemDragEnd}
              onExpandChange={handleExpandTrendsTreeChange}
              item={TrendsTreeCustomItem}
            />
          </div>
          <div className="separator" />
          <div className="selected-trends">
            <TreeView
              ref={axisTreeRef}
              draggable={true}
              data={processTreeViewItems(axisTree, {
                expand: expandAxesTree,
              })}
              expandIcons={true}
              onExpandChange={handleExpandAxesTreeChange}
              item={AxisTreeCustomItem}
            />
            <div
              className="create-axis-area"
              onMouseEnter={handleMouseEnterCreateNewAxisArea}
              onMouseLeave={handleMouseLeaveCreateNewAxisArea}
            >
              <Typography.p style={{ marginBottom: 0 }}>
                {t("trends-page:create_new_axis")}
              </Typography.p>
            </div>
          </div>
        </div>
        {showCreateAxisDialog && (
          <Dialog onClose={toggleAxisDialog}>
            <Label>{t("trends-page:new_axis_name")}</Label>
            <TextBox value={newAxisName} onChange={handleAxisNameChange} />
            <DialogActionsBar>
              <Button type="button" onClick={createNewAxis}>
                {t("common:confirm")}
              </Button>
            </DialogActionsBar>
          </Dialog>
        )}
        <DialogActionsBar>
          <Button type="button" onClick={onCancelButtonClick}>
            {t("common:cancel")}
          </Button>
          <Button type="button" onClick={onSaveButtonClick}>
            {t("common:save")}
          </Button>
        </DialogActionsBar>
      </Dialog>
    </React.Fragment>
  );
});

export default ChartEditDialog;
