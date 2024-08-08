import React, {useState} from "react";
import { Link } from "react-router-dom";
import { Button, TextField } from "@material-ui/core";
import { AppBar } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core";
import UserAccount from "./UserAccount";
import UserPayment from "./UserPayment";
import UserSocials from "./UserSocials";
import UserBio from "./UserBio";
import Confirm from "./Confirm";
import axios from "axios";
import { USERS_API } from "../constants";


function Form(){
    const[page,setPage] = useState(0);
    
    const [formData, setFormData] = useState({
        displayName: "",
        email: "",
        firstName: "",
        lastName: "",
        twitter: "",
        instagram: "",
        snapchat: "",
        cashApp: "",
        venmo: "",
        paypal: "",
        bio: ""

      });

    const FormTitles = ["Performer Info","Socials","Payments","Bio","Summary"];

    const PageDisplay = () => {
        if (page === 0){
            return <UserAccount formData={formData} setFormData={setFormData}/>;
        } else if (page === 1){
            return <UserSocials formData={formData} setFormData={setFormData}/>;
        } else if (page === 2){
            return <UserPayment formData={formData} setFormData={setFormData}/>;
        } else if (page === 3){
            return <UserBio formData={formData} setFormData={setFormData}/>;
        } else {
            return <Confirm formData={formData} setFormData={setFormData}/>;
        }
    }

    return(
        <div className="form">
            <div className="progressbar">
                <div style={{width: page === 0 ? "20%": page === 1 ? "40%": 
                page === 2 ? "60%": page === 3 ? "80%": "100%"}}></div>
            </div>
            <div className="form-container">
                <div className="header">
                    <h1>{FormTitles[page]}</h1>
                </div>
                <div className="form-body">{PageDisplay()}</div>
                <div className="footer">
                    <Button variant="contained" color='secondary'
                     disabled = {page == 0}
                    onClick={() => {setPage((currPage) => currPage-1)}}>
                    Prev</Button>

                    <Button variant="contained" color='primary'
                        onClick={() => {
                            if (page === FormTitles.length -1){
                                console.log(formData)
                                const postUsers = () => {
                                    axios
                                      .post(USERS_API, {
                                        user_fname: formData.firstName,
                                        user_lname: formData.lastName,
                                        username: formData.displayName,
                                        is_event_host: false,
                                        is_event_performer: true,
                                        is_event_guest: false
                                      })
                                      .then(response => {
                                        // console.log(response);
                                        console.log(response)
                                      })
                                      .catch(error => {
                                        console.error(error);
                                      });
                                  };
                                  postUsers();

                            }else{
                            setPage((currPage) => currPage+1)
                            }
                        }}
                    >
                         

                    {page === FormTitles.length - 1 ? "Submit":"Next"}</Button>
                
                </div>
            </div>
        </div>
    )
}

export default Form;