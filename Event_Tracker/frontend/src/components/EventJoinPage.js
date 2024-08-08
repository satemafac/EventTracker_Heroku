import React, { Component } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class EventJoinPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      eventCode: "",
      error: ""
    };
    this.handelTextFieldChange = this.handelTextFieldChange.bind(this);
    this.eventButtonProssed = this.eventButtonProssed.bind(this);
  }

  render() {
    return (
      <Grid container spacing={1} className="center">
        <Grid item xs={12} align="center">
          <Typography variant="h4" component="h4">
            Join Event
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <TextField 
          erorr={this.state.error} 
          label="code"
          placeholder="Enter a Event Code"
          value={this.state.eventCode}
          helperText={this.state.error}
          variant="outlined"
          onChange={this.handelTextFieldChange}>
          </TextField>
        </Grid>
        <Grid item xs={12} align="center">
        <Button variant="contained" color="primary" onClick={this.eventButtonProssed}>
          Enter Event
        </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" to="/" component={Link}> 
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  handelTextFieldChange(e){
    this.setState({
      eventCode: e.target.value,
    });
  }

  eventButtonProssed(){
    
    const requestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        event_code_short: this.state.eventCode,
      }),
    };
    fetch("/host/join-event", requestOptions).then((response) =>{
      if (response.ok){
          this.props.history.push(`/welcome/${this.state.eventCode}`);
        } else {
          this.setState({ error: "Room not found." });
        }
    })
     .catch((error) => {
        console.log(error);
      });
  }

}