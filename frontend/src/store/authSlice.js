import { createSlice } from "@reduxjs/toolkit";

import { loginUser } from "./authThunk";

const storedUser = (() => {
    try { return JSON.parse(localStorage.getItem("user") || "null"); } catch { return null; }
})();

const initialState = {
    loading: false,
    error: null,
    user: storedUser,
    token: localStorage.getItem("accessToken"),
    isAuthenticated: Boolean(localStorage.getItem("accessToken")),
};

const authSlice = createSlice({

    name: "auth",

    initialState,

    reducers: {

        logout(state) {

            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            localStorage.removeItem("user");
        }

    },

    extraReducers: builder => {

        builder

            .addCase(loginUser.pending, state => {

                state.loading = true;
                state.error = null;

            })

            .addCase(loginUser.fulfilled, (state, action) => {

                state.loading = false;

                state.user = action.payload.user;

                state.token = action.payload.token;

                state.isAuthenticated = true;

            })

            .addCase(loginUser.rejected, (state, action) => {

                state.loading = false;

                state.error = action.payload?.message;

            });

    }

});

export const {

    logout

} = authSlice.actions;

export default authSlice.reducer;