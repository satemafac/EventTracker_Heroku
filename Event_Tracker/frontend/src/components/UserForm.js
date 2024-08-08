import React, {Component} from "react";
import Confirm from "./Confirm";
import Success from "./Success";
import UserAccount from "./UserAccount";
import UserPayment from "./UserPayment";

export class UserForm extends Component{
    state = {
        step: 1,
        displayName: "",
        firstName: "", //optional
        lastName: "", //optional
        bio: "",
        snapChat: "",
        instagram: "",
        twitter: "",
        cashApp: "",
        venmo: "",
        payPal: "",
    }

    nextStep = () => {
        const { step } = this.state
        this.setState({
            step: step + 1
        });
    };

    prevStep = () => {
        const { step } = this.state
        this.setState({
            step: step - 1
        });
    };
    
    handleChange = input => e => {
        this.setState({ [input]: e.target.value });
    };

    render() {
        const { step } = this.state
        const { displayName, firstName, lastName, bio, snapChat, instagram, twitter, cashApp, venmo, payPal } = this.state;
        const values = { displayName, firstName, lastName, bio, snapChat, instagram, twitter, cashApp, venmo, payPal };

        switch (step) {
            case 1:
                return(
                    <UserAccount
                        nextStep={this.nextStep}
                        handleChange={this.handleChange}
                        values={values}
                    />
                );
            case 2:
                return(
                    <UserPayment
                        nextStep={this.nextStep}
                        prevStep={this.prevStep}
                        handleChange={this.handleChange}
                        values={values}
                    />
                );
            case 3:
                return(
                    <Confirm
                        nextStep={this.nextStep}
                        prevStep={this.prevStep}
                        values={values}
                    />
                );
            case 4:
                return <Success />;
        }
    }
}


export default UserForm