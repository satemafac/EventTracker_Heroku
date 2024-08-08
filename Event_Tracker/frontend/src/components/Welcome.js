import React, { Component } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
// import InformationModal from "./InformationModal";
// import { TextField, Button, Grid, Typography } from "@material-ui/core";
// import { Link } from "react-router-dom";

export default class Welcome extends Component {
    constructor(props) {
      super(props);
    this.eventCode = this.props.match.params.eventCode;
    }
    // This would have to go to the next page
    async componentDidMount(){
        fetch("/host/get-event?event_code_short="+this.eventCode)
        .then((response) => {
            if(!response.ok){
                this.setState({
                    reqs: 404
                });
            console.log(bad_request)
            }
            else return response.json();
        })
            .then((data) => {
                this.setState({
                    location: data.event_location,
                    org: data.event_org,
                });
            });
    }   


render(){
    if (this.reqs != 404){
    return(
        
        <Grid container spacing={1} className="center">
            <Grid item xs={12} align="center">
                <Button variant="contained" color= "primary" onClick={this.eventButtonProssed}>
                        Guest
                        {/* <InformationModal
                        placeholder="Enter a Event Code"/> */}
                </Button>
                <Button variant="contained" color= "secondary"  to={"/performer/"+this.eventCode} component={Link}>
                {/* <Button variant="contained" color="secondary" to={"/host/get-event/?event_code_short=" +this.eventCode} component={Link}>  */}
                        Performer
                        {/* <InformationModal/> */}
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
            <Typography variant="h4" component="h4">
            URL Data is: {this.eventCode + this.reqs}
            {/* <InformationModal/> */}
          </Typography>
            </Grid>
        </Grid>
        
    );}
    // return<html lang="en">
    //     <nav class="navbar navbar-dark">  
    //         <div class="container-fluid">
    //                 {/* <!-- <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navmenu">
    //             <span class="navbar-toggler-icon"></span>
    //             inputProps={{style:{textAlign: "center"}}}
    //             </button> -->  */}

    //         <a  style={{"color": "yellow"}} href="/host/event/home/">
    //             Go Back
    //         </a>
    //         </div>
           
    //         <div> <p>This is Homepage Testing 101</p> </div>
    //         <div><p> Tryin g something else</p> </div>
    //         <div><p> Stanly is a whore</p> </div>
    //         <a class="test" href="/host/event/home/" > Test </a>
    //     </nav>     
    //         <div className="center">
    //             <button type="button" class="btn btn-primary btn-lg"> Guest</button>
    //             <button type="button" class="btn btn-primary btn-lg" to="/"> Performer</button>
    //         </div>

    //         {/* <Grid item xs={12} align="center">
    //       <Button variant="contained" color="secondary" to="/" component={Link}> 
    //         Back
    //       </Button>
    //     </Grid> */}

        
    // </html>
}

}