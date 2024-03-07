import React, {useState} from "react";
import {useDispatch} from "react-redux";
import style from "./NioktrFilter.module.css";
import {setSize} from "../../../store/slices/NioktrsSlice";
import NioktrFilter from "./NioktrFilter";


const NioktrFilterSize = (props) => {
    const [seeFiltered, setSeeFiltered] = useState(false);
    const dispatch = useDispatch();

    const [Active, setActive] = useState(false);

    const toggle = () => {
        setActive(!Active);
    }

    return <div className={style.container}>
        <div className={style.burger} onClick={toggle}>
            <span></span>
        </div>
        <div className={Active ? style.menu + " " + style.active : style.menu}>
            <div onClick={() => {
                if (seeFiltered === true) setSeeFiltered(false)
            }}>
                <div className={style.size}>
                    Отображать по:
                    <ul>
                        <li onClick={() => {
                            dispatch(setSize(props.min));
                        }}>{props.min}
                        </li>
                        <li onClick={() => {
                            dispatch(setSize(props.mid));
                        }}>{props.mid}
                        </li>
                        <li onClick={() => {
                            dispatch(setSize(props.max));
                        }}>{props.max}
                        </li>
                    </ul>
                </div>
                <div>
                    <NioktrFilter/>
                </div>
            </div>
        </div>
    </div>
}

export default NioktrFilterSize;
