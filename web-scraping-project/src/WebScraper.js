import logo from './logo.svg';
import './WebScraper.css';
import React, { useState, useEffect }  from 'react';
import { useParams, useNavigate, useSearchParams } from "react-router-dom";

function WebScraper() {
  const params = useParams();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [message, setMessage] = useState("");
  const [repositories, setRepositories] = useState([]);
  const [userList, setUserList] = useState([]);
  const [userName, setUserName] = useState();
  const [page, setPage] = useState(1);
  const [hasPrev, setHasPrev] = useState(false);
  const [hasNext, setHasNext] = useState(false);
  const [newUserName, setNewUserName] = useState();
  useEffect(() => {
    async function loadInitialState(){
      await getUserList();
      if (params.userName) {
        setUserName(params.userName);
        await getRepositories(params.userName, searchParams.get('page') || 1);       
      }
    }
    loadInitialState();
  },[params.userName, searchParams.get('page')]);
  const selectUser = async (event) => {
    setPage(1);
    navigate(`/users/${event.target.value}/repositories`);
  }
  const onChangeNewUserName =  (event) => {
    setNewUserName(event.target.value);
  }
  async function getNextPage(){
    setPage(page+1);
    setSearchParams({page: page+1});
  }
  async function getPrevPage(){
    setPage(page-1);
    setSearchParams({page: page-1});
  }
  async function addNewUser() {
    const scrape = await fetch(`http://127.0.0.1:5000/users/${newUserName}`);
    const data = await scrape.json();
    setMessage(data.message);
    if (data.status == "USER_ADDED" || data.status == "USER_EXISTS"){
      navigate(`/users/${newUserName}/repositories`);
    }
  }
  async function getRepositories(user_name, pageNumber=1) {
    const repositories = await fetch(`http://127.0.0.1:5000/users/${user_name}/repositories?page=${pageNumber}`);
    const data = await repositories.json();
    const totalRepositories = data.total;
    const totalNumberOfPages = Math.ceil(totalRepositories/10);
    if (pageNumber == 1){
      setHasPrev(false);
    }
    if (pageNumber>1 && pageNumber<=totalNumberOfPages) {
      setHasPrev(true);
    }
    if (pageNumber<totalNumberOfPages) {
      setHasNext(true);
    }
    if (pageNumber == totalNumberOfPages){
      setHasNext(false);
    }
    setRepositories(data.repository);
  }
  async function getUserList() {
    const user_list = await fetch(`http://127.0.0.1:5000/users`);
    const data = await user_list.json();
    setUserList(data.user_list);
  } 
   return (
    <div className="WebScraperMain">
      <div className="WebScraperAddNewUser">
        <h4>Enter a new user to scrape</h4>
          <input type="text" id="user_name" onChange={onChangeNewUserName}/> 
          <button onClick={addNewUser}>Submit</button>
        <h3>{message}</h3> 
      </div>
      <div className="WebScraperSelectUser">
        <select onChange={selectUser} id="user_list" value={userName}>
          {
              userList.map((user, i) => {
                return(<option key={i} value={`${user.user_name}`}>{user.user_name}</option>)
              })
            }
        </select>
        {
          repositories.map((repo, i) =>{
            return (<h4 key={i}>{repo.name}</h4> )
          })
        }
      </div>
      <div className="WebScraperPrevNext">
        <button onClick={getPrevPage} className="prevButton" disabled={!hasPrev}>Previous</button> 
        <button onClick={getNextPage} className="nextButton" disabled={!hasNext}>Next</button> 
      </div>
      </div>
  );
}
export default WebScraper;