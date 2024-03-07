import {useCallback, useEffect, useState} from "react";
import {useCookies} from "react-cookie";
import {DOMAIN, SECURE} from "../../../settings.js"

const COLOR_THEME = {
    light: "light",
    dark: "dark"
};

export const useColorTheme = () => {
    const [colorTheme, setColorTheme] = useState(COLOR_THEME.light);
    const [cookiesTheme, setCookiesTheme] = useCookies(['theme'])

    const changeColorTheme = useCallback((theme = "") => {
        const currentTheme = theme === "" ? COLOR_THEME.light : theme;
        setColorTheme(currentTheme);
        document.documentElement.setAttribute("data-theme", currentTheme);
    }, []);

    const toggleColorTheme = useCallback(() => {
        if(cookiesTheme.theme !== undefined){
            if (colorTheme === COLOR_THEME.light) {
                changeColorTheme(COLOR_THEME.dark)
                setCookiesTheme('theme', COLOR_THEME.dark, {path: '/', maxAge: 60 * 60 * 24 * 30, domain: DOMAIN, secure: SECURE});
            } else if (colorTheme === COLOR_THEME.dark) {
                changeColorTheme(COLOR_THEME.light);
                setCookiesTheme('theme', COLOR_THEME.light, {path: '/', maxAge: 60 * 60 * 24 * 30, domain: DOMAIN, secure: SECURE});
            }
        }else {
            changeColorTheme("");
            setCookiesTheme('theme', COLOR_THEME.light, {path: '/', maxAge: 60 * 60 * 24 * 30, domain: DOMAIN, secure: SECURE});
        }

    }, [colorTheme, changeColorTheme, cookiesTheme]);

    return {colorTheme, changeColorTheme, toggleColorTheme};
};
