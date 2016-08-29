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

1. Create a **Electronic Funds Transfer Bank Detail**.
	* It is basicly all the information provided by your bank to make it work.
2. Create a **Electronic Funds Transfer Supplier Information**.
	* It is containing all the bank information of your supplier.

## How to use it

1. Create a **Electronic Funds Transfer Supplier Information**.
	* You'll need to provide the **Electronic Funds Transfer Bank Detail** you will be using.
	* The only protocol working right now is the **80 bytes**.
	* Each item is the purchase invoice that need to be paid.
2. Save and Submit the document.
	* This will reserve a sequence number for the bank.
	* It will also save the posting date.
3. Click on **Generate text file**
	* It will create a attachment file that can be send to the bank.
4. Click on **Make payment entry**


## License

GNU V3
