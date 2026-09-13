import { createAsyncThunk } from "@reduxjs/toolkit";

import authService from "./authService";

export const loginUser = createAsyncThunk(

    "auth/login",

    async (credentials, thunkAPI) => {

        try {

            const response =
                await authService.login(credentials);

            const data = response.data;
            return {
                ...data,
                token: data.access_token,
                user: data.user,
            };

        }

        catch (error) {

            return thunkAPI.rejectWithValue(

                error.response?.data ||

                {

                    message: "Login failed"

                }

            );

        }

    }

);