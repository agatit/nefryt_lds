import { Button } from "@progress/kendo-react-buttons";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
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
  TreeViewItemClickEvent,
  TreeViewOperationDescriptor,
} from "@progress/kendo-react-treeview";
import { DetailPanel } from "onyks_shared_kendo";
import React from "react";
import { useTranslation } from "react-i18next";
import { AxisType, TreeViewDataItem } from "./TrendsPage";
import {
  cancelIcon,
  checkIcon,
  pencilIcon,
  saveIcon,
  xIcon,
} from "@progress/kendo-svg-icons";
import { Template, Trend } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { chartLegendIcon } from "../../components/chartLegendIcon";

export interface TrendDetailPanelProps {
  isLoadingTrends: boolean;
  trends: Trend[];
  axesState: AxisType[];
  onAxesStateChange: (value: AxisType[]) => void;
  onChartEditButtonClick: React.MouseEventHandler<HTMLButtonElement>;
  startDate: Date;
  endDate: Date;
  onStartDateChange: (event: DateTimePickerChangeEvent) => void;
  onEndDateChange: (event: DateTimePickerChangeEvent) => void;
  templates: Template[];
  onSelectedTemplateChange: (value: Template) => void;
  handleCreateNewTemplate: (name: string) => void;
  onHighlightedTrendIDChange: (value: number | null) => void;
}

const TrendsDetailPanel = React.memo(function TrendsDetailPanel({
  isLoadingTrends,
  trends,
  axesState,
  onAxesStateChange,
  onChartEditButtonClick,
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  templates,
  onSelectedTemplateChange,
  handleCreateNewTemplate,
  onHighlightedTrendIDChange,
}: TrendDetailPanelProps) {
  const { t } = useTranslation(["common", "trends-page"]);

  const [tabSelected, setTabSelected] = React.useState<number>(0);

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    []
  );

  // chart
  const axisTreeRef = React.useRef<any>(null);

  const axisTree: TreeViewDataItem[] = React.useMemo(() => {
    return axesState.map((axis) => {
      return {
        text: axis.Name,
        items: axis.TrendIDs.map((id) => {
          const trend = trends.find((trend) => trend.ID == id);
          return {
            id: id,
            text: trend!.Name!,
          };
        }),
      };
    });
  }, [axesState, trends]);
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

  const removeFromAxes = React.useCallback(
    (props: ItemRenderProps) => {
      const indexArray = props.itemHierarchicalIndex.split("_");

      if (indexArray.length == 1) {
        onAxesStateChange(
          axesState.filter((axis) => axis.Name !== props.item.text)
        );
        return;
      }

      onAxesStateChange(
        axesState.map((axis, i) => {
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
    [axesState]
  );

  const handleTreeItemMouseEnter = React.useCallback((id: number) => {
    onHighlightedTrendIDChange(id);
  }, []);

  const handleTreeItemMouseLeave = React.useCallback(() => {
    onHighlightedTrendIDChange(null);
  }, []);

  const TreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      const trend = trends.find((trend) => trend.ID == props.item.id);
      const correctDepth = props.itemHierarchicalIndex.split("_").length > 1;

      return (
        <div
          className={correctDepth ? "change-cursor" : ""}
          onMouseEnter={
            correctDepth
              ? () => handleTreeItemMouseEnter(props.item.id)
              : () => {}
          }
          onMouseLeave={correctDepth ? handleTreeItemMouseLeave : () => {}}
        >
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
    [trends, removeFromAxes]
  );

  // templates
  const templateTree: TreeViewDataItem[] = React.useMemo(() => {
    return templates.map((template) => {
      return {
        text: template.Name,
        id: template.ID,
      };
    });
  }, [templates]);

  const [templateSelect, setTemplateSelect] = React.useState<string[]>([""]);
  const handleTemplateClick = React.useCallback(
    (event: TreeViewItemClickEvent) => {
      setTemplateSelect([event.itemHierarchicalIndex]);
      onSelectedTemplateChange(
        templates.find((template) => template.ID == event.item.id)!
      );
    },
    [templates]
  );

  const [showDialog, setShowDialog] = React.useState<boolean>(false);
  const [newTemplateName, setNewTemplateName] = React.useState<string>("");

  const handleNewTemplateNameChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      setNewTemplateName(event.value ? event.value.toString() : "");
    },
    []
  );

  const handleSaveTemplateButtonClick = React.useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      setShowDialog(true);
    },
    []
  );

  const handleCreateTemplateConfirm = React.useCallback(() => {
    setShowDialog(false);
    handleCreateNewTemplate(newTemplateName);
  }, [newTemplateName]);

  const closeDialog = React.useCallback(() => {
    setShowDialog(false);
  }, []);

  return (
    <DetailPanel className="chart-detail-panel" flexGrow={1} extandable={false}>
      <TabStrip
        className="detail-panel-tabs"
        keepTabsMounted={true}
        selected={tabSelected}
        onSelect={handleTabSelect}
      >
        <TabStripTab title={t("trends-page:chart_management")}>
          {!isLoadingTrends ? (
            <div className="detail-panel-content">
              <div className="item">
                {/* <Typography.p fontSize="large" margin={0}>
                  {t("trends-page:chart_legend")}
                </Typography.p> */}
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
              <div className="separator" />
              <div className="item">
                {/* <Typography.p fontSize="large" margin={0}>
                  {t("trends-page:time_interval")}
                </Typography.p> */}
                <div className="item-column">
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
              <div className="separator" />
              <div className="item">
                <div className="item-row">
                  <Button svgIcon={pencilIcon} onClick={onChartEditButtonClick}>
                    {t("common:edit")}
                  </Button>
                  <Button
                    svgIcon={saveIcon}
                    onClick={handleSaveTemplateButtonClick}
                  >
                    {t("trends-page:save_as_template")}
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <Loader size="medium" type={"infinite-spinner"} />
          )}
        </TabStripTab>
        <TabStripTab title={t("trends-page:templates")}>
          <TreeView
            data={processTreeViewItems(templateTree, {
              select: templateSelect,
            })}
            onItemClick={handleTemplateClick}
            className="detail-panel-content"
          />
        </TabStripTab>
      </TabStrip>
      {showDialog && (
        <Dialog
          title={t("trends-page:enter_template_name")}
          onClose={closeDialog}
        >
          <TextBox
            value={newTemplateName}
            onChange={handleNewTemplateNameChange}
          />
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={closeDialog}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              onClick={handleCreateTemplateConfirm}
              themeColor={"primary"}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </DetailPanel>
  );
});

export default TrendsDetailPanel;
