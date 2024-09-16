import React from 'react';
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import {Form, Field, FormElement, FieldWrapper, FieldRenderProps} from '@progress/kendo-react-form';
import { Input } from '@progress/kendo-react-inputs';
import { Button } from '@progress/kendo-react-buttons';
import { Label, Error } from "@progress/kendo-react-labels";
import { EventDef } from "../../services/api";
import "../../assets/components/eventdefdialog.scss"

interface EventDefDialogProps {
    onClose: () => void;
    onSubmit: (data: any) => void;
    initialValues: EventDef;
}

const TextBoxField = (fieldRenderProps: FieldRenderProps) => {
    const { validationMessage, visited, label, id, valid, ...others } = fieldRenderProps;
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

const CheckboxField = (fieldRenderProps: FieldRenderProps) => {
    const { label, id, ...others } = fieldRenderProps;
    return (
        <div className="k-form-field">
            <Label editorId={id} className="k-checkbox-label">
                {label}
            </Label>
            <input id={id} type="checkbox" {...others} className="k-checkbox" />
        </div>
    );
};

const EventDefDialog = ({ onClose, onSubmit, initialValues }: EventDefDialogProps) => {
    return (
        <Dialog title="Event Definition" onClose={onClose} className="event-def-dialog">
            <Form
                initialValues={initialValues}
                onSubmit={onSubmit}
                render={(formRenderProps) => (
                    <FormElement>
                        <FieldWrapper>
                            <Field
                                name="ID"
                                component={TextBoxField}
                                label="ID"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="Caption"
                                component={TextBoxField}
                                label="Caption"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="Verbosity"
                                component={TextBoxField}
                                label="Verbosity"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="Silent"
                                component={CheckboxField}
                                label="Silent"
                                type="checkbox"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="Visible"
                                component={CheckboxField}
                                label="Visible"
                                type="checkbox"
                            />
                        </FieldWrapper>
                        <FieldWrapper>
                            <Field
                                name="Enabled"
                                component={CheckboxField}
                                label="Enabled"
                                type="checkbox"
                            />
                        </FieldWrapper>
                        <DialogActionsBar layout="start">
                            <Button
                                type={"submit"}
                                themeColor={"primary"}
                                disabled={!formRenderProps.allowSubmit}
                                onClick={formRenderProps.onSubmit}
                            >
                                Save
                            </Button>
                            <Button
                                onClick={onClose}
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

export default EventDefDialog;
