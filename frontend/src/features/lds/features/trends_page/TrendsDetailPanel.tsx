import { Button } from "@progress/kendo-react-buttons";
import { Typography } from "@progress/kendo-react-common";
import {
  DateTimePicker,
  DateTimePickerChangeEvent,
} from "@progress/kendo-react-dateinputs";
import { Loader } from "@progress/kendo-react-indicators";
import { Label } from "@progress/kendo-react-labels";
import {
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import {
  ItemRenderProps,
  processTreeViewItems,
  TreeView,
  TreeViewExpandChangeEvent,
  TreeViewOperationDescriptor,
} from "@progress/kendo-react-treeview";
import { DetailPanel } from "onyks_shared_kendo";
import React from "react";
import { useTranslation } from "react-i18next";
import { TreeViewDataItem } from "./TrendsPage";
import { pencilIcon, saveIcon } from "@progress/kendo-svg-icons";

export interface TrendDetailPanelProps {
  isLoadingTrends: boolean;
  axisTreeRef: React.RefObject<any>;
  axisTree: TreeViewDataItem[];
  TreeCustomItem: React.ComponentType<ItemRenderProps>;
  isChartInEdit: boolean;
  onChartEditButtonClick: React.MouseEventHandler<HTMLButtonElement>;
  startDate: Date;
  endDate: Date;
  onStartDateChange: (event: DateTimePickerChangeEvent) => void;
  onEndDateChange: (event: DateTimePickerChangeEvent) => void;
}

const TrendsDetailPanel = React.memo(function TrendsDetailPanel({
  isLoadingTrends,
  axisTreeRef,
  axisTree,
  TreeCustomItem,
  isChartInEdit,
  onChartEditButtonClick,
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
}: TrendDetailPanelProps) {
  const { t } = useTranslation(["common", "trends-page"]);

  const [tabSelected, setTabSelected] = React.useState<number>(0);

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    []
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

  return (
    <DetailPanel className="chart-detail-panel" flexGrow={1}>
      <TabStrip
        className="detail-panel-tabs"
        keepTabsMounted={true}
        selected={tabSelected}
        onSelect={handleTabSelect}
      >
        <TabStripTab title={t("trends-page:chart_config")}>
          {!isLoadingTrends ? (
            <div className="chart-config-content">
              <div className="item">
                <Typography.p fontSize="large" margin={0}>
                  {t("trends-page:legend")}
                </Typography.p>
                <div className="legend-container">
                  <TreeView
                    ref={axisTreeRef}
                    draggable={true}
                    data={processTreeViewItems(axisTree, {
                      expand: expandAxesTree,
                    })}
                    expandIcons={true}
                    onExpandChange={handleExpandAxesTreeChange}
                    item={TreeCustomItem}
                  />
                </div>
              </div>
              <div className="item">
                <Button
                  svgIcon={isChartInEdit ? undefined : pencilIcon}
                  onClick={onChartEditButtonClick}
                >
                  {isChartInEdit ? t("common:save") : t("common:edit")}
                </Button>
              </div>
              <div className="item">
                <Typography.p fontSize="large" margin={0}>
                  {t("trends-page:time_interval")}
                </Typography.p>
                <div className="item-row">
                  <div>
                    <Label>{t("common:from")}</Label>
                    <DateTimePicker
                      format={"dd/MM/yy HH:mm:ss"}
                      value={startDate}
                      onChange={onStartDateChange}
                    />
                  </div>
                  <div>
                    <Label>{t("common:to")}</Label>
                    <DateTimePicker
                      format={"dd/MM/yy HH:mm:ss"}
                      value={endDate}
                      onChange={onEndDateChange}
                    />
                  </div>
                </div>
              </div>
              <div className="item">
                <Button svgIcon={saveIcon}>
                  {t("trends-page:save_as_template")}
                </Button>
              </div>
            </div>
          ) : (
            <Loader size="medium" type={"infinite-spinner"} />
          )}
        </TabStripTab>
        <TabStripTab title={t("trends-page:templates")}></TabStripTab>
      </TabStrip>
    </DetailPanel>
  );
});

export default TrendsDetailPanel;
