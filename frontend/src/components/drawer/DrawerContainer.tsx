import React from "react";
import {useNavigate} from "react-router-dom";

import {
    Drawer,
    DrawerContent,
    DrawerItemProps,
    DrawerSelectEvent,
    DrawerItem,
} from "@progress/kendo-react-layout";
import "../../assets/components/drawercontainer.scss";

const items = [
    {title: "Tab1", text: "Event", selected: true, route: "/event"},
    {title: "Tab2", text: "EventDef", route: "/eventdef"},
    {title: "Tab3", text: "Trend", route: "/trend"},
    {title: "Tab4", text: "TrendChart", route: "/trendchart"},
];

const CustomItem = (props: DrawerItemProps) => {
    return (
        <DrawerItem {...props}>
            <div className="item-title">
                {props.title}
            </div>
            <div className="item-text">
                {props.text}
            </div>
        </DrawerItem>
    );
};

const DrawerContainer = ({expanded, children}: {
    expanded: boolean;
    children: React.ReactNode;
}) => {
    const navigate = useNavigate();
    const [selected, setSelected] = React.useState(
        items.findIndex((x) => x.selected === true)
    );

    const onSelect = React.useCallback((e: DrawerSelectEvent) => {
            navigate(e.itemTarget.props.route);
            setSelected(e.itemIndex);
        }, [navigate]
    );

    return (
        <div className="drawer-container">
            <Drawer
                expanded={expanded}
                mode="push"
                mini={true}
                width={175}
                items={items.map((item, index) => ({
                    ...item,
                    selected: index === selected,
                }))}
                onSelect={onSelect}
                item={CustomItem}
            >
                <DrawerContent>
                    {children}
                </DrawerContent>
            </Drawer>
        </div>
    );
};

export default DrawerContainer;