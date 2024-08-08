import React, {Component} from "react";
import { Box,Button, TextField } from "@material-ui/core";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";



function UserPayment({formData, setFormData}) {
    return (
        <div className="other-info-container">
            <Box m={2}>
            <TextField id="outlined-basic" 
            label="Cas App" 
            value={formData.cashApp}
            onChange={(e) => {
                setFormData({ ...formData, cashApp: e.target.value });
              }} 
            variant="outlined" />
            </Box>

            <TextField id="outlined-basic" 
            label="PayPal" 
            value={formData.paypal}
            onChange={(e) => {
                setFormData({ ...formData, paypal: e.target.value });
              }} 
            variant="outlined" /> 

            <Box m={2}>
            <TextField id="outlined-basic" 
            label="Venmo" 
            value={formData.venmo}
            onChange={(e) => {
                setFormData({ ...formData, venmo: e.target.value });
              }} 
            variant="outlined" />    
            </Box>                   
        </div>
        
    )
}

export default UserPayment