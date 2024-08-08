import React, { Component } from 'react';
import {Helmet} from "react-helmet";
import Header from "./Header";
import { LinkPreview } from '@dhaiwat10/react-link-preview';

export default class Event extends Component {
    state = {img_url : ""}
    
    constructor(props){
        super(props);
        this.state = {
            eventName : "Open Mic",
            hostName : "Stalanic",
            eventOrg : "Bust Boys"
        };
        this.eventCode = this.props.match.params.eventCode;
    }

    // getRoomDetails(){
    //     fetch("get-room"+"?code="+this.eventCode)
    // }
    async componentDidMount(){
        fetch("/host/get-event?event_code_short="+this.eventCode)
            // .then((response) => response.json())
            .then((response) => {
                if(!response.ok){
                    this.setState({
                        req: response.status
                    });
                    console.log(bad_request)
                }
                else return response.json();
            })
            // console.log(response)
            .then((data) => {
                this.setState({
                    // req: response.status,
                    event_name: data.event_name,
                    location: data.event_location,
                    org: data.event_org,
                    start: data.event_start_date,
                    end: data.event_end_date,
                    event_bio: data.about_event,
                    image: "http://127.0.0.1:8000/"+data.event_image,
                    // api_status: data.response.json()
                });
            });
    } 
    
// if (req === 400)
    render(){
        if (this.state.req != 404){
        return ( 
        <>
        <div className="overflow-auto">
            <Header imgUrl = {this.state.image}  />
            <h3>{this.eventCode}</h3>
            <p> Event Name: {this.state.event_name}</p>
            <p> Org: {this.state.org} </p>
            <p> Location: {this.state.location} </p>
            <p> Event start: {this.state.start} </p>
            <p> Event end: {this.state.end} </p>
            <p> Event Bio: {this.state.event_bio} </p>
            <p> Image: {this.state.image} </p>
            <LinkPreview url='https://www.instagram.com/stalanic/' width='200px' />;
            {/* <a href="https://twitter.com/TwitterDev?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-show-count="false">Follow @TwitterDev</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> */}
            <a class="twitter-timeline" data-width="220" data-height="200" data-theme="dark" href="https://twitter.com/TwitterDev?ref_src=twsrc%5Etfw">Tweets by TwitterDev</a> <Helmet><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script></Helmet>
            <a href="https://msng.link/o/?standeman35=sc">Message me on Snapchat</a>
            <a href="https://msng.link/o/?alphakings5=tt">Message me on TikTok</a>
            <a href="https://msng.link/o/?stalanic=ig">Message me on Instagram</a>
            
        </div>
        </>
        );}
        
    }
}