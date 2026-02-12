import React from "react";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import {
  PipelineParam,
  PipelineParamCreate,
} from "../../../../../../services/api";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon } from "@progress/kendo-svg-icons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";

interface Props {
  params: PipelineParam[];
  selected: PipelineParam | null;
  onSelect: (value: PipelineParam) => void;
  openDialog: () => void;
  closeDialog: () => void;
  showDialog: boolean;
  pipelineID: number;
  addPipelineParam: (
    value: PipelineParamCreate,
    pipelineID: number,
  ) => Promise<any>;
}

const PipelineParams = React.memo(function PipelineParamGrid({
  params,
  selected,
  onSelect,
  addPipelineParam,
  pipelineID,
}: Props) {
  const { t } = useTranslation(["pipeline-page", "common"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();
  const [showDialog, setShowDialog] = React.useState(false);
  const [pipelineParamDefID, setPipelineParamDefID] = React.useState("");
  const [value, setValue] = React.useState("");

  const handleSelectionChange = React.useCallback(
    (e: GridSelectionChangeEvent) => {
      const item = e.endDataItem as PipelineParam;
      onSelect(item);
      setSelect(e.select);
    },
    [onSelect],
  );

  const confirmAdd = async () => {
    if (!pipelineParamDefID.trim() || !value.trim()) return;

    await addPipelineParam(
      {
        PipelineParamDefID: pipelineParamDefID,
        Value: value,
      },
      pipelineID,
    );

    setPipelineParamDefID("");
    setValue("");
    setShowDialog(false);
  };

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <>
      <Grid
        data={params}
        dataItemKey="PipelineParamDefID"
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={() => setShowDialog(true)}>
              {t("pipeline-page:add_pipeline_param")}
            </Button>
          </ButtonGroup>
        </GridToolbar>

        <GridColumn field="Name" title="Name" />
        <GridColumn field="PipelineParamDefID" title="Param ID" />
        <GridColumn field="Value" title="Value" />
        <GridColumn field="DataType" title="Type" />
      </Grid>

      {showDialog && (
        <Dialog
          title="Add Pipeline Parameter"
          onClose={() => setShowDialog(false)}
        >
          <Label>Param ID</Label>
          <TextBox
            value={pipelineParamDefID}
            onChange={(e) =>
              setPipelineParamDefID(String(e.value ?? "").toUpperCase())
            }
          />

          <Label>Value</Label>
          <TextBox
            value={value}
            onChange={(e) => setValue(String(e.value ?? ""))}
          />

          <DialogActionsBar>
            <Button onClick={() => setShowDialog(false)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmAdd}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </>
  );
});
export default PipelineParams;
