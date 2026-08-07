import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import "@fontsource/inter";

import "./styles/global.css";
import "./styles/tables.css";
import "./styles/sidebar.css";


ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);