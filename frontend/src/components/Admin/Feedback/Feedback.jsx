import React from "react";
import {fetchFeedback} from "../../../store/slices/FeedbackSlice";
import {useDispatch, useSelector} from "react-redux";
import ReactPaginate from "react-paginate";
import style from "./Feedback.module.css"
import {useCookies} from "react-cookie";
import Preloader from "../../Helpers/Preloader/Preloader";
import Admin from "../Admin";
import Erorr404 from "../../Helpers/Errors/Erorr404";

const Feedback = () => {
    const [cookies, ] = useCookies(['isAuth'])
    const {feedbacks, pageSize, count} = useSelector(state => state.feedbacks);
    const dispatch = useDispatch();
    let pageCount = Math.ceil(count / pageSize);

    const handlePageClick = (e) => {
        try {
            dispatch(fetchFeedback({page: e.selected, pageSize}))
        } catch (e) {
            console.log(e);
        }
    }

    React.useEffect(() => {
        try {
            dispatch(fetchFeedback({page: 0, pageSize}))
        } catch (e) {
            console.log(e);
        }

    }, [pageSize]);


    return <div>
        {feedbacks.isFetching === true ? <Preloader/> :
            <div>
                {cookies.isAuth ? <div>
                    <Admin/>
                    {feedbacks.map((feedback, index) => <div key = {index} className={style.block}>
                        <div>Имя: {feedback.name}</div>
                        <div>Почта: {feedback.mail}</div>
                        <div>Сообщение: {feedback.message}</div>
                        <div>Дата: {feedback.date}</div>
                        <div>{feedback.solved ? 'Решено' : 'Не решено'}</div>
                    </div>)}

                    <ReactPaginate
                        breakLabel="..."
                        nextLabel="->"
                        onPageChange={handlePageClick}
                        pageRangeDisplayed={5}
                        pageCount={pageCount}
                        previousLabel="<-"
                        renderOnZeroPageCount={null}

                        pageClassName="page-item"
                        pageLinkClassName="page-link"
                        previousClassName="page-item"
                        previousLinkClassName="page-link"
                        nextClassName="page-item"
                        nextLinkClassName="page-link"
                        breakClassName="page-item"
                        breakLinkClassName="page-link"
                        containerClassName="pagination"
                        activeClassName="active"
                    /></div> : <Erorr404/>}
            </div>
        }
    </div>
}

export default Feedback;
