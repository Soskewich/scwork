import React, {useState} from "react";
import Modal from "../../Bugtracker/BugtrackerWindow";
import MergeForm from "./MergeForm";
import style from "./Merge.module.css"

const MergeButton = (props) => {

    const [isModal, setModal] = useState(false);

    return(
        <div>
            <button className={style.button} onClick={() => setModal(true)}>Слить автора</button>
            {isModal ? <Modal visible={true} active={isModal} setActive={setModal}>
                <MergeForm authorId = {props.authorId}/>
            </Modal> : null}
        </div>
    )
}

export default MergeButton;