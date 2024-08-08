import React, {Component} from "react";
import {Box, Button, } from "@material-ui/core";
import { FaBeer } from 'react-icons/fa';
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import TextField from '@mui/joy/TextField';
import Chip from '@mui/joy/Chip';
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";



function UserAccount({formData, setFormData}) {
    return (
        <div className="other-info-container">
            <Box m={2}>
            <TextField id="outlined-basic" 
            label="Display Name" 
            startDecorator={<PersonRoundedIcon fontSize="small" />}
            value={formData.displayName}
            onChange={(e) => {
                setFormData({ ...formData, displayName: e.target.value });
              }}
            variant="outlined" />
            </Box>

            <TextField id="outlined-basic" 
            label="e-mail" 
            value={formData.email}
            onChange={(e) => {
                setFormData({ ...formData, email: e.target.value });
              }}
            variant="outlined" />
            
            <Box m={2}>
            <TextField id="outlined-basic" 
            label="First Name"
            value={formData.firstName}
            onChange={(e) => {
                setFormData({ ...formData, firstName: e.target.value });
              }} 
            variant="outlined" /> 
            </Box>

            <TextField id="outlined-basic" 
            label="Last name" 
            value={formData.lastName}
            onChange={(e) => {
                setFormData({ ...formData, lastName: e.target.value });
              }}
            variant="outlined" />
                     
        </div>
    );
}

export default UserAccount