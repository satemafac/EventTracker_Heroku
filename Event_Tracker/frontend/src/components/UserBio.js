import React, {Component} from "react";
import { Box,Button, TextField } from "@material-ui/core";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";



function UserBio({formData, setFormData}) {
    return (
        <div className="other-info-container">
            <Box m={2}>
            <TextField id="outlined-textarea"
            label="Introduction/Bio"
            placeholder="About Me"
            multiline
            value={formData.bio}
            onChange={(e) => {
                setFormData({ ...formData, bio: e.target.value });
              }} 
            variant="outlined" />
            </Box>             
        </div>
        
    )
}

export default UserBio