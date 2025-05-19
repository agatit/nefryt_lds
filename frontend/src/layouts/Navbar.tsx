import React from "react";
import {
  AppBar,
  AppBarSection,
  AppBarSpacer,
} from "@progress/kendo-react-layout";
import "../styles/layouts/navbar.scss";
import { Typography } from "@progress/kendo-react-common";

const companyPageLink: string = "https://www.agatit.pl";
const logoImage: string = "/img/Agat It Logo.png";

export interface NavbarProps {
  title?: string;
}

export default function Navbar(props: NavbarProps) {
  return (
    <React.Fragment>
      <AppBar themeColor="inherit">
        <a href={companyPageLink}>
          <AppBarSection className="navbar-logo">
            <img src={logoImage} id="logo" alt="Agat IT Onyks OWL logo" />
          </AppBarSection>
        </a>

        <AppBarSection className="navbar-title">
          <Typography.h2 fontWeight="bold">
            {props.title ? props.title : "Onyks OWL"}
          </Typography.h2>
        </AppBarSection>

        <AppBarSpacer />
      </AppBar>
    </React.Fragment>
  );
}
