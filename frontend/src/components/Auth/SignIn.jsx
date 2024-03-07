import React from "react";
import {useForm} from "react-hook-form";
import {useDispatch, useSelector} from "react-redux";
import {setIsAuth, setError} from "../../store/slices/SignInSlice";
import {postSignIn} from "../../store/api";
import {Navigate} from "react-router-dom";
import {useCookies} from "react-cookie";
import style from "./SignIn.module.css"
import {DOMAIN, SECURE} from "../../settings.js"

const SignIn = () => {

    const {error} = useSelector(state => state.signIn)
    const {register, formState: {errors}, handleSubmit} = useForm();
    const dispatch = useDispatch();
    const [cookies, setCookies] = useCookies(['isAuth'])

    const onSubmit = (data) => {

        const postUser = async () => {
            try {
                const res = await postSignIn(data);
                dispatch(setError(res.status));
                if (res.status === 200) {
                    dispatch(setIsAuth(true));
                data.checkbox === true ? setCookies('isAuth', true, {
                        path: '/',
                        maxAge: 60 * 24 * 30,
                        domain: DOMAIN,
                        secure: SECURE
                    }) :
                    setCookies('isAuth', true, {path: '/', maxAge: 60*60*24, domain: DOMAIN, secure: SECURE})
                }
                if(res.status === 403){
                    dispatch(setError(403))
                }
            } catch (e) {
                dispatch(setError(e.response.status));
            }

        }
        postUser();
    };

    return (<div>
            {cookies.isAuth? <Navigate to = "/publication"/> :
                <div>
                    {error === 403? <p className={style.error}>Неверный логин или пароль!</p>:null}
                    <form onSubmit={handleSubmit(onSubmit)} className={style.form}>
                        <div className={style.block}>
                            <input className={style.input} {...register("username", {required: true})}
                                   aria-invalid={errors.username ? "true" : "false"}/>
                            {errors.username?.type === 'required' && <p role="alert">Login is required</p>}
                            <input className={style.input} type={"password"} {...register("password", {required: true})}
                                   aria-invalid={errors.password ? "true" : "false"}/>
                            {errors.password?.type === 'required' && <p role="alert">Password is required</p>}
                            <div>
                                <input className={style.input} type={"checkbox"}
                                       {...register("checkbox")}/> Запомнить меня
                            </div>
                            <input className={style.input} type="submit"/>
                        </div>
                    </form>
                </div>
            }
        </div>
    );
}

export default SignIn;
