import {
  memo,
  useEffect,
  useMemo,
  useState,
  useContext,
  useCallback,
} from "react";
import { useTranslation } from "react-i18next";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import {
  NumericTextBox,
  FlatColorPicker,
  TextBox,
} from "@progress/kendo-react-inputs";
import {
  cancelIcon,
  saveIcon,
  trashIcon,
  pencilIcon,
} from "@progress/kendo-svg-icons";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { TFunction } from "i18next";
import {
  Trend,
  TrendCreate,
  TrendUpdate,
  TrendDef,
  TrendGroup,
  TrendParamDef,
  TrendParamCreate,
  Unit,
} from "../../../../../../services/api";
import { LDSContext } from "../../../../contexts/ldsContext";
import { useHandleApiResponse } from "../../../../../../hooks/useHandleApiResponse";

interface Props {
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  trendParamDefs: TrendParamDef[];
  units: Unit[];
  selected: Trend | null;
  editTrend: (id: number, v: TrendUpdate) => Promise<void>;
  addTrend: (v: TrendCreate) => Promise<Trend>;
  deleteTrend: (value: Trend) => Promise<void>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  closePanel: () => void;
}

interface TrendFormValues {
  Name: string;
  TrendDef: TrendDef | null;
  TrendGroup: TrendGroup | null;
  Unit: Unit | null;
  Color: string;
  RawMin: number | null;
  RawMax: number | null;
  ScaledMin: number | null;
  ScaledMax: number | null;
}

interface ValidationErrors {
  [key: string]: string;
}

const trendValidator = (t: TFunction) => (values: TrendFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.Name?.trim()) {
    errors.Name = t("config-page:name_required");
  }

  if (!values.TrendDef) {
    errors.TrendDefID = t("config-page:type_required");
  }

  if (!values.TrendGroup) {
    errors.TrendGroupID = t("config-page:group_required");
  }

  if (!values.Unit) {
    errors.UnitID = t("config-page:unit_required");
  }

  if (
    values.RawMin != null &&
    values.RawMax != null &&
    values.RawMin === values.RawMax
  ) {
    errors.RawMin = " ";
    errors.RawMax = t("config-page:raw_same");
  }

  if (
    values.RawMin != null &&
    values.RawMax != null &&
    values.RawMin > values.RawMax
  ) {
    errors.RawMin = " ";
    errors.RawMax = t("config-page:raw_range");
  }

  if (
    values.ScaledMin != null &&
    values.ScaledMax != null &&
    values.ScaledMin > values.ScaledMax
  ) {
    errors.ScaledMin = " ";
    errors.ScaledMax = t("config-page:scaled_same");
  }

  if (
    values.ScaledMin != null &&
    values.ScaledMax != null &&
    values.ScaledMin === values.ScaledMax
  ) {
    errors.ScaledMin = " ";
    errors.ScaledMax = t("config-page:scaled_range");
  }

  return Object.keys(errors).length ? errors : undefined;
};

const ValidatedTextBox = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...inputProps } = props;

  return (
    <div className="field-wrapper">
      <TextBox {...inputProps} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedDropDown = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, data, ...inputProps } = props;

  return (
    <div className="field-wrapper">
      <DropDownList {...inputProps} data={data} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedNumericTextBox = (props: FieldRenderProps) => {
  const {
    validationMessage,
    touched,
    visited,
    valid,
    modified,
    ...inputProps
  } = props;

  return (
    <div className="field-wrapper">
      <NumericTextBox
        {...inputProps}
        validationMessage={validationMessage ?? undefined}
      />

      {(touched || visited) && validationMessage && (
        <Error className="error-container">{validationMessage}</Error>
      )}
    </div>
  );
};

const ColorPickerField = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...rest } = props;

  return (
    <div className="field-wrapper">
      <FlatColorPicker
        {...rest}
        showButtons={false}
        showClearButton={false}
        showPreview={false}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const TrendConfigurationDetailPanel = memo(function Panel({
  trendDefs,
  trendGroups,
  trendParamDefs,
  units,
  selected,
  editTrend,
  addTrend,
  deleteTrend,
  addMode,
  setAddMode,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "config-page"]);
  const ldsContext = useContext(LDSContext);
  const handleApiResponse = useHandleApiResponse();
  const [inEdit, setInEdit] = useState(addMode);
  const [loading, setLoading] = useState(false);
  const [paramsLoaded, setParamsLoaded] = useState(addMode);
  const [trendParams, setTrendParams] = useState<number[]>([]);
  const [activeTrendDefId, setActiveTrendDefId] = useState<
    TrendDef["ID"] | undefined
  >(selected?.TrendDefID);

  const requiredTrendParams = useMemo(
    () => trendParamDefs.filter((d) => d.TrendDefID === activeTrendDefId),
    [trendParamDefs, activeTrendDefId],
  );

  useEffect(() => {
    if (addMode) {
      setTrendParams([]);
      setParamsLoaded(true);
      return;
    }

    if (!selected) {
      setTrendParams([]);
      setParamsLoaded(true);
      return;
    }

    setParamsLoaded(false);
    const trendId = selected.ID;
    const paramCount = trendParamDefs.filter(
      (d) => d.TrendDefID === selected.TrendDefID,
    ).length;

    async function loadParams() {
      try {
        const res =
          await ldsContext!.trendParamApi.listTrendParamsByTrendIdTrendTrendIdParamGet(
            trendId,
          );
        const values = res.data?.items?.map((p) => Number(p.Value)) ?? [];
        setTrendParams(
          Array.from({ length: paramCount }, (_, i) => values[i] ?? 0),
        );
      } catch {
        setTrendParams(Array(paramCount).fill(0));
      } finally {
        setParamsLoaded(true);
      }
    }

    loadParams();
  }, [selected, addMode]);

  const initialValues = useMemo((): TrendFormValues => {
    if (addMode || !selected) {
      return {
        Name: "",
        TrendDef: null,
        TrendGroup: null,
        Unit: null,
        Color: "#000000",
        RawMin: 0,
        RawMax: 0,
        ScaledMin: 0,
        ScaledMax: 0,
      };
    }

    return {
      Name: selected.Name,
      TrendDef: trendDefs.find((d) => d.ID === selected.TrendDefID) ?? null,
      TrendGroup:
        trendGroups.find((g) => g.ID === selected.TrendGroupID) ?? null,
      Unit: units.find((u) => u.ID === selected.UnitID) ?? null,
      Color: selected.Color ?? "#000000",
      RawMin: selected.RawMin ?? 0,
      RawMax: selected.RawMax ?? 0,
      ScaledMin: selected.ScaledMin ?? 0,
      ScaledMax: selected.ScaledMax ?? 0,
    };
  }, [selected, addMode, trendDefs, trendGroups, units]);

  const saveTrendParams = useCallback(
    async (trendId: number) => {
      for (let i = 0; i < requiredTrendParams.length; i++) {
        const value: TrendParamCreate = {
          TrendParamDefID: requiredTrendParams[i].ID,
          Value: String(trendParams[i] ?? 0),
        };

        await handleApiResponse(
          ldsContext!.trendParamApi.createTrendParamTrendTrendIdParamPost.bind(
            ldsContext!.trendParamApi,
          ),
          trendId,
          value,
        );
      }
    },
    [requiredTrendParams, trendParams, ldsContext, handleApiResponse],
  );

  const handleSubmit = useCallback(
    async (values: TrendFormValues) => {
      setLoading(true);
      const payload: TrendCreate = {
        Name: values.Name,
        TrendDefID: values.TrendDef!.ID,
        TrendGroupID: values.TrendGroup!.ID,
        UnitID: values.Unit!.ID,
        Color: values.Color,
        RawMin: values.RawMin ?? 0,
        RawMax: values.RawMax ?? 0,
        ScaledMin: values.ScaledMin ?? 0,
        ScaledMax: values.ScaledMax ?? 0,
      };

      try {
        setLoading(true);
        if (addMode) {
          const trend = await addTrend(payload);
          await saveTrendParams(trend.ID);

          closePanel();

          return;
        }

        if (!selected) return;

        await editTrend(selected.ID, payload as TrendUpdate);
        await saveTrendParams(selected.ID);
        setInEdit(false);
      } finally {
        setLoading(false);
      }
    },
    [
      addMode,
      addTrend,
      editTrend,
      selected,
      setAddMode,
      closePanel,
      saveTrendParams,
    ],
  );

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      validator={trendValidator(t)}
      onSubmit={(values) => handleSubmit(values as TrendFormValues)}
      render={(formRenderProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("config-page:name")}</Label>
              <Field
                name="Name"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:trend_type")}</Label>
              <Field
                name="TrendDef"
                component={ValidatedDropDown}
                disabled={!inEdit}
                data={trendDefs}
                textField="Name"
                dataItemKey="ID"
                onChange={(e: { value: TrendDef | null }) => {
                  setActiveTrendDefId(e.value?.ID);
                  const newParamCount = trendParamDefs.filter(
                    (d) => d.TrendDefID === e.value?.ID,
                  ).length;
                  setTrendParams(Array(newParamCount).fill(0));
                  formRenderProps.onChange("TrendDef", { value: e.value });
                }}
              />
            </div>
            <div>
              <Label>{t("config-page:trend_group")}</Label>
              <Field
                name="TrendGroup"
                component={ValidatedDropDown}
                disabled={!inEdit}
                data={trendGroups}
                textField="Name"
                dataItemKey="ID"
              />
            </div>
            <div>
              <Label>{t("config-page:unit")}</Label>
              <Field
                name="Unit"
                component={ValidatedDropDown}
                disabled={!inEdit}
                data={units}
                textField="Symbol"
                dataItemKey="ID"
              />
            </div>

            <div>
              <Label>{t("config-page:color")}</Label>
              <Field
                name="Color"
                component={ColorPickerField}
                disabled={!inEdit}
              />
            </div>

            {!loading &&
              requiredTrendParams.map((trendParam, index) => (
                <div key={trendParam.ID}>
                  <Label>{trendParam.Name}</Label>
                  <NumericTextBox
                    value={trendParams[index] ?? 0}
                    disabled={!inEdit}
                    onChange={(e) => {
                      const copy = [...trendParams];
                      copy[index] = e.value ?? 0;
                      setTrendParams(copy);
                    }}
                  />
                </div>
              ))}
            <div>
              <Label>{t("config-page:raw_min")}</Label>
              <Field
                name="RawMin"
                component={ValidatedNumericTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:raw_max")}</Label>
              <Field
                name="RawMax"
                component={ValidatedNumericTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:scaled_min")}</Label>
              <Field
                name="ScaledMin"
                component={ValidatedNumericTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:scaled_max")}</Label>
              <Field
                name="ScaledMax"
                component={ValidatedNumericTextBox}
                disabled={!inEdit}
              />
            </div>
          </div>

          <div className="separator" />

          <div className="item-row">
            {!inEdit && !addMode ? (
              <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
                {t("common:edit")}
              </Button>
            ) : (
              <>
                <Button
                  svgIcon={cancelIcon}
                  disabled={loading}
                  onClick={() => {
                    setAddMode(false);
                    setInEdit(false);
                    formRenderProps.onFormReset();
                    setActiveTrendDefId(selected?.TrendDefID);
                  }}
                >
                  {t("common:cancel")}
                </Button>

                {!addMode && selected && (
                  <Button
                    svgIcon={trashIcon}
                    disabled={loading}
                    onClick={() => deleteTrend(selected)}
                  >
                    {t("common:delete")}
                  </Button>
                )}

                <Button
                  type="submit"
                  svgIcon={saveIcon}
                  themeColor="primary"
                  disabled={!formRenderProps.allowSubmit || loading}
                >
                  {addMode ? t("common:add") : t("common:save")}
                </Button>
              </>
            )}
          </div>
        </FormElement>
      )}
    />
  );
});

export default TrendConfigurationDetailPanel;
