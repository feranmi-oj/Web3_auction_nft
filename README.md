## ARTWORK AUCTION NFT
ARTWORK AUCTION NFT is a platform for managing the sale of works 
of art through a charity auction that interacts with
two smart contracts distributed on Ganache and created, c
ompiled with Remix Ide, an Token erc20 that will be used as a spendable currency 
and an token erc721 used to create works of art nft.

To enter the platform and start bidding and purchasing artwork,
there are two pages for user registration and login. The platform provides each user with a random amount of $ upon registration and 10 FeroToken.

Within the platform only the administrator can create the NFT artwork.

To start bidding on artwork, any user can convert dollars into FeroToken. 10 $ equals 1 Ferotoken.
At the end of an auction, the database will receive and save all information about the auction and the winner.

### Installation:
To be able to see the platform you need to: 
- download the code and open it in a development environment
- then open a virtual environment and thanks to the requirements.txt file you can install all the necessary packages for the project

### Start the project

- Before starting the runserver  in the terminal you need to do a first migration with:
```sh
    $ python manage.py migrate
 ```
    
* And create a superuser with: 
```sh
    $ python manage.py createsuperuser
 ```
- **Example Superuser**
 
    username: admin 
    
     password: admin


- Then, start the project by typing:
```sh
    $ python manage.py runserver 
```
- Once the server is started, we enter the registration page
  and start registering from the third address of your ganache 
  because the first two are used for tokens

- When you have the address, copy the private key of the address and go to your Metamask wallet. 
  Once there, attach the private key to import the account. 
  Now you can open the site and register with the same Ganache address you chose.