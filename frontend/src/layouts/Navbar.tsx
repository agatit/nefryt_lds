import React from "react";
import {
  AppBar,
  AppBarSection,
  AppBarSpacer,
} from "@progress/kendo-react-layout";
import "../styles/layouts/navbar.scss";
import { Typography } from "@progress/kendo-react-common";
import { Switch, SwitchChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";

const companyPageLink: string = "https://www.agatit.pl";
const logoImage: string = "/img/Agat It Logo.png";

export interface NavbarProps {
  title?: string;
  useMockup?: boolean;
  handleOnUseMockupChange?: (value: SwitchChangeEvent) => void;
}

const Navbar = React.memo(function Navbar({
  title,
  useMockup,
  handleOnUseMockupChange,
}: NavbarProps) {
  return (
    <React.Fragment>
      <AppBar themeColor="inherit">
        <a href={companyPageLink}>
          <AppBarSection className="navbar-logo">
            <img src={logoImage} id="logo" alt="Agat IT Onyks OWL logo" />
          </AppBarSection>
        </a>

        <AppBarSection className="navbar-title">
          <Typography.h2 style={{ marginBottom: 0 }} fontWeight="bold">
            {title ?? "Onyks OWL"}
          </Typography.h2>
        </AppBarSection>

        <AppBarSpacer />

        {import.meta.env.VITE_ALLOW_MOCKUP == "true" && (
          <AppBarSection className="mockup-switch-section">
            <Label>Use Mockup Data</Label>
            <Switch
              className="mockup-switch"
              value={useMockup}
              onChange={handleOnUseMockupChange}
              onLabel={"Mockup"}
              offLabel={"Backend"}
            />
          </AppBarSection>
        )}
      </AppBar>
    </React.Fragment>
  );
});

export default Navbar;
