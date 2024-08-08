import React, {Component} from "react";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";



export class Success extends Component{
    continue = e => {
        e.preventDefault();
        //Process Form//
        this.props.nextStep();
    };
    back = e => {
        e.preventDefault();
        this.props.prevStep();
    };

    render() {
        return(<>
         {/* <h1> Test </h1> */}
             <MuiThemeProvider>
                <>
                    <Dialog
                        open
                        fullWidth
                        maxWidth="sm"
                    >
                        <AppBar title="Sucess" />
                        <h1> Form Successfully filled out </h1>
                    </Dialog>
                </>
            </MuiThemeProvider>
            </>
        )
    }
}

export default Success