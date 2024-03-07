import React, {useState} from 'react';
import style from './Nioktrs.module.css';
import styleSearch from '../Helpers/Search/Search.module.css';
import {useDispatch, useSelector} from "react-redux";
import {fetchNioktrs, fetchNioktrsSearch} from "../../store/slices/NioktrsSlice";
import ReactPaginate from "react-paginate";
import {NavLink} from "react-router-dom";
import {useDebounce} from "use-debounce";
import Preloader from "../Helpers/Preloader/Preloader";
import NioktrFilterSize from "../Helpers/Filters/NioktrFilterSize";
// PublicationFilterSize Посмотреть и переделать?
// import PublicationFilterSize from "../Helpers/Filters/PublicationFilterSize";


const Nioktrs = () => {
    const {nioktrs, pageSize, count, isFetching, data} = useSelector(state => state.nioktrs);
    const dispatch = useDispatch();
    let pageCount = Math.ceil(count / pageSize);
    const [search, setSearch] = useState('');
    const debouncedSearch = useDebounce(search, 500);
    let keywords = [];
    // console.log("nioktrs",nioktrs[0].keyword_nioktrs[0].keyword.keyword)

    const onSearchChange = (e) => {
        const {value} = e.target
        setSearch(value)
    }

    const handlePageClick = (e) => {
        dispatch(fetchNioktrsSearch({search, author_id: data.authorName, from_date: data.beforeTime,
            to_date: data.afterTime, page: e.selected, pageSize}));
    }

    React.useEffect(() => {
        if (debouncedSearch[0] !== '') {
            dispatch(fetchNioktrsSearch({search, author_id: data.authorName,
                from_date: data.beforeTime, to_date: data.afterTime, page: 0, pageSize}))
        } else {
            dispatch(fetchNioktrs({page: 0, pageSize}))
        }
    }, [pageSize, debouncedSearch[0]]);

    return (<div className={style.container}>
            <input className={styleSearch.search} placeholder='Поиск' type="text" value={search}
                   onChange={onSearchChange}/>
            <div className={style.blockCount}>
                <div>Количество найденных <br></br>НИОКТР: <span className={style.count}>{count}</span></div>
            </div>
            <NioktrFilterSize min={20} mid={40} max={80}/>
            {isFetching === true ? <Preloader/> :
                <div className={style.block}>
                    {nioktrs.map((item, index) => <div key={index}>
                        <div className={style.blocks}>
                            <NavLink to={"/nioktr/" + item.id}>
                                <div>{item.title}</div>
                            </NavLink>

                            <div>
                                Регистрационный номер: {item.registration_number}
                            </div>
                            <div >
                                Руководитель работы:
                             
                                 <NavLink to={"/author/" + item.work_supervisor.id}>
                                     &nbsp;{item.work_supervisor.surname} {item.work_supervisor.name} {item.work_supervisor.patronymic}
                                 </NavLink>

                            </div>

                            <div className={style.keyword_nioktrs}>
                                Ключевые слова:
                                <div className={style.keyword_nioktr}>
                                    {item.keyword_nioktrs.map((wordItem, index) =>
                                        // nioktrs[0].keyword_nioktrs[0].keyword.keyword

                                        <span> {wordItem.keyword.keyword}</span>

                                    )}
                                </div>
                            </div>

                            <div>
                                {item.nioktr_date === null ||
                                item.nioktr_date === undefined ? '' :
                                    item.nioktr_date.slice(0, 4)}
                            </div>
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

export default Nioktrs;

