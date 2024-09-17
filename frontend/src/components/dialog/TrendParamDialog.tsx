import React from 'react';
import {Dialog, DialogActionsBar} from '@progress/kendo-react-dialogs';
import {Form, Field, FormElement, FieldRenderProps, FieldWrapper} from "@progress/kendo-react-form";
import {TextBox} from "@progress/kendo-react-inputs";
import {Button} from '@progress/kendo-react-buttons';
import {TrendParam} from '../../services/api';
import {Error, Label} from "@progress/kendo-react-labels";
import "../../assets/components/dialog/trenddialogs.scss"

interface TrendParamDialogProps {
    data: TrendParam | null;
    onSubmit: (data: TrendParam) => void;
    onCancel: () => void;
}

const TextBoxField = (fieldRenderProps: FieldRenderProps) => {
    const {validationMessage, visited, label, id, ...others} = fieldRenderProps;
    return (
        <>
            <Label editorId={id} className={"k-form-label"}>
                {label}
            </Label>
            <div className={"k-form-field-wrap"}>
                <TextBox {...others} />
                {visited && validationMessage && <Error>{validationMessage}</Error>}
            </div>
        </>
    );
};

const TrendParamDialog = ({data, onSubmit, onCancel}: TrendParamDialogProps) => {
    return (
        <Dialog title="Trend Parameter Details" onClose={onCancel}>
            <Form
                initialValues={data || {}}
                onSubmit={(values) => onSubmit(values as TrendParam)}
                render={(formRenderProps) => (
                    <form onSubmit={formRenderProps.onSubmit}>
                        <FormElement>
                            <FieldWrapper>
                                <Field
                                    name={"Value"}
                                    component={TextBoxField}
                                    label={"Value"}
                                    required
                                    validator={(value) => value ? "" : "Value is required"}
                                />
                            </FieldWrapper>
                        </FormElement>

                        <DialogActionsBar>
                            <Button
                                type={"submit"}
                                className="save-button"
                                themeColor={"primary"}
                                disabled={!formRenderProps.allowSubmit}
                                onClick={formRenderProps.onSubmit}
                            >
                                Save
                            </Button>
                            <Button
                                className="cancel-button"
                                onClick={onCancel}
                            >
                                Cancel
                            </Button>
                        </DialogActionsBar>
                    </form>
                )}
            />
        </Dialog>
    );
};

export default TrendParamDialog;
