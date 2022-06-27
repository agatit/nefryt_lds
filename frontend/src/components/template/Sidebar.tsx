import React from 'react';
import {ChevronLeftOutlined, Menu } from "@material-ui/icons"
import { Divider, Drawer, IconButton, Toolbar } from "@material-ui/core"

import { SidebarParams } from "./type";
import { NestedList } from "./ListItem";


export const Sidebar: React.FC<SidebarParams> = (p) => {
    return (
        <Drawer className={p.styles.drawer} anchor="left" open={p.is_open} classes={{paper:p.styles.drawerPaper}}>
            <div className={p.styles.drawerHeader + ' ' + p.styles.sidebar} >
                <p className={p.styles.sidebarTitle}>NefrytLDS</p>
                <IconButton className={p.styles.sidebarRightButton} onClick={p.handleDrawer}>
                    <ChevronLeftOutlined />
                </IconButton>
                <Divider/>
            </div>
            <Divider/>
            <NestedList/>
        </Drawer>
    )
}