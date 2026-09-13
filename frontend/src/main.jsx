import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router-dom";

import "./index.css";
import router from "./routes/Router";
import { store } from "./store/store";
import ERPDataBootstrap from "./components/system/ERPDataBootstrap";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <ERPDataBootstrap><RouterProvider router={router} /></ERPDataBootstrap>
    </Provider>
  </StrictMode>
);
