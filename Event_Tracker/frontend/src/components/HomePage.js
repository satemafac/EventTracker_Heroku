import React, { Component } from "react";
import EventJoinPage from "./EventJoinPage";
import MicrophoneComponent from "./MicrophoneComponent";
import CreateRoomPage from "./CreateRoomPage";
import Event from "./Event";
import Welcome from "./Welcome";
import Home from "./Home";
import PerformerForm from "./PerformerForm";

import { BrowserRouter as Router, Switch, Route, Link, Redirect, } from "react-router-dom";


export default class App extends Component{
    constructor(props){
        super(props);
    }
    render(){
        return (
        <Router>
            <switch>
                <Route exact path='/' component={Home} ></Route>
                <Route path='/welcome/:eventCode' component={Welcome} ></Route>
                <Route path='/join' component={EventJoinPage} ></Route>
                <Route path='/performer/:eventCode' component={PerformerForm} ></Route>
                <Route path='/create' component={CreateRoomPage} ></Route>
                <Route path='/event/:eventCode' component={Event}></Route>
                <Route path='/dictate' component={MicrophoneComponent}></Route>
            </switch>
        </Router>);
    }
}.5