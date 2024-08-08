import React, {Component} from "react";
import { Button, TextField } from "@material-ui/core";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";
import { List, ListItem, ListItemText } from "@material-ui/core";



function Confirm({formData, setFormData}){
        return(<>
         {/* <h1> Test </h1> */}
             <MuiThemeProvider>
                <>
                        <AppBar title="Confirm User Data" />
                        <List>
                            <ListItem>
                                <ListItemText primary="display Name" secondary={formData.displayName} />
                            </ListItem>
                            <ListItem>
                                <ListItemText primary="First Name" secondary={formData.firstName} />
                            </ListItem>
                            <ListItem>
                                <ListItemText primary="Last Name" secondary={formData.lastName} />
                            </ListItem>
                            <ListItem>
                                <ListItemText primary="cashApp" secondary={formData.cashApp} />
                            </ListItem>
                            <ListItem>
                                <ListItemText primary="venmo" secondary={formData.venmo} />
                            </ListItem>
                            <ListItem>
                                <ListItemText primary="payPal" secondary={formData.payPal} />
                            </ListItem>
                        </List>
                        <br />
                </>
            </MuiThemeProvider>
            </>
        )
}

export default Confirm