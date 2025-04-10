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
import "../../styles/features/auth/login.scss";
import { Label } from "@progress/kendo-react-labels";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { useCookies } from "react-cookie";
import { LoadingPanel } from "onyks_shared_kendo";
import { Navigate } from "react-router-dom";
import { axiosInstance, config, host } from "../../lib/apiUtilities";
import { AuthApi, LoginPermissions } from "../../services/api";
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

interface LoginProps {
  setToken: (token: string | null) => void;
  setPermissions: (permissions: string[] | null) => void;
}

export default function Login(props: LoginProps) {
  const authApiRef = React.useRef(new AuthApi(config, host, axiosInstance));

  const [cookies, setCookie] = useCookies([
    "token",
    "permissions",
    "refreshToken",
  ]);
  const [showLoading, setShowLoading] = React.useState<boolean>(false);

  if (cookies.token && cookies.permissions) return <Navigate to="/" />;

  function handleSubmit(dataItem: any) {
    setShowLoading(true);

    authApiRef.current
      .authLoginAuthLoginPost({
        username: dataItem.login,
        password: dataItem.password,
      })
      .then((response: AxiosResponse<LoginPermissions>) => {
        props.setToken(response.data.token);
        if (response.data.permissions)
          props.setPermissions(response.data.permissions);
        setCookie("token", JSON.stringify(response.data.token), {
          expires: 0 as any,
        });
        setCookie("permissions", JSON.stringify(response.data.permissions), {
          expires: 0 as any,
        });
        setCookie("refreshToken", JSON.stringify(response.data.refreshToken), {
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
