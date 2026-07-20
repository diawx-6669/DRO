import { createSlice } from "@reduxjs/toolkit";

const binsSlice = createSlice({
  name: "bins",
  initialState: { items: [], selectedId: null },
  reducers: {
    setBins(state, action) {
      state.items = action.payload;
    },
    selectBin(state, action) {
      state.selectedId = action.payload;
    },
  },
});

export const { setBins, selectBin } = binsSlice.actions;
export default binsSlice.reducer;
