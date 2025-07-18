import { Button } from "@progress/kendo-react-buttons";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
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
import {
  AxisType,
  MockupTrendGroupType,
  MockupTrendType,
  TreeViewDataItem,
} from "./TrendsPage";
import { Trend, TrendDefBase } from "../../../../services/api";
import {
  cancelIcon,
  checkIcon,
  plusIcon,
  xIcon,
} from "@progress/kendo-svg-icons";
import { chartLegendIcon } from "../../components/chartLegendIcon";

export interface ChartEditDialogProps {
  useMockup: boolean;
  closeDialog: () => void;
  trendDefs: TrendDefBase[];
  trendGroups: MockupTrendGroupType[];
  mockupTrendTreeData: TreeViewDataItem[];
  trendsState: Trend[] | MockupTrendType[];
  axesState: AxisType[];
  onAxesStateChange: (value: AxisType[]) => void;
  onShowCursorBubbleChange: (value: boolean) => void;
  onCursorBubbleTextChange: (value: string) => void;
}

const ChartEditDialog = React.memo(function ChartEditDialog({
  useMockup,
  closeDialog,
  trendDefs,
  trendGroups,
  mockupTrendTreeData,
  trendsState,
  axesState,
  onAxesStateChange,
  onShowCursorBubbleChange,
  onCursorBubbleTextChange,
}: ChartEditDialogProps) {
  const { t } = useTranslation(["common", "trends-page"]);

  const [newAxesState, setNewAxesState] = React.useState(axesState);

  const trendsTree: TreeViewDataItem[] = React.useMemo(() => {
    if (useMockup) return mockupTrendTreeData;

    const trendsTree: TreeViewDataItem[] = trendGroups.map((item) => {
      return {
        id: item.ID,
        text: item.Name,
        items: [],
      };
    });

    for (let trend of trendsState) {
      const index = trendsTree.findIndex(
        (item) => item.id == trend.TrendGroupID
      );
      const trendDef = trendDefs.find((item) => item.ID == trend.TrendDefID);

      const indexTrendDef = trendsTree[index].items?.findIndex(
        (item) => item.id == trend.TrendDefID
      );

      if (indexTrendDef == -1) {
        trendsTree[index].items?.push({
          id: trend.TrendDefID,
          text: trendDef?.Name!,
          items: [
            {
              id: trend.ID,
              text: trend.Name!,
            },
          ],
        });

        continue;
      }

      trendsTree[index].items![indexTrendDef!].items?.push({
        id: trend.ID,
        text: trend.Name!,
      });
    }

    return trendsTree;
  }, [trendsState, trendDefs, trendGroups]);

  const axisTreeRef = React.useRef<any>(null);

  const axisTree: TreeViewDataItem[] = React.useMemo(() => {
    return newAxesState.map((axis) => {
      return {
        text: axis.Name,
        items: axis.TrendIDs.map((id) => {
          const trend = trendsState.find((trend) => trend.ID == id);
          return {
            id: id,
            text: trend!.Name!,
          };
        }),
      };
    });
  }, [newAxesState, trendsState]);

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
    setNewAxesState([
      ...newAxesState,
      {
        Name: newAxisName,
        Unit: unit,
        TrendIDs: [draggedTrend.current?.ID!],
        ScaleMax: 0,
        ScaleMin: 0,
      },
    ]);
    setShowCreateAxisDialog(false);
  }, [trendsState, newAxesState, newAxisName]);

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
          newAxesState[
            parseInt(
              eventAnalyzer.destinationMeta.itemHierarchicalIndex.split("_")[0]
            )
          ].Name
      );
    },
    [newAxesState]
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

      setNewAxesState(
        newAxesState.map((axis: AxisType, i) => {
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
    [newAxesState]
  );

  const removeFromAxes = React.useCallback(
    (props: ItemRenderProps) => {
      const indexArray = props.itemHierarchicalIndex.split("_");

      if (indexArray.length == 1) {
        setNewAxesState(
          newAxesState.filter((axis) => axis.Name !== props.item.text)
        );
        return;
      }

      setNewAxesState(
        newAxesState.map((axis, i) => {
          if (i !== parseInt(indexArray[0])) return axis;
          return {
            ...axis,
            TrendIDs: axis.TrendIDs.filter(
              (ids, index) => index !== parseInt(indexArray[1])
            ),
          };
        })
      );
    },
    [newAxesState]
  );

  const TrendsTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      const trend = trendsState.find((trend) => trend.ID == props.item.id);
      const correctDepth = props.itemHierarchicalIndex.split("_").length > 2;

      return (
        <div className={correctDepth ? "change-cursor grabable" : ""}>
          {trend && correctDepth && (
            <SvgIcon
              icon={chartLegendIcon}
              size="xlarge"
              style={{ stroke: (trend as any).Color }}
            />
          )}
          {correctDepth ? (
            <span>{props.item.text}</span>
          ) : (
            <span style={{ fontWeight: "bold" }}>{props.item.text}</span>
          )}
        </div>
      );
    },
    [trendsState]
  );

  const AxisTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      const trend = trendsState.find((trend) => trend.ID == props.item.id);
      const correctDepth = props.itemHierarchicalIndex.split("_").length > 1;

      return (
        <div>
          {trend && correctDepth && (
            <SvgIcon
              icon={chartLegendIcon}
              size="xlarge"
              style={{ stroke: (trend as any).Color }}
            />
          )}
          {correctDepth ? (
            <span>{props.item.text}</span>
          ) : (
            <span style={{ fontWeight: "bold" }}>{props.item.text}</span>
          )}
          <Button
            svgIcon={xIcon}
            onClick={() => removeFromAxes(props)}
            fillMode="flat"
          />
        </div>
      );
    },
    [trendsState]
  );

  const [showCreateAxisDialog, setShowCreateAxisDialog] =
    React.useState<boolean>(false);

  const toggleAxisDialog = React.useCallback(() => {
    setShowCreateAxisDialog(!showCreateAxisDialog);
  }, [showCreateAxisDialog]);

  const handleConfirmButtonClick = React.useCallback(() => {
    onAxesStateChange(newAxesState);
    closeDialog();
  }, [newAxesState]);

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
              className="axis-treeview"
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
              <SvgIcon icon={plusIcon} size="large" />
              <Typography.p
                style={{ marginBottom: 0 }}
                fontWeight="bold"
                fontSize="large"
              >
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
          <Button type="button" svgIcon={cancelIcon} onClick={closeDialog}>
            {t("common:cancel")}
          </Button>
          <Button
            type="button"
            svgIcon={checkIcon}
            onClick={handleConfirmButtonClick}
            themeColor={"primary"}
          >
            {t("common:save")}
          </Button>
        </DialogActionsBar>
      </Dialog>
    </React.Fragment>
  );
});

export default ChartEditDialog;
