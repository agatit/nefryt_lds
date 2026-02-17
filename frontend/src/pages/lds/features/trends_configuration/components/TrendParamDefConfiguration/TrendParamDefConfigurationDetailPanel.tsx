import React from "react";
import { useTranslation } from "react-i18next";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { TrendParamDef } from "../../../../../../services/api";

export interface TrendParamDefConfigurationDetailPanelProps {
  selected: TrendParamDef | null;
}

const TrendParamDefConfigurationDetailPanel = React.memo(
  function TrendParamDefConfigurationDetailPanel({
    selected,
  }: TrendParamDefConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrendParamDef: TrendParamDef) => {
        setTrendParamDefName(selectedTrendParamDef.Name ?? "");
      },
      []
    );

    const [trendParamDefID, setTrendParamDefID] = React.useState<
      string | undefined
    >(selected?.ID ?? "");
    const [trendParamTrendDefID, setTrendParamTrendDefID] = React.useState<
      string | undefined
    >(selected?.TrendDefID ?? "");
    const [trendParamDefName, setTrendParamDefName] = React.useState<
      string | undefined
    >(selected?.Name ?? "");
    const [trendParamDefDataType, setTrendParamDefDataType] = React.useState<
      string | undefined
    >(selected?.DataType ?? "");

    React.useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    const handleTrendParamDefIDChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendParamDefID(event.value.toString());
      },
      []
    );

    const handleTrendParamDefTrendDefIDChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendParamTrendDefID(event.value.toString());
      },
      []
    );

    const handleTrendParamDefNameChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendParamDefName(event.value.toString());
      },
      []
    );

    const handleTrendParamDefDataTypeChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendParamDefDataType(event.value.toString());
      },
      []
    );

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="trendParamDefID">{t("config-page:id")}</Label>
              <TextBox
                id="trendParamDefID"
                value={trendParamDefID}
                onChange={handleTrendParamDefIDChange}
                disabled={true}
              />
            </div>
            <div>
              <Label editorId="trendParamDefTrendDefID">
                {t("config-page:trend_type")}
              </Label>
              <TextBox
                id="trendParamDefTrendDefID"
                value={trendParamTrendDefID}
                onChange={handleTrendParamDefTrendDefIDChange}
                disabled={true}
              />
            </div>
            <div>
              <Label editorId="trendParamDefName">
                {t("config-page:name")}
              </Label>
              <TextBox
                id="trendParamDefName"
                value={trendParamDefName}
                onChange={handleTrendParamDefNameChange}
                disabled={true}
              />
            </div>
            <div>
              <Label editorId="trendParamDefDataType">
                {t("config-page:data_type")}
              </Label>
              <TextBox
                id="trendParamDefDataType"
                value={trendParamDefDataType}
                onChange={handleTrendParamDefDataTypeChange}
                disabled={true}
              />
            </div>
          </div>
        </div>
        <div className="separator" />
      </div>
    );
  }
);

export default TrendParamDefConfigurationDetailPanel;
