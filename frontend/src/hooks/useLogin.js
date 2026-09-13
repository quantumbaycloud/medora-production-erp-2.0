import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { loginUser } from "../store/authThunk";

export default function useLogin() {

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const {
        loading,
        error,
        user,
        isAuthenticated
    } = useSelector(state => state.auth);

    const login = async (credentials) => {

        const result = await dispatch(
            loginUser(credentials)
        );

        if (loginUser.fulfilled.match(result)) {

            navigate("/dashboard");

        }

        return result;

    };

    return {

        login,
        loading,
        error,
        user,
        isAuthenticated

    };

}