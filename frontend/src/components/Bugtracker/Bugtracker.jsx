import React, {useState, useRef} from "react";
import bugtracker from "./../../assets/img/bagtracker.png"
import style from "./Bugtracker.module.css"
import Modal from "./BugtrackerWindow";
import ReCAPTCHA from "react-google-recaptcha";
import axios from "axios";
import {REACT_APP_SITE_KEY} from "../../settings"

const BugTracker = () => {

    const [isModal, setModal] = useState(false);
    const captchaRef = useRef(null);


    const handleSubmit = (e) => {
        setModal(false)
        e.preventDefault();
        const message = document.getElementById("message").value;
        const token = captchaRef.current.getValue();
        captchaRef.current.reset();
        const name = document.getElementsByTagName("input")[0].value;
        const mail = document.getElementsByTagName("input")[1].value;

        const postToken = async () => {
            const res = await axios.post("/api/feedback", {
                token: token,
                feedback: {name: name, mail: mail, message: message}
            });
        }
        postToken();
    }

    return (<div>
            <img src={bugtracker} className={style.image} onClick={() => setModal(true)} alt=''/>
            {isModal ? <Modal visible={true} active={isModal} setActive={setModal}>
                <form onSubmit={handleSubmit} className={style.form}>
                    <div className={style.title}>Форма обратной связи</div>
                    <div className={style.line}>
                        <div>
                            <div>Имя</div>
                            <input type="text" name="name" className={style.input}/>
                        </div>
                        <div>
                            <div>Почта</div>
                            <input type="email" name="mail" className={style.input}/>
                        </div>
                    </div>
                    <div>Сообщение</div>
                    <textarea className={style.input} id="message" name="message"/>
                    <ReCAPTCHA
                        sitekey={REACT_APP_SITE_KEY}
                        ref={captchaRef}
                    />
                    <div><input className={style.input} type="submit" value="Отправить"/></div>
                </form>
            </Modal> : null}
        </div>
    );
}

export default BugTracker;
