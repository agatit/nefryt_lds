import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import {Appbar} from "./layouts/Appbar";
import DrawerContainer from "./components/drawer/DrawerContainer";
import EventTab from "./pages/EventTab";
import EventDefTab from "./pages/EventDefTab";
import TrendTab from "./pages/TrendTab";
import TrendChartTab from "./pages/TrendChartTab";

const App = () => {
    const [expanded, setExpanded] = React.useState(true);

    const handleDrawerOpen = React.useCallback(() => {
            setExpanded(!expanded);
        }, [expanded]
    );

    return (
        <BrowserRouter>
            <div className="app-container">
                <Appbar onMenuClick={handleDrawerOpen}/>
                <DrawerContainer expanded={expanded}>
                    <Routes>
                        <Route path="/event" element={<EventTab/>}/>
                        <Route path="/eventdef" element={<EventDefTab/>}/>
                        <Route path="/trend" element={<TrendTab/>}/>
                        <Route path="/trendChart" element={<TrendChartTab/>}/>
                    </Routes>
                </DrawerContainer>
            </div>
        </BrowserRouter>
    );
};

export default App;
