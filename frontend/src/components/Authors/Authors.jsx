import React, {useState} from 'react';
import {NavLink} from "react-router-dom";
import style from "./Authors.module.css";
import styleSearch from '../Helpers/Search/Search.module.css';
import ReactPaginate from "react-paginate";
import Paginator from '../Helpers/Paginator/Paginator.css';
import {useDispatch, useSelector} from "react-redux";
import {fetchAuthor, fetchAuthorSearch, setData, setSize} from "../../store/slices/AuthorsSlice";
import {useDebounce} from "use-debounce";
import Preloader from "../Helpers/Preloader/Preloader";

const Authors = () => {

    const {authors, pageSize, count, isFetching} = useSelector(state => state.authors);
    const dispatch = useDispatch();
    let pageCount = Math.ceil(count / pageSize);
    const [search, setSearch] = useState('');
    const debouncedSearch = useDebounce(search, 500);

    const onSearchChange = (e) => {
        const {value} = e.target
        setSearch(value)
    }

    const handlePageClick = (e) => {
        try {
            dispatch(fetchAuthorSearch({search, page: e.selected, pageSize}))
        } catch (e) {
            console.log(e);
        }
    }

    React.useEffect(() => {
        try {
            if (debouncedSearch[0] !== '') {
                dispatch(fetchAuthorSearch({search, page: 0, pageSize}))
            } else {
                dispatch(fetchAuthor({page: 0, pageSize}))
            }
        } catch (e) {
            console.log(e);
        }
    }, [pageSize, debouncedSearch[0]]);

    return (<div className={style.container}>
            <input className={styleSearch.search} placeholder='Поиск' type="text" value={search}
                   onChange={onSearchChange}/>
            <div className={style.blockCount}>
                <div>Количество найденных <br></br>авторов: <span className={style.count}>{count}</span></div>
            </div>
            <div className={style.size}>
                Отображать по:
                <ul>
                    <li onClick={() => {
                        dispatch(setSize(30));
                    }}>30
                    </li>
                    <li onClick={() => {
                        dispatch(setSize(60));
                    }}>60
                    </li>
                    <li onClick={() => {
                        dispatch(setSize(90));
                    }}>90
                    </li>
                </ul>
            </div>
            {isFetching === true ? <Preloader/> :
                <div className={style.block}>
                    <ul className={style.ulAuthors}>
                        {authors.map((author, index) =>
                            <li key={index}>
                                <NavLink to={'/author/' + author.id}>
                                    {author.surname} {author.name} {author.patronymic}
                                </NavLink>
                            </li>
                        )}
                    </ul>
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

export default Authors;
