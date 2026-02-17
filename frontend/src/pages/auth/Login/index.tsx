import {
  Field,
  FieldRenderProps,
  FieldWrapper,
  Form,
  FormElement,
  FormRenderProps,
} from "@progress/kendo-react-form";
import { Card, CardBody } from "@progress/kendo-react-layout";
import React from "react";
import "./login.scss";
import { Label } from "@progress/kendo-react-labels";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { useCookies } from "react-cookie";
import { LoadingPanel } from "onyks_shared_kendo";
import { Navigate } from "react-router-dom";
import { axiosInstance, config, host } from "../../../lib/apiUtilities";
import { AuthApi, LoginPermissions } from "../../../services/api";
import { AxiosResponse } from "axios";

function LoginField(props: FieldRenderProps) {
  const { validationMessage, visited, label, id, valid, ...others } = props;

  return (
    <FieldWrapper>
      <Label editorId={id}>{label}</Label>
      <Input type="text" id={id} {...others} />
    </FieldWrapper>
  );
}

function PasswordField(props: FieldRenderProps) {
  const { validationMessage, visited, label, id, valid, ...others } = props;

  return (
    <FieldWrapper>
      <Label editorId={id}>{label}</Label>
      <Input type="password" id={id} {...others} />
    </FieldWrapper>
  );
}

export default function Login() {
  const authApiRef = React.useRef(new AuthApi(config, host, axiosInstance));

  const [cookies, setCookie] = useCookies(["auth"]);
  const [showLoading, setShowLoading] = React.useState<boolean>(false);

  if (typeof cookies.auth !== "undefined") return <Navigate to="/" />;

  function handleSubmit(dataItem: any) {
    setShowLoading(true);

    authApiRef.current
      .authLoginAuthLoginPost({
        username: dataItem.login,
        password: dataItem.password,
      })
      .then((response: AxiosResponse<LoginPermissions>) => {
        setCookie("auth", JSON.stringify(response.data), {
          expires: 0 as any,
        });
      });
  }

  return (
    <main className="login-view gradient-background under-appbar-height">
      <Card>
        <CardBody className="test">
          <Form
            onSubmit={handleSubmit}
            render={(formRenderProps: FormRenderProps) => (
              <FormElement>
                <Field
                  id="login"
                  name="login"
                  label="Login"
                  component={LoginField}
                />
                <Field
                  id="password"
                  name="password"
                  label="Hasło"
                  component={PasswordField}
                />
                <Button
                  themeColor={"primary"}
                  type="submit"
                  className="submit-button"
                >
                  Zaloguj
                </Button>
              </FormElement>
            )}
          />
        </CardBody>
      </Card>
      {showLoading && <LoadingPanel querySelectorString=".App" />}
    </main>
  );
}
