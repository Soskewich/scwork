import React from "react";
import {useParams} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {fetchPublication} from "../../../store/slices/PublicationSlice";
import style from "./Publication.module.css"
import {NavLink} from "react-router-dom";

import Preloader from "../../Helpers/Preloader/Preloader";

const Publication = () => {
    const params = useParams();
    const dispatch = useDispatch();
    const publication = useSelector(state => state.publication);
    const keywords = [];

    React.useEffect(() => {
        dispatch(fetchPublication(params.id))
    }, [])

    return (<div className={style.theme}>
            {publication.isFetching === true ? <Preloader/> :
                <div>
                    <div className={style.block}>
                        <div>{publication.publication_type.name}</div>
                        <div><NavLink to={'/source/' + publication.source.id}>{publication.source.name}</NavLink></div>
                    </div>
                    <div className={style.block}>
                        <div>{publication.title}</div>
                        <div>{publication.publication_date}</div>
                    </div>
                    <div className={style.block}>
                        Авторы: <div>{publication.publication_authors.map((authorPublication, index) =>
                        <div key={index}>
                            <NavLink
                                to={'/author/' + authorPublication.author.id}>{authorPublication.author.surname} {authorPublication.author.name} {authorPublication.author.patronymic}</NavLink>
                            {authorPublication.author_publication_organizations.map((organization, index) =>
                                <div key = {index} className={style.organization}>
                                &nbsp;({organization.organization.name}{organization.organization.country === null ?
                                "" : ", "}
                                {organization.organization.country}{organization.organization.city === null ?
                                "" : ", "}{organization.organization.city})
                            </div>)}
                        </div>)}</div>
                    </div>
                    <div className={style.block}>
                        Аннотация: <div>{publication.abstract}</div>
                    </div>
                    <div className={style.block}>
                        Ключевые слова:
                        {publication.keyword_publications.map(word => {
                                keywords.push(word.keyword.keyword)
                            }
                        )}
                        <div>{keywords.join(", ")}</div>
                    </div>
                    <div className={style.block}>
                        <div>{publication.publication_links.map((links, index) => <div key = {index}>
                            {links.publication_link_type.name}: {links.publication_link_type.name === "DOI" ?
                            <a href={"https://www.doi.org/" + links.link} target="_blank">{links.link}</a> :
                            <a href={links.link} target="_blank">{links.link}</a>}
                        </div>)
                        }</div>
                    </div>
                </div>
            }
        </div>
    )
};

export default Publication;
