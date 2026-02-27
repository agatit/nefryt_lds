// import {
//   memo,
//   useState,
//   useEffect,
//   useContext,
//   useCallback,
//   useMemo,
// } from "react";
// import { useTranslation } from "react-i18next";
// import { TFunction } from "i18next";
// import {
//   Form,
//   Field,
//   FormElement,
//   FieldRenderProps,
// } from "@progress/kendo-react-form";
// import { TextBox, NumericTextBox } from "@progress/kendo-react-inputs";
// import { Label, Error } from "@progress/kendo-react-labels";
// import { Button } from "@progress/kendo-react-buttons";
// import {
//   cancelIcon,
//   saveIcon,
//   trashIcon,
//   pencilIcon,
// } from "@progress/kendo-svg-icons";
// import { DropDownList } from "@progress/kendo-react-dropdowns";
// import {
//   Method,
//   MethodCreate,
//   MethodUpdate,
//   MethodDef,
//   MethodParamDef,
//   MethodParamCreate,
// } from "../../../../../../services/api";
// import { LDSContext } from "../../../../contexts/ldsContext";

// interface Props {
//   selected: Method | null;
//   updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
//   requestDelete: () => void;
//   addMethod: (value: MethodCreate) => Promise<Method>;
//   addMode: boolean;
//   setAddMode: (v: boolean) => void;
//   pipelines: any[];
//   methodDefs: MethodDef[];
//   closePanel: () => void;
// }

// interface ValidationErrors {
//   [key: string]: string;
// }

// export interface MethodFormValues {
//   MethodDefID: MethodDef | null;
//   PipelineID: { ID: number; Name: string } | null;
//   Name?: string;
// }

// const ValidatedTextBox = (props: FieldRenderProps) => {
//   const { validationMessage, touched, modified, ...inputProps } = props;

//   return (
//     <div className="field-wrapper">
//       <TextBox {...inputProps} />
//       {(touched || modified) && validationMessage && (
//         <Error>{validationMessage}</Error>
//       )}
//     </div>
//   );
// };

// const ValidatedDropDown = (props: FieldRenderProps) => {
//   const { validationMessage, touched, modified, data, ...inputProps } = props;

//   return (
//     <div className="field-wrapper">
//       <DropDownList {...inputProps} data={data} />
//       {(touched || modified) && validationMessage && (
//         <Error>{validationMessage}</Error>
//       )}
//     </div>
//   );
// };

// const methodValidator = (t: TFunction) => (values: MethodFormValues) => {
//   const errors: ValidationErrors = {};
//   if (!values.PipelineID)
//     errors.PipelineID = t("methods-page:pipeline_required");
//   if (!values.MethodDefID)
//     errors.MethodDefID = t("methods-page:method_def_required");
//   return Object.keys(errors).length ? errors : undefined;
// };

// const MethodsDetailPanel = memo(function MethodsDetailPanel({
//   selected,
//   updateMethod,
//   requestDelete,
//   addMethod,
//   addMode,
//   setAddMode,
//   pipelines,
//   closePanel,
//   methodDefs,
// }: Props) {
//   const { t } = useTranslation(["common", "methods-page"]);
//   const ldsContext = useContext(LDSContext);
//   const [inEdit, setInEdit] = useState(false);
//   const [loading, setLoading] = useState(false);
//   const [activeMethodDefId, setActiveMethodDefId] = useState<
//     string | undefined
//   >(selected?.MethodDefID);
//   const [paramValues, setParamValues] = useState<number[]>([]);
//   const [displayParams, setDisplayParams] = useState<MethodParamDef[]>([]);

//   const requiredParams = useMemo(
//     () =>
//       ldsContext?.methodParamDefs.filter(
//         (d) => d.MethodDefID === activeMethodDefId,
//       ) ?? [],
//     [ldsContext?.methodParamDefs, activeMethodDefId],
//   );

//   useEffect(() => {
//     setActiveMethodDefId(selected?.MethodDefID);

//     if (!selected) {
//       setParamValues([]);
//       return;
//     }

//     if (addMode) {
//       setParamValues([]);
//       return;
//     }

//     const existingParams =
//       ldsContext?.methodParams.filter((p) => p.MethodID === selected.ID) ?? [];

//     const paramDefs =
//       ldsContext?.methodParamDefs.filter(
//         (d) => d.MethodDefID === selected.MethodDefID,
//       ) ?? [];

//     setParamValues(
//       paramDefs.map((def) => {
//         const found = existingParams.find((p) => p.MethodParamDefID === def.ID);
//         return Number(found?.Value ?? 0);
//       }),
//     );
//   }, [
//     selected,
//     addMode,
//     ldsContext?.methodParams,
//     ldsContext?.methodParamDefs,
//   ]);

//   useEffect(() => {
//     if (!loading) {
//       setDisplayParams(requiredParams);
//     }
//   }, [requiredParams, loading]);

//   useEffect(() => setInEdit(addMode), [selected, addMode]);

//   const saveParams = useCallback(
//     async (
//       methodID: number,
//       paramsToSave: MethodParamDef[],
//       values: number[],
//     ) => {
//       if (!ldsContext) return;
//       for (let i = 0; i < paramsToSave.length; i++) {
//         const payload: MethodParamCreate = {
//           MethodParamDefID: paramsToSave[i].ID,
//           Value: String(values[i] ?? 0),
//         };
//         await ldsContext.addMethodParam(methodID, payload);
//       }
//     },
//     [ldsContext],
//   );

//   const handleSubmit = async (values: MethodFormValues) => {
//     if (!ldsContext) return;

//     setDisplayParams(requiredParams);
//     setLoading(true);

//     try {
//       if (addMode) {
//         // On add: create with all fields including MethodDefID, then save params
//         const payload: MethodCreate = {
//           Name: values.Name,
//           PipelineID: values.PipelineID!.ID,
//           MethodDefID: values.MethodDefID!.ID,
//         };
//         const method = await addMethod(payload);
//         await saveParams(method.ID, requiredParams, paramValues);
//         closePanel();
//         return;
//       }

//       // On edit: MethodDef and params cannot be changed — only Name and PipelineID
//       const updatePayload: MethodUpdate = {
//         Name: values.Name,
//         PipelineID: values.PipelineID!.ID,
//       };
//       await updateMethod(selected!.ID, updatePayload);
//       setInEdit(false);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const initialValues = useMemo((): MethodFormValues => {
//     if (addMode || !selected) {
//       return {
//         Name: "",
//         PipelineID: null,
//         MethodDefID: null,
//       };
//     }

//     return {
//       Name: selected.Name ?? "",
//       PipelineID: pipelines.find((p) => p.ID === selected.PipelineID) ?? null,
//       MethodDefID:
//         methodDefs.find((d) => d.ID === selected.MethodDefID) ?? null,
//     };
//   }, [selected, addMode, pipelines, methodDefs]);

//   if (!paramsLoaded) return null;

//   return (
//     <Form
//       key={addMode ? "add" : selected?.ID}
//       initialValues={initialValues}
//       validator={methodValidator(t)}
//       onSubmit={(values) => handleSubmit(values as MethodFormValues)}
//       render={(formProps) => (
//         <FormElement className="detail-panel-content">
//           <div className="item-column">
//             <div>
//               <Label>{t("methods-page:pipeline")}</Label>
//               <Field
//                 name="PipelineID"
//                 component={ValidatedDropDown}
//                 data={pipelines}
//                 textField="Name"
//                 dataItemKey="ID"
//                 disabled={!inEdit}
//               />
//             </div>
//             <div>
//               <Label>{t("methods-page:method_definition")}</Label>
//               <Field
//                 name="MethodDefID"
//                 component={ValidatedDropDown}
//                 data={methodDefs}
//                 textField="Name"
//                 dataItemKey="ID"
//                 disabled={!inEdit || !addMode}
//                 onChange={(e: { value: MethodDef | null }) => {
//                   setActiveMethodDefId(e.value?.ID);
//                   const newCount =
//                     ldsContext?.methodParamDefs.filter(
//                       (d) => d.MethodDefID === e.value?.ID,
//                     ).length ?? 0;
//                   setParamValues(Array(newCount).fill(0));
//                   formProps.onChange("MethodDefID", { value: e.value });
//                 }}
//               />
//             </div>
//             <div>
//               <Label>{t("methods-page:name")}</Label>
//               <Field
//                 name="Name"
//                 component={ValidatedTextBox}
//                 disabled={!inEdit}
//               />
//             </div>
//             {displayParams.map((paramDef, index) => (
//               <div
//                 key={paramDef.ID}
//                 style={{ display: "flex", flexDirection: "column" }}
//               >
//                 <Label>{paramDef.Name ?? paramDef.ID}</Label>
//                 <NumericTextBox
//                   value={paramValues[index] ?? 0}
//                   disabled={!inEdit || !addMode}
//                   onChange={(e) => {
//                     const copy = [...paramValues];
//                     copy[index] = e.value ?? 0;
//                     setParamValues(copy);
//                   }}
//                 />
//               </div>
//             ))}
//           </div>
//           <div className="separator" />
//           <div className="item-row">
//             {!inEdit && !addMode ? (
//               <Button
//                 type="button"
//                 svgIcon={pencilIcon}
//                 onClick={() => setInEdit(true)}
//               >
//                 {t("common:edit")}
//               </Button>
//             ) : (
//               <>
//                 <Button
//                   type="button"
//                   svgIcon={cancelIcon}
//                   disabled={loading}
//                   onClick={() => {
//                     setAddMode(false);
//                     setInEdit(false);
//                     setActiveMethodDefId(selected?.MethodDefID);
//                     formProps.onFormReset();
//                   }}
//                 >
//                   {t("common:cancel")}
//                 </Button>

