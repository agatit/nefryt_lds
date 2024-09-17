import React from "react";
import {
    AppBar,
    AppBarSection,
    AppBarSpacer,
} from "@progress/kendo-react-layout";
import { Button } from "@progress/kendo-react-buttons";
import "../assets/layouts/appbar.scss"
import {menuIcon} from "@progress/kendo-svg-icons";

export function Appbar({onMenuClick}: {onMenuClick: () => void}) {

    return (
        <React.Fragment>
            <AppBar className="k-appbar">
                <AppBarSection>
                    <Button
                        className="menu-icon"
                        svgIcon={menuIcon}
                        fillMode="flat"
                        onClick={onMenuClick}
                    />
                </AppBarSection>
                <AppBarSpacer />
                <AppBarSection>
                    <h1 className="title">KendoTest</h1>
                </AppBarSection>
                <AppBarSpacer />
                <AppBarSection></AppBarSection>
            </AppBar>
        </React.Fragment>
    )
}