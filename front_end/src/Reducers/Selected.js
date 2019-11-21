import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const selected = createSlice({
    slice: 'select',
    initialState: {
        selectedRow: null
    },
    reducers: {
        SET_SELECTED_ROW: (state, action) => {
            state.selectedRow = action.payload.selectedRow
        },
    }
});

export const {
    SET_SELECTED_ROW,
} = selected.actions;

export default selected.reducer;
