import React, { Component } from "react";
import UserForm from "./UserForm";
import { Dialog, DialogActions, DialogContent } from "@material-ui/core";
import { Button, TextField } from "@material-ui/core";
// import InformationForm from "./informationform";
// import InformationModal from "./InformationModal";
// import axios from "axios";
// import { API_URL } from "..";
// import { Paper} from "@mui/material";
// import { Box } from "@mui/material";


class Home extends Component {
    constructor(props) {
      super(props);
    }

    render(){
        // const [ open, setOpen ] = React.useState(false);

        // const handleClickOpen = () => {
        //     setOpen(true);
        // };

        // const handleClose = () => {
        //     setOpen(false);
        // };

        return <html>
            <div className="center">
                <p>This is Homepage Testing 101</p>
                <p> Tryin g something else</p>
                <a href="/host/event/home/" > Test </a>

                <Button
                    variant="outlined"
                > Open Dialog </Button> 

                <UserForm/>
            </div>
                {/* <div className="App">
                <Button
                    variant="outlined"
                    onClick={handleClickOpen}
                >
                    Continue
                </Button>
                <Dialog
                    open={ open} 
                    onClose={handleClose}
                    fullWidth
                    maxWidth="sm"
                >
                <UserForm/>
                <Button onClick={handleClose}>Cancel</Button>
                </Dialog>
                </div> */}
                {/* <div>
                <Box
                sx={{
                    display: 'flex;',
                    flexwrap: 'wrap',
                    '& > :not(style)':{
                        m: 1,
                        width: 250,
                        height: 250,
                    },
                }}
                >
                    <Paper elevetion={0}>
                        <InformationForm />
                    </Paper>
                </Box>  
                </div>               */}
        </html>
    }
}

export default Home