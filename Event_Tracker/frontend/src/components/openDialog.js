import * as React from "react";
import { Button, Dialog, DialogActions, DialogContent } from "@material-ui/core";
import UserAccount from "./UserAccount";

export default function openDialog() {
    const [ open, setOpen] = React.useState(false)

    handleClickOpen = () => {
        setOpen(true);
    };

    handleClose = () => {
        setOpen(false);
    };

    return (
        <>
        <Button variant="outlined" onClick={handleClickOpen}>
            Open Dialog
        </Button>
        <Dialog
            open={ open} 
            onClose={handleClose}
            fullWidth
            maxWidth="sm"
        >
            <UserAccount 
                handleClickOpen={this.handleClickOpen}
                handleClose={this.handleClose}
            />
            <Button onClick={handleClose}>Cancel</Button>
        </Dialog>

            

        </>
    )

    
}

