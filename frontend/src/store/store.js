import { configureStore } from "@reduxjs/toolkit";

import binsReducer from "./binsSlice.js";

export const store = configureStore({
  reducer: {
    bins: binsReducer,
  },
});
