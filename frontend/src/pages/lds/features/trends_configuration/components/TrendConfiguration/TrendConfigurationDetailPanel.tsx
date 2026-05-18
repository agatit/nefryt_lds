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
  if (values.RawMin != null && values.RawMax != null) {
    if (values.RawMin > values.RawMax) {
      errors.RawMin = t("config-page:raw_range");
      errors.RawMax = t("config-page:raw_range");
    } else if (values.RawMin === values.RawMax) {
      errors.RawMin = t("config-page:raw_same");
      errors.RawMax = t("config-page:raw_same");
    }
  }
  if (values.ScaledMin != null && values.ScaledMax != null) {
    if (values.ScaledMin > values.ScaledMax) {
      errors.ScaledMin = t("config-page:scaled_range");
      errors.ScaledMax = t("config-page:scaled_range");
    } else if (values.ScaledMin === values.ScaledMax) {
      errors.ScaledMin = t("config-page:scaled_same");
      errors.ScaledMax = t("config-page:scaled_same");
    }
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
  const { validationMessage, touched, valid, modified, ...inputProps } = props;
  return (
    <div className="field-wrapper">
      <NumericTextBox
        {...inputProps}
        validationMessage={validationMessage ?? undefined}
      />
      {(touched || modified) && validationMessage && (
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
  const [paramsLoaded, setParamsLoaded] = useState(false);
  const [activeTrendDefId, setActiveTrendDefId] = useState<
    TrendDef["ID"] | undefined
  >(undefined);

  const [loadedTrendParams, setLoadedTrendParams] = useState<number[]>([]);
  const [editParamValues, setEditParamValues] = useState<number[]>([]);

  const requiredTrendParams = useMemo(
    () => trendParamDefs.filter((d) => d.TrendDefID === activeTrendDefId),
    [trendParamDefs, activeTrendDefId],
  );

  useEffect(() => {
    setInEdit(addMode);
  }, [addMode]);

  useEffect(() => {
    if (addMode) {
      setActiveTrendDefId(undefined);
      setLoadedTrendParams([]);
      setEditParamValues([]);
      setParamsLoaded(true);
      return;
    }

    if (!selected) {
      setActiveTrendDefId(undefined);
      setLoadedTrendParams([]);
      setParamsLoaded(true);
      return;
    }

    setActiveTrendDefId(selected.TrendDefID);
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
        const items = res.data?.items ?? [];
        const values = items.map((p) => Number(p.Value));
        setLoadedTrendParams(
          Array.from({ length: paramCount }, (_, i) => values[i] ?? 0),
        );
      } catch {
        setLoadedTrendParams(Array(paramCount).fill(0));
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

  const displayParamValues = addMode ? editParamValues : loadedTrendParams;

  const saveTrendParams = useCallback(
    async (trendId: number, paramValues: number[]) => {
      for (let i = 0; i < requiredTrendParams.length; i++) {
        const paramDef = requiredTrendParams[i];
        const create: TrendParamCreate = {
          TrendParamDefID: paramDef.ID,
          Value: String(paramValues[i] ?? 0),
        };
        await handleApiResponse(
          ldsContext!.trendParamApi.createTrendParamTrendTrendIdParamPost.bind(
            ldsContext!.trendParamApi,
          ),
          trendId,
          create,
        );
      }
    },
    [requiredTrendParams, ldsContext, handleApiResponse],
  );

  const handleSubmit = useCallback(
    async (values: TrendFormValues) => {
      setLoading(true);
      try {
        if (addMode) {
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
          const trend = await addTrend(payload);
          await saveTrendParams(trend.ID, editParamValues);
          closePanel();
          return;
        }

        if (!selected) return;

        const updatePayload: TrendUpdate = {
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
        await editTrend(selected.ID, updatePayload);
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
      closePanel,
      saveTrendParams,
      editParamValues,
    ],
  );

  if (!paramsLoaded) return null;

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
                disabled={!inEdit || !addMode}
                data={trendDefs}
                textField="Name"
                dataItemKey="ID"
                onChange={(e: { value: TrendDef | null }) => {
                  const newParamCount = trendParamDefs.filter(
                    (d) => d.TrendDefID === e.value?.ID,
                  ).length;
                  setActiveTrendDefId(e.value?.ID);
                  setEditParamValues(Array(newParamCount).fill(0));
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

            {requiredTrendParams.map((trendParam, index) => (
              <div key={trendParam.ID}>
                <Label>{trendParam.Name}</Label>
                <NumericTextBox
                  value={displayParamValues[index] ?? 0}
                  disabled={!inEdit || !addMode}
                  onChange={(e) => {
                    const copy = [...editParamValues];
                    copy[index] = e.value ?? 0;
                    setEditParamValues(copy);
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
                    setEditParamValues([]);
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
