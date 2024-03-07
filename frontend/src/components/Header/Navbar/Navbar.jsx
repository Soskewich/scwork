import React, {useState, useEffect} from "react";
import style from "./Navbar.module.css"
import {NavLink} from "react-router-dom";
import BugTracker from "../../Bugtracker/Bugtracker";
import {useColorTheme} from "../../Helpers/Theme/Theme";
import theme from "../../../assets/img/theme-dark.png"
import {useSelector} from "react-redux";
import SignOut from "../../Auth/SignOut";
import {useCookies} from "react-cookie";

const Navbar = () => {

    const [cookies, , ] = useCookies(['isAuth']);
    const [Active, setActive] = useState(false);
    const toggle = () => {
        setActive(!Active);
    }
    const [cookiesTheme, _] = useCookies(['theme']);
    const {colorTheme, toggleColorTheme} = useColorTheme();

    useEffect(() => {
        if (cookiesTheme.theme !== colorTheme) {
            toggleColorTheme();
        }
    },[colorTheme])
    const onChangeTheme = () => {
        document.getElementById("app-wrapper").style.transition = '.5s ease-in-out';
        toggleColorTheme();
    };

    useEffect(() => {
        if (Active === true && window.innerWidth < 991) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
    }, [Active]);


    return (
        <div className={style.appWrapperNavbar}>
            <div className={style.burger} onClick={toggle}>
                <span></span>
            </div>
            <div className={Active ? style.back : null}>
                <div className={Active ? style.menu + " " + style.active : style.menu}>


                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/publication"
                                 className={navData => navData.isActive ? style.active : null}>Публикации</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/author"
                                 className={navData => navData.isActive ? style.active : null}>Персоналии</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/source"
                                 className={navData => navData.isActive ? style.active : null}>Источники</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/analysis"
                                 className={navData => navData.isActive ? style.active : null}>Аналитика</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/nioktr"
                                 className={navData => navData.isActive ? style.active : null}>НИОКТР</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/rid"
                                 className={navData => navData.isActive ? style.active : null}>РИД</NavLink>
                    </div>
                    {cookies.isAuth? <div className={style.item} onClick={toggle}>
                        <NavLink to="/admin/unconfirmed">Администратор</NavLink>
                    </div> : null}
                    <div className={style.item}>
                        <BugTracker/>
                    </div>
                    <div className={style.item} onClick={onChangeTheme}>
                        <img src={theme} className={style.image}/>
                    </div>
                    <div>
                        {cookies.isAuth? <div onClick={toggle}><SignOut/></div> : <NavLink to="/login">
                                <button className={style.btn} onClick={toggle}>Войти</button>
                            </NavLink>
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Navbar;