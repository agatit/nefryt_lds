import React from 'react';
import {Dialog, DialogActionsBar} from '@progress/kendo-react-dialogs';
import {Form, Field, FormElement, FieldWrapper, FieldRenderProps} from '@progress/kendo-react-form';
import {Input, NumericTextBox} from '@progress/kendo-react-inputs';
import {DropDownList, DropDownListChangeEvent} from "@progress/kendo-react-dropdowns";
import {Button} from '@progress/kendo-react-buttons';
import {Label, Error} from "@progress/kendo-react-labels";
import {Trend, TrendDef} from "../../services/api";

interface TrendDialogProps {
    data: Trend;
    trendDefs: TrendDef[];
    onSubmit: (data: any) => void;
    onCancel: () => void;
}

const TextBoxField = (fieldRenderProps: FieldRenderProps) => {
    const {validationMessage, visited, label, id, valid, ...others} = fieldRenderProps;
    return (
        <>
            <Label editorId={id} className={"k-form-label"}>
                {label}
            </Label>
            <div className={"k-form-field-wrap"}>
                <Input {...others} />
                {visited && validationMessage && <Error>{validationMessage}</Error>}
            </div>
        </>
    );
};

const NumericTextBoxField = (fieldRenderProps: FieldRenderProps) => {
    const {validationMessage, visited, label, id, valid, ...others} = fieldRenderProps;
    return (
        <>
            <Label editorId={id} className={"k-form-label"}>
                {label}
            </Label>
            <div className={"k-form-field-wrap"}>
                <NumericTextBox {...others} />
                {visited && validationMessage && <Error>{validationMessage}</Error>}
            </div>
        </>
    );
};

const DropDownListField = (fieldRenderProps: FieldRenderProps) => {
    const {validationMessage, visited, label, id, onChange, ...others} = fieldRenderProps;
    console.log("PROPS: ", fieldRenderProps.data);


    const handleChange = (event: DropDownListChangeEvent) => {
        const newValue = event.target.value;
        console.log('SELECTED VALUE:', newValue);
        console.log('ID SELECTED VALUE:', event.target.value.ID);
        onChange({target: event.target, value: event.target.value.ID});
    };

    return (
        <>
            <Label editorId={id} className={"k-form-label"}>
                {label}
            </Label>
            <div className={"k-form-field-wrap"}>
                <DropDownList
                    {...others}
                    data={fieldRenderProps.data}
                    onChange={handleChange}
                />
                {visited && validationMessage && <Error>{validationMessage}</Error>}
            </div>
        </>
    );
};

const TrendDialog = ({data, trendDefs, onSubmit, onCancel}: TrendDialogProps) => {
    console.log('INITIAL DATA:', data);

    return (
        <Dialog title="Trend" onClose={onCancel}>
            <Form
                initialValues={data}
                onSubmit={(formData) => {
                    console.log('DATA:', formData);
                    onSubmit(formData);
                }}
                // onSubmit={onSubmit}
                render={(formRenderProps) => (
                    <FormElement>
                        <FieldWrapper>
                            <Field
                                name="Name"
                                component={TextBoxField}
                                label="Trend Name"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="TrendDefID"
                                component={DropDownListField}
                                label="Trend Definition"
                                data={trendDefs}
                                textField="Name"
                                valueField="ID"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="RawMin"
                                component={NumericTextBoxField}
                                label="Raw Min"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="RawMax"
                                component={NumericTextBoxField}
                                label="Raw Max"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="ScaledMin"
                                component={NumericTextBoxField}
                                label="Scaled Min"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="ScaledMax"
                                component={NumericTextBoxField}
                                label="Scaled Max"
                            />
                        </FieldWrapper>
                        <DialogActionsBar>
                            <Button
                                type={"submit"}
                                themeColor={"primary"}
                                disabled={!formRenderProps.allowSubmit}
                                onClick={formRenderProps.onSubmit}
                            >
                                Save
                            </Button>
                            <Button
                                onClick={onCancel}
                            >
                                Cancel
                            </Button>
                        </DialogActionsBar>
                    </FormElement>
                )}
            />
        </Dialog>
    );
};

export default TrendDialog;
