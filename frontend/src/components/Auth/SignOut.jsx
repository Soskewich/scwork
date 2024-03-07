import React from "react";
import {useDispatch} from "react-redux";
import style from "./../Header/Navbar/Navbar.module.css";
import {setIsAuth} from "../../store/slices/SignInSlice";
import {useCookies} from 'react-cookie';
import {DOMAIN, SECURE} from "../../settings.js"


const SignOut = () => {
    const [cookies, setCookies, removeCookies] = useCookies(['isAuth'])
    const dispatch = useDispatch();
    const logout = () => {
        removeCookies('isAuth', {path: '/', domain: DOMAIN, secure: SECURE});
        dispatch(setIsAuth(false));
    }
    return (<div>
            <button className={style.btn} onClick={logout}>Выйти</button>

        </div>
    );
}

export default SignOut;
