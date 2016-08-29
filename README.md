# Electronic Funds Transfer

 Electronic Funds Transfer (EFT) Direct Deposit is an electronic payment service that provides your business with a fast and simple way to issue Canadian and U.S. dollar payments to accounts at any financial institution in Canada.

## Warning

 This is an Alpha Version use at your own risk.

 Only the payment of the supplier is supported as of now.

## Full Install

The Easy Way: our install script for bench will install all dependencies (e.g. MariaDB). See https://github.com/frappe/bench for more details.

New passwords will be created for the ERPNext "Administrator" user, the MariaDB root user, and the frappe user (the script displays the passwords and saves them to ~/frappe_passwords.txt).

Once you install ERPNext run -

```
$ bench get-app EFT https://github.com/CloudGround/electronic_funds_tranfer.git
$ bench install-app EFT 
```

## Initial configuration



#### License

GNU V3
