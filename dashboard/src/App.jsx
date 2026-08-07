import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/common/Sidebar";

import Dashboard from "./pages/Dashboard";
import Sales from "./pages/Sales";
import Inventory from "./pages/Inventory";
import Insights from "./pages/Insights";
import Settings from "./pages/Settings";

import "./styles/sidebar.css";

function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout>
              <Dashboard />
            </Layout>
          }
        />

        <Route
          path="/sales"
          element={
            <Layout>
              <Sales />
            </Layout>
          }
        />

        <Route
          path="/inventory"
          element={
            <Layout>
              <Inventory />
            </Layout>
          }
        />

        <Route
          path="/insights"
          element={
            <Layout>
              <Insights />
            </Layout>
          }
        />

        <Route
          path="/settings"
          element={
            <Layout>
              <Settings />
            </Layout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}