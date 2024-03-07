import React, {useState} from 'react';
import style from './Publications.module.css';
import styleSearch from '../Helpers/Search/Search.module.css';
import {useDispatch, useSelector} from "react-redux";
import {fetchPublications, fetchPublicationsSearch} from "../../store/slices/PublicationsSlice";
import ReactPaginate from "react-paginate";
import {NavLink} from "react-router-dom";
import PublicationFilterSize from "../Helpers/Filters/PublicationFilterSize";
import {useDebounce} from "use-debounce";
import Preloader from "../Helpers/Preloader/Preloader";

const Publications = () => {
    const {publications, pageSize, count, isFetching, data} = useSelector(state => state.publications);
    const dispatch = useDispatch();
    let pageCount = Math.ceil(count / pageSize);
    const [search, setSearch] = useState('');
    const debouncedSearch = useDebounce(search, 500);

    const onSearchChange = (e) => {
        const {value} = e.target
        setSearch(value)
    }

    const handlePageClick = (e) => {
        dispatch(fetchPublicationsSearch({search,publication_type_id: data.publicationType,author_id: data.authorName,
            source_rating_type_id: data.SourceRating, department: data.department, from_date: data.beforeTime,
            to_date: data.afterTime, page: e.selected, pageSize}));
    }

    React.useEffect(() => {
        if (debouncedSearch[0] !== '') {
            dispatch(fetchPublicationsSearch({search,publication_type_id: data.publicationType,author_id: data.authorName,
                source_rating_type_id: data.SourceRating, department: data.department,
                from_date: data.beforeTime, to_date: data.afterTime, page: 0, pageSize}))
        } else {
            dispatch(fetchPublications({page: 0, pageSize}))
        }
    }, [pageSize, debouncedSearch[0]]);

    return (<div className={style.container}>
            <input className={styleSearch.search} placeholder='Поиск' type="text" value={search}
                   onChange={onSearchChange}/>
            <div className={style.blockCount}>
                <div>Количество найденных <br></br>публикаций: <span className={style.count}>{count}</span></div>
            </div>
            <PublicationFilterSize min={20} mid={40} max={80}/>
            {isFetching === true ? <Preloader/> :
                <div className={style.block}>
                    {publications.map((publications, index) => <div key={index}>
                        <div className={style.blocks}>
                            <div>
                                {publications.publication_type.name}</div>
                            <div>
                                <NavLink to={'/source/' + publications.source.id}>
                                    {publications.source.name}
                                </NavLink>
                            </div>
                            <NavLink to={"/publication/" + publications.id}>
                                <div>{publications.title}</div>
                            </NavLink>
                            <div className={style.authors}>
                                <div className={style.author}>
                                    {publications.publication_authors.map((authors, index) =>
                                        <NavLink key={index}
                                                 to={'/author/' + authors.author.id}>
                                            {authors.author.surname} {authors.author.name}
                                        </NavLink>
                                    )}</div>
                            </div>
                            <div>
                                {publications.publication_date === null ||
                                publications.publication_date === undefined ? '' :
                                    publications.publication_date.slice(0, 4)}</div>
                        </div>
                    </div>)}
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
    );
};

export default Publications;

