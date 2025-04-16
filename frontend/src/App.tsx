import React from "react";
import "./App.scss";
import Navbar from "./layouts/Navbar";
import { Route, Routes, useLocation } from "react-router-dom";
import { LoadingPanel } from "onyks_shared_kendo";
import { useTranslation } from "react-i18next";
import Login from "./features/auth/login";
import LDS from "./features/lds/LDS";
import { NavbarContextProvider } from "./contexts/navbarContext";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  const { t } = useTranslation(["common", "titles"]);
  const { pathname } = useLocation();

  // Navbar stuff if any
  const [title, setTitle] = React.useState<string>(t("titles:" + pathname));

  return (
    <div className="App">
      <Navbar title={title} />
      <React.Suspense fallback={<LoadingPanel querySelectorString=".App" />}>
        <NavbarContextProvider setTitle={setTitle}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/*"
              element={
                <PrivateRoute>
                  <LDS />
                </PrivateRoute>
              }
            />
          </Routes>
        </NavbarContextProvider>
      </React.Suspense>
    </div>
  );
}

export default App;
