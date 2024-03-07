import React, {useEffect} from "react";
import './App.css';
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import {Route, Routes} from "react-router-dom";
import Authors from "./components/Authors/Authors";
import Author from "./components/Authors/Author/Author";
import Publications from "./components/Publications/Publications";
import SignIn from "./components/Auth/SignIn";
import Publication from "./components/Publications/Publication/Publication";
import Sources from "./components/Sources/Sources";
import Source from "./components/Sources/Source/Source";
import AuthorsPublications from "./components/Authors/Author/AuthorsPublications";
import Feedback from "./components/Admin/Feedback/Feedback";
import {useCookies, withCookies} from 'react-cookie';
import Error404 from "./components/Helpers/Errors/Erorr404";
import {setIsAuth} from "./store/slices/SignInSlice";
import {useDispatch, useSelector} from "react-redux";
import {useColorTheme} from "./components/Helpers/Theme/Theme";
import UploadDate from "./components/Admin/UploadDate/UploadDate";
import Merge from "./components/Admin/Merge/Merge";
import Admin from "./components/Admin/Admin";
import UnconfirmedAuthors from "./components/Admin/UnconfirmedAuthors/UnconfirmedAuthors";
import Main from "./components/Main/Main";
import AnalysisDate from "./components/Analysis/AnalysisDate";
import Nioktrs from "./components/Nioktrs/Nioktrs";
import Nioktr from "./components/Nioktrs/Nioktr/Nioktr";
import Rids from "./components/Rids/Rids";

function App() {
    const [cookies, , ] = useCookies(['isAuth']);
    const [cookiesTheme, ] = useCookies(['theme']);
    const {colorTheme, toggleColorTheme} = useColorTheme();
    const dispatch = useDispatch();

    useEffect(() => {
        if (cookiesTheme.theme !== colorTheme) {
            toggleColorTheme();
        }
    }, [])

    return <div className='app-wrapper' id='app-wrapper'>
        <main className="main">
            <div className="app-wrapper__container">
                <Header/>
                <div className='app-wrapper-content'>
                    <Routes>
                        <Route exact path = '/' element = {<Main/>}/>
                        <Route exact path='/author/:id'
                               element={<Author/>}/>
                        <Route exact path='/author'
                               element={<Authors/>}/>
                        <Route exact path='/analysis'
                               element={<AnalysisDate/>}/>
                        <Route exact path='/publication'
                               element={<Publications/>}/>
                        <Route exact path='/publication/:id'
                               element={<Publication/>}/>
                        <Route exact path='/nioktr'
                               element={<Nioktrs/>}/>
                        <Route exact path='/nioktr/:id'
                               element={<Nioktr/>}/>
                        <Route exact path='/rid'
                               element={<Rids/>}/>
                        {/*<Route exact path='/rid/:id'*/}
                        {/*       element={<Rid/>}/>*/}
                        <Route exact path='/login'
                               element={<SignIn/>}/>
                        <Route exact path='/source'
                               element={<Sources/>}/>
                        <Route exact path='/source/:id'
                               element={<Source/>}/>
                        <Route exact path='/author/:id/publications'
                               element={<AuthorsPublications/>}/>
                        {cookies.isAuth? <>
                            <Route exact path='/admin/feedbacks'
                                   element={<Feedback/>}/>
                            <Route exact path="/admin/upload"
                                   element={<UploadDate/>}/>
                            <Route exact path={"/admin/unconfirmed"}
                                   element={<UnconfirmedAuthors/>}/>
                            <Route exact path="/admin/merge"
                                   element={<Merge/>}/></> : null}
                        <Route path='*' element={<Error404/>}/>
                    </Routes>
                </div>
                <Footer/>
            </div>
        </main>
    </div>
}

export default withCookies(App);
