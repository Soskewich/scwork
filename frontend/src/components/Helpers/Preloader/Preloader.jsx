import React from "react";
import preloaderDark from "../../../assets/img/preloader.svg"
import preloaderLight from "../../../assets/img/preloader-2.svg"
import {useCookies} from "react-cookie";

const Preloader = () => {
    const [cookiesTheme, _] = useCookies(['theme']);
    return <div>
        {cookiesTheme.theme === "dark" ? <img src={preloaderLight} alt=""/> : <img src={preloaderDark} alt=""/>}
    </div>

}

export default Preloader;