//                 {!addMode && selected && (
//                   <Button
//                     type="button"
//                     svgIcon={trashIcon}
//                     disabled={loading}
//                     onClick={requestDelete}
//                   >
//                     {t("common:delete")}
//                   </Button>
//                 )}

//                 <Button
//                   type="submit"
//                   svgIcon={saveIcon}
//                   themeColor="primary"
//                   disabled={!formProps.allowSubmit || loading}
//                 >
//                   {addMode ? t("common:add") : t("common:save")}
//                 </Button>
//               </>
//             )}
//           </div>
//         </FormElement>
//       )}
//     />
//   );
// });

// export default MethodsDetailPanel;

import {
  memo,
  useState,
  useEffect,
  useContext,
  useCallback,
  useMemo,
} from "react";
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { TextBox, NumericTextBox } from "@progress/kendo-react-inputs";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  cancelIcon,
  saveIcon,
  trashIcon,
  pencilIcon,
} from "@progress/kendo-svg-icons";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import {
  Method,
  MethodCreate,
  MethodUpdate,
  MethodDef,
  MethodParamDef,
  MethodParamCreate,
} from "../../../../../../services/api";
import { LDSContext } from "../../../../contexts/ldsContext";

interface Props {
  selected: Method | null;
  updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
  requestDelete: () => void;
  addMethod: (value: MethodCreate) => Promise<Method>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  pipelines: any[];
  methodDefs: MethodDef[];
  closePanel: () => void;
}

interface ValidationErrors {
  [key: string]: string;
}

export interface MethodFormValues {
  MethodDefID: MethodDef | null;
  PipelineID: { ID: number; Name: string } | null;
  Name?: string;
}

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

const methodValidator = (t: TFunction) => (values: MethodFormValues) => {
  const errors: ValidationErrors = {};
  if (!values.PipelineID)
    errors.PipelineID = t("methods-page:pipeline_required");
  if (!values.MethodDefID)
    errors.MethodDefID = t("methods-page:method_def_required");
  return Object.keys(errors).length ? errors : undefined;
};

const MethodsDetailPanel = memo(function MethodsDetailPanel({
  selected,
  updateMethod,
  requestDelete,
  addMethod,
  addMode,
  setAddMode,
  pipelines,
  closePanel,
  methodDefs,
}: Props) {
  const { t } = useTranslation(["common", "methods-page"]);
  const ldsContext = useContext(LDSContext);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activeMethodDefId, setActiveMethodDefId] = useState<
    string | undefined
  >(undefined);

  const [editParamValues, setEditParamValues] = useState<number[]>([]);

  useEffect(() => setInEdit(addMode), [selected, addMode]);

  useEffect(() => {
    if (addMode) {
      setActiveMethodDefId(undefined);
      setEditParamValues([]);
    }
  }, [addMode]);

  const selectedParamDefs = useMemo(() => {
    if (!selected || addMode) return [];
    return (
      ldsContext?.methodParamDefs.filter(
        (d) => d.MethodDefID === selected.MethodDefID,
      ) ?? []
    );
  }, [selected, addMode, ldsContext?.methodParamDefs]);

  const selectedParamValues = useMemo(() => {
    if (!selected || addMode) return [];
    const existingParams =
      ldsContext?.methodParams.filter((p) => p.MethodID === selected.ID) ?? [];
    return selectedParamDefs.map((def) => {
      const found = existingParams.find((p) => p.MethodParamDefID === def.ID);
      return Number(found?.Value ?? 0);
    });
  }, [selected, addMode, selectedParamDefs, ldsContext?.methodParams]);

  const addModeParamDefs = useMemo(() => {
    if (!addMode) return [];
    return (
      ldsContext?.methodParamDefs.filter(
        (d) => d.MethodDefID === activeMethodDefId,
      ) ?? []
    );
  }, [addMode, activeMethodDefId, ldsContext?.methodParamDefs]);

  const displayParams = addMode ? addModeParamDefs : selectedParamDefs;
  const displayParamValues = addMode ? editParamValues : selectedParamValues;

  const saveParams = useCallback(
    async (
      methodID: number,
      paramsToSave: MethodParamDef[],
      values: number[],
    ) => {
      if (!ldsContext) return;
      for (let i = 0; i < paramsToSave.length; i++) {
        const payload: MethodParamCreate = {
          MethodParamDefID: paramsToSave[i].ID,
          Value: String(values[i] ?? 0),
        };
        await ldsContext.addMethodParam(methodID, payload);
      }
    },
    [ldsContext],
  );

  const handleSubmit = async (values: MethodFormValues) => {
    if (!ldsContext) return;
    setLoading(true);

    try {
      if (addMode) {
        const payload: MethodCreate = {
          Name: values.Name,
          PipelineID: values.PipelineID!.ID,
          MethodDefID: values.MethodDefID!.ID,
        };
        const method = await addMethod(payload);
        await saveParams(method.ID, addModeParamDefs, editParamValues);
        closePanel();
        return;
      }

      const updatePayload: MethodUpdate = {
        Name: values.Name,
        PipelineID: values.PipelineID!.ID,
      };
      await updateMethod(selected!.ID, updatePayload);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  const initialValues = useMemo((): MethodFormValues => {
    if (addMode || !selected) {
      return { Name: "", PipelineID: null, MethodDefID: null };
    }
    return {
      Name: selected.Name ?? "",
      PipelineID: pipelines.find((p) => p.ID === selected.PipelineID) ?? null,
      MethodDefID:
        methodDefs.find((d) => d.ID === selected.MethodDefID) ?? null,
    };
  }, [selected, addMode, pipelines, methodDefs]);

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      validator={methodValidator(t)}
      onSubmit={(values) => handleSubmit(values as MethodFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("methods-page:pipeline")}</Label>
              <Field
                name="PipelineID"
                component={ValidatedDropDown}
                data={pipelines}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("methods-page:method_definition")}</Label>
              <Field
                name="MethodDefID"
                component={ValidatedDropDown}
                data={methodDefs}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit || !addMode}
                onChange={(e: { value: MethodDef | null }) => {
                  setActiveMethodDefId(e.value?.ID);
                  const newCount =
                    ldsContext?.methodParamDefs.filter(
                      (d) => d.MethodDefID === e.value?.ID,
                    ).length ?? 0;
                  setEditParamValues(Array(newCount).fill(0));
                  formProps.onChange("MethodDefID", { value: e.value });
                }}
              />
            </div>
            <div>
              <Label>{t("methods-page:name")}</Label>
              <Field
                name="Name"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
            </div>
            {displayParams.map((paramDef, index) => (
              <div
                key={paramDef.ID}
                style={{ display: "flex", flexDirection: "column" }}
              >
                <Label>{paramDef.Name ?? paramDef.ID}</Label>
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
          </div>
          <div className="separator" />
          <div className="item-row">
            {!inEdit && !addMode ? (
              <Button
                type="button"
                svgIcon={pencilIcon}
                onClick={() => setInEdit(true)}
              >
                {t("common:edit")}
              </Button>
            ) : (
              <>
                <Button
                  type="button"
                  svgIcon={cancelIcon}
                  disabled={loading}
                  onClick={() => {
                    setAddMode(false);
                    setInEdit(false);
                    formProps.onFormReset();
                  }}
                >
                  {t("common:cancel")}
                </Button>

                {!addMode && selected && (
                  <Button
                    type="button"
                    svgIcon={trashIcon}
                    disabled={loading}
                    onClick={requestDelete}
                  >
                    {t("common:delete")}
                  </Button>
                )}

                <Button
                  type="submit"
                  svgIcon={saveIcon}
                  themeColor="primary"
                  disabled={!formProps.allowSubmit || loading}
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

export default MethodsDetailPanel;

