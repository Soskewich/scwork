import React, {useEffect, useState} from "react";
import {NavLink} from "react-router-dom";
import ReactPaginate from "react-paginate";
import {setData} from "../../../store/slices/PublicationsSlice";
import {useDispatch, useSelector} from "react-redux";
import style from "../../Publications/Publications.module.css";
import {AuthorAPI} from "../../../store/api";
import Preloader from "../../Helpers/Preloader/Preloader";


const AuthorsPublications = () => {
    const author = useSelector(state => state.author);
    const dispatch = useDispatch();
    const {publications, pageSize, count} = useSelector(state => state.publications);
    let pageCount = Math.ceil(count / pageSize);
    const [isFetching, toggleIsFetching] = useState(false);


    const handlePageClick = (e) => {
        toggleIsFetching(true);
        try {
            const fetchPublications = async () => {
                const res = await AuthorAPI.getAuthorPublication(author.id, e.selected, pageSize);
                dispatch(setData(res.data));
                toggleIsFetching(false);
            }
            fetchPublications();
        } catch (e) {
            console.log(e);
        }
    }

    useEffect(() => {
        toggleIsFetching(true);
        try {
            const fetchPublications = async () => {
                const res = await AuthorAPI.getAuthorPublication(author.id, 0, pageSize);
                dispatch(setData(res.data));
                toggleIsFetching(false);
            }
            fetchPublications();
        } catch (e) {
            console.log(e);
        }
    }, [author.id]);

    return <div>
        {isFetching === true ? <Preloader/> :
            <div>
                <div className={style.block}>
                    {publications.map((authorsPublication, index) => <div key={index}>
                        <div className={style.blocks}>
                            <div>{authorsPublication.publication_type.name}</div>
                            <div><NavLink
                                to={'/source/' + authorsPublication.source.id}>
                                {authorsPublication.source.name}</NavLink>
                            </div>
                            <NavLink to={"/publication/" + authorsPublication.id}>
                                <div>{authorsPublication.title}</div>
                            </NavLink>
                            <div className={style.authors}>
                                <div className={style.author}>
                                    {authorsPublication.publication_authors.map((authors,index) =>
                                    <NavLink key={index} to={"/author/" + authors.author.id}>
                                        {authors.author.surname} {authors.author.name}
                                    </NavLink>
                                )}</div>
                            </div>
                            <div>{authorsPublication.publication_date === null ||
                            authorsPublication.publication_date === undefined ? '' :
                                authorsPublication.publication_date.slice(0, 4)}</div>
                        </div>
                    </div>)}
                </div>
            </div>
        }
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
        />
    </div>
}

export default AuthorsPublications;