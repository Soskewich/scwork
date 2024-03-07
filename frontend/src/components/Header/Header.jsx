import React from "react";
import style from './Header.module.css'
import Navbar from "./Navbar/Navbar";
import {NavLink} from "react-router-dom";

const Header = () => {
    return <div className={style.header}>
        <div className={style.head}><NavLink to='/'>Science</NavLink></div>
        <Navbar/>
    </div>
}

export default Header;