import React, {useState, useEffect} from "react";
import {NavLink} from "react-router-dom";
import ReactPaginate from "react-paginate";
import {setData} from "../../../store/slices/PublicationsSlice";
import {useDispatch, useSelector} from "react-redux";
import stylePublication from "../../Publications/Publications.module.css";
import style from "./Source.module.css"
import {SourceAPI} from "../../../store/api";
import Preloader from "../../Helpers/Preloader/Preloader";


const SourcePublications = () => {
    const source = useSelector(state => state.source);
    const dispatch = useDispatch();
    const {publications, pageSize, count} = useSelector(state => state.publications);
    let pageCount = Math.ceil(count / pageSize);
    const [isFetching, toggleIsFetching] = useState(false);


    const handlePageClick = (e) => {
        toggleIsFetching(true);
        try {
            const fetchPublications = async () => {
                const res = await SourceAPI.getSourcePageSize(source.id, e.selected, pageSize);
                dispatch(setData(res.data));
                toggleIsFetching(false);
            }
            fetchPublications();
        } catch (e){
            console.log(e)
        }
    }

    useEffect(() => {
        toggleIsFetching(true);
        try {
            const fetchPublications = async () => {
                const res = await SourceAPI.getSourcePageSize(source.id, 0, pageSize);
                dispatch(setData(res.data));
                toggleIsFetching(false);
            }
            fetchPublications();
        } catch (e) {
            console.log(e)
        }

    }, [source.id]);

    return (<div className={style.theme}>
            {isFetching === true ? <Preloader/> :
                <div>
                    <div className={stylePublication.block}>
                        {publications.map((publication, index) => <div key={index}>
                            <div className={stylePublication.blocks}>
                                <div>{publication.publication_type.name}</div>
                                <div>{publication.source.name}</div>
                                <NavLink to={"/publication/" + publication.id}>
                                    <div>{publication.title}</div>
                                </NavLink>
                                <div className={stylePublication.authors}>
                                    <div
                                        className={stylePublication.author}>{publication.publication_authors.map((authors, index) =>
                                        <NavLink key={index} to={"/author/" + authors.author.id}>
                                            {authors.author.surname} {authors.author.name}
                                        </NavLink>
                                    )}</div>
                                </div>
                                <div>{publication.publication_date === null ||
                                publication.publication_date === undefined ? '' :
                                    publication.publication_date.slice(0, 4)}</div>
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
    )
}

export default SourcePublications;
