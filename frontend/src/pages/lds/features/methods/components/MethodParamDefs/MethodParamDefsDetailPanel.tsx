import React from "react";
import { Typography } from "@progress/kendo-react-common";
import { useTranslation } from "react-i18next";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { MethodParamDef } from "../../../../../../services/api";

type Props = {
  selected: MethodParamDef | null;
};

const MethodParamDefDetailPanel = React.memo(
  function MethodParamDefDetailPanel({ selected }: Props) {
    const { t } = useTranslation(["common", "config-page"]);
    const [ParamDefID, setParamDefID] = React.useState<string | undefined>(
      selected?.ID ?? "",
    );

    const [ParamDefMethodDefID, setParamDefMethodDefID] = React.useState<
      string | undefined
    >(selected?.MethodDefID ?? "");

    const [ParamDefName, setMethodParamDefName] = React.useState<
      string | undefined
    >(selected?.Name ?? "");

    const [methodParamDefDataType, setParamDefDataType] = React.useState<
      string | undefined
    >(selected?.DataType ?? "");

    React.useEffect(() => {
      setParamDefID(selected?.ID ?? "");
      setParamDefMethodDefID(selected?.MethodDefID ?? "");
      setMethodParamDefName(selected?.Name ?? "");
      setParamDefDataType(selected?.DataType ?? "");
    }, [selected]);

    if (!selected) {
      return (
        <Typography.p style={{ padding: 20 }}>
          {t("common:no_selection")}
        </Typography.p>
      );
    }

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="ID">{t("config-page:id")}</Label>
              <TextBox value={ParamDefID} disabled />
            </div>

            <div>
              <Label editorId="Name">{t("config-page:name")}</Label>
              <TextBox value={ParamDefName} disabled />
            </div>

            <div>
              <Label editorId="DataType">{t("config-page:data_type")}</Label>
              <TextBox value={methodParamDefDataType} disabled />
            </div>

            <div>
              <Label editorId="MethodDefID">
                {t("config-page:method_def_id")}
              </Label>
              <TextBox value={ParamDefMethodDefID} disabled />
            </div>
          </div>
        </div>

        <div className="separator" />
      </div>
    );
  },
);

export default MethodParamDefDetailPanel;
