import React from "react";
import Admin from "../Admin";
import {useForm} from "react-hook-form";
import {useDispatch, useSelector} from "react-redux";
import Preloader from "../../Helpers/Preloader/Preloader";
import Error404 from "../../Helpers/Errors/Erorr404";
import MergeForm from "./MergeForm";
import {useCookies} from "react-cookie";

const Merge = () => {
    const {register, formState: {errors}, handleSubmit} = useForm();
    const {authors, count} = useSelector(state => state.authors);
    const authorConfirmed = useSelector(state => state.authorsConfirmedFalse);
    const [cookies, ] = useCookies(['isAuth'])


    return (
        <div>
            {cookies.isAuth ?
            <div>
                {authorConfirmed.isFetching === true && authors.isFetching === true ? <Preloader/> :
                    <div>
                        <Admin/>
                       <MergeForm/>
                    </div>
                }
            </div> : <Error404/>}
        </div>
    )
}

export default Merge;