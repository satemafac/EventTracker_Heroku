import React, {Component} from "react";
import { Box,Button, TextField } from "@material-ui/core";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";



function UserSocials({formData, setFormData}) {
    return (
        <div className="other-info-container">
            <Box m={2}>
            <TextField id="outlined-basic" 
            label="Twitter"
            value={formData.twitter}
            onChange={(e) => {
                setFormData({ ...formData, twitter: e.target.value });
              }} 
            variant="outlined" />
            </Box>

            <TextField id="outlined-basic" 
            label="Instagram" 
            value={formData.instagram}
            onChange={(e) => {
                setFormData({ ...formData, instagram: e.target.value });
              }} 
            variant="outlined" /> 

            <Box m={2}>
            <TextField id="outlined-basic" 
            label="Snapchat"
            value={formData.snapchat}
            onChange={(e) => {
                setFormData({ ...formData, snapchat: e.target.value });
              }} 
            variant="outlined" />  
            </Box>
        </div>
    )
}

export default UserSocials