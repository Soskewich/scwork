import React, {useState} from "react";
import {NavLink} from "react-router-dom";
import style from "./Admin.module.css";

const Admin = () => {
    const [Active, setActive] = useState(false);
    const toggle = () => {
        setActive(!Active);
    }

    return (
        <div className={style.AdminWrapper}>
            <div className={style.burger} onClick={toggle}>
                <span></span>
            </div>
            <div className={Active ? style.menu + " " + style.active : style.menu}>
                <div className={style.menuItems}>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to = "/admin/unconfirmed">Список неподтвержденных авторов университета</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/admin/feedbacks">Сообщения пользователей</NavLink>
                    </div>
                    <div className={style.item} onClick={toggle}>
                        <NavLink to="/admin/upload">Загрузка данных</NavLink>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Admin;