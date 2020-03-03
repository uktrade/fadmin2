import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const filter = createSlice({
    slice: 'edit',
    initialState: {
        open: false
    },
    reducers: {
        TOGGLE_FILTER: (state, action) => {
            if (state.open) {
                state.open = false
            } else {
                state.open = true
            }
        },
    }
});

export const {
    TOGGLE_FILTER,
} = filter.actions;

export default filter.reducer;
