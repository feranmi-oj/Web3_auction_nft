from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Profile, Artwork
from django.contrib import messages
from .forms import NFT, Conversion, Make_an_offer
import json
from web3 import Web3
from datetime import datetime
import pytz
from bson import ObjectId
import pymongo
from eth_utils import to_hex

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))


w3.eth.defaultAccount = w3.eth.accounts[1]
Faucet = w3.eth.defaultAccount


w3.eth.defaultAccount = w3.eth.accounts[0]
Recipient = w3.eth.defaultAccount

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Artwork__Project__Web3"]

# ArtworkToken ERC1155
contract_address1155 = w3.toChecksumAddress("0xA911F7e46DB3e68Cdce80cDB18F15890fe82772b")
abi = json.loads(
    """[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_artist","type":"address"},{"internalType":"string","name":"artworkID","type":"string"},{"internalType":"uint256","name":"initialSupply","type":"uint256"},{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"}],"name":"addArtwork","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"artworkIDCounter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"burnBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getAllTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"idmap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lookupmap","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"namemap","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]"""
)
contract1155 = w3.eth.contract(
    address=contract_address1155,
    abi=abi,
)


# Contract FeroToken ERC20
contract_address20 = w3.toChecksumAddress("0x2fc81445FcF32c8e7217cF983CBFcc085B601805")
abi20 = json.loads(
    """[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]"""
)
contract20 = w3.eth.contract(address=contract_address20, abi=abi20)


# views first page app
def home_page_view(request):
    return render(request, "app/base.html")


# We are creating our NFT
def create_artwork(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = NFT(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            name = form.name
            symbol = form.symbol
            image = form.image
            description = form.description
            artwork_url = form.artwork_url
            artist_address = form.artist_address
            starting_price = form.starting_price
            buy_now = form.buy_now
            ending_auction = form.ending_auction
            # Minting Our Token ERC1155

            txHashForERC1155 = contract1155.functions.addArtwork(
                profile.address_g,
                artwork_url,
                1,
                name,
                symbol,
            ).transact({"from": Recipient})

            new_artwork = Artwork.objects.create(
                name=name,
                symbol=symbol,
                image=image,
                description=description,
                artwork_url=artwork_url,
                artwork_hash= w3.toHex(txHashForERC1155),
                artist_address=artist_address,
                starting_price=starting_price,
                buy_now=buy_now,
                ending_auction=ending_auction,
            )
            new_artwork.status = "open"

            if new_artwork.artist_address != profile.address_g:
                new_artwork.delete()
                messages.error(request, "You are not the address owner")
                return redirect("app:create_section")
            if new_artwork.artwork_url in Artwork.objects.all():
                new_artwork.delete()
                messages.error(request, "Artwork url exist in database")

            new_artwork.save()
            profile.save()
            form.save()
            messages.success(request, f"""{request.user}...You Minted A New Nft""")
            return redirect("app:home_auction")

    else:
        form = NFT()
        context = {"form": form}
        return render(request, "app/create_section.html", context)


def show_artwork(request, pk):
    artwork = Artwork.objects.filter(_id=ObjectId(pk)).first()
    context = {"artwork": artwork}
    utc = pytz.UTC
    # if the auction ends, it rewards the winner if one exists
    if artwork.ending_auction.replace(tzinfo=utc) < datetime.today().replace(
        tzinfo=utc
    ):
        if artwork.buyer != None:

            # Tranfer Artwork NFT
            contract1155.functions.safeTransferFrom(
                Recipient, artwork.buyer.address_g, contract1155.functions.idmap(artwork.artwork_url).call(), 1, "")

            winnerAuction = {
                "Item Name": artwork.name,
                "Artwork Url": artwork.artwork_url,
                "Item Hash": artwork.artwork_hash,
                "Creator": artwork.artist_address,
                "Winner": artwork.buyer.address_g,
                "Price": artwork.token_offer,
            }

            myNewColl = mydb["Winner Auction "]
            informationAboutIt = winnerAuction
            populateDatabase = myNewColl.insert_one(informationAboutIt)
            messages.success(
                request,
                f"""The Artwork {artwork.name} at auction were sold at {artwork.buyer} for the price of {artwork.token_offer} ether""",
            )
        else:
            messages.success(
                request,
                f"the auction that included the sale of these artwork {artwork.name}, was not awarded to anyone",
            )
            noWinnerAuction = {
                "Artwork Name": artwork.name,
                "Artwork Url": artwork.artwork_url,
                "ArtworkTX Hash": artwork.artwork_hash,
                "Creator": artwork.artist_address,
            }
            myColl = mydb["No Winner Auction"]
            informationAbout = noWinnerAuction
            populateDatabase = myColl.insert_one(informationAbout)

        artwork.status = "close"
        artwork.save()
        return redirect("app:home_auction")
    return render(request, "app/show_section.html", context)


# view home list auction
def home_auction_view(request):

    artwork = Artwork.objects.filter(status="open").order_by("-ending_auction")
    context = {"artwork": artwork}
    return render(request, "app/home_auction.html", context)


# views make offer with FeroToken
def make_offer_view(request, pk):
    profile = Profile.objects.get(user=request.user)
    artwork = Artwork.objects.filter(_id=ObjectId(pk)).first()

    if request.method == "POST":
        form = Make_an_offer(request.POST)
        if form.is_valid():
            offer = form.cleaned_data.get("offer")

            if offer < 0:
                messages.error(
                    request, "This Offer Cannot Be Updated, Because Is Lower Than 0 "
                )
                return redirect("app:make_an_offer", kwargs={"pk": artwork.pk})
            if profile.token_amount >= offer:

                # if the offer is equal to the cost of the artwork to buy now the auction ends and the user wins the artwork
                if offer == artwork.buy_now:
                    if artwork.token_offer > 0.0:
                        prev_token_offer = artwork.token_offer
                        prev_buyer = artwork.buyer
                        contract20.functions.transfer(
                            prev_buyer.address_g, w3.toWei(prev_token_offer, "ether")
                        ).transact({"from": artwork.artist_address})
                        prev_buyer.save()

                    # Send FeroToken
                    contract20.functions.transfer(
                        artwork.artist_address, w3.toWei(offer, "ether")
                    ).transact({"from": profile.address_g})

                    # Tranfer Artwork NFT
                    contract1155.functions.safeTransferFrom(
                        Recipient,profile.address_g,contract1155.functions.idmap(artwork.artwork_url).call(),1, "")

                    artwork.buyer = profile
                    profile.save()
                    messages.success(
                        request,
                        f"""Your offer is equal to Buy Now price. Congrats To Your Wonderfull Item Choise. Your Balance Now Is {profile.token_amount} ether""",
                    )
                    artwork.status = "close"
                    artwork.save()

                    return redirect("app:home_auction")

                # if the bid is greater than the initial price and the previous bid, the user wins the auction for the time being
                elif offer >= artwork.starting_price and offer >= artwork.token_offer:
                    # if there was a previous winner, the money spent is refunded
                    if artwork.buyer != None:
                        prev_token_offer = artwork.token_offer
                        prev_buyer = artwork.buyer
                        contract20.functions.transfer(
                            prev_buyer.address_g, w3.toWei(prev_token_offer, "ether")
                        ).transact({"from": artwork.artist_address})
                        prev_buyer.save()

                    # Send FeroToken
                    contract20.functions.transfer(
                        artwork.artist_address, w3.toWei(offer, "ether")
                    ).transact({"from": profile.address_g})

                    artwork.token_offer = offer
                    artwork.buyer = profile
                    artwork.save()
                    profile.save()

                    messages.success(request, "Offer Update Succesfully")
                    return redirect(f"/show_section/{artwork.pk}")
                elif offer < artwork.starting_price:
                    messages.error(
                        request,
                        f"Your bid cannot be considered, because the starting price for this auction is {artwork.starting_price} $",
                    )
                    return redirect(f"/make_an_offer/{artwork.pk}")
                elif offer >= artwork.starting_price and offer <= artwork.token_offer:
                    messages.error(
                        request,
                        f"""Excuse me. Your offer cannot be considered, because an offer of {artwork.token_offer} has been made.
                                        If you are going to buy it, you need to make a better offer""",
                    )
                    return redirect(f"/make_an_offer/{artwork.pk}")

    else:
        form = Make_an_offer()
    return render(request, "app/make_an_offer.html", {"form": form, "artwork": artwork})


# view conversion dollar a Ferotoken
def conversion_dollar_view(request):
    profile = Profile.objects.get(user=request.user)
    contract_name = contract20.functions.name().call()
    contract_symbol = contract20.functions.symbol().call()
    f = contract20.functions.balanceOf(Faucet).call()
    faucet_balance = w3.fromWei(f, "ether")
    t = contract20.functions.totalSupply().call()
    total_supply = w3.fromWei(t, "ether")

    if request.method == "POST":
        form = Conversion(request.POST)
        if form.is_valid():
            convert_dollar = form.cleaned_data.get("convert_dollar")

            if convert_dollar == 0:
                messages.error(request, "Cannot convert 0")
                return redirect(reverse("conversion"))

            if convert_dollar < 0:
                messages.error(request, "Cannot convert less than 0")
                return redirect(reverse("conversion"))

            if convert_dollar > 0 and profile.dollar_amount >= convert_dollar:
                profile.dollar_amount -= convert_dollar
                dollarToWei = w3.toWei((convert_dollar / 10), "ether")

                txHashConversion = contract20.functions.transfer(
                    profile.address_g, dollarToWei
                ).transact({"from": Faucet})

                profile.save()
                messages.success(request, "You converted your dollar correctly")
                return redirect("accounts:profile", request.user.pk)

            else:
                messages.error(request, "Your funds are not enough!")
                return redirect("accounts:profile", request.user.pk)

    else:
        form = Conversion()
    context = {
        "form": form,
        "contract_name": contract_name,
        "contract_symbol": contract_symbol,
        "faucet_balance": faucet_balance,
        "total_supply": total_supply,
        "faucet": Faucet,
        "contract_address20": contract_address20,
    }
    return render(request, "app/convert_dollar.html", context)


# views buy now
def buy_now(request):
    profile = Profile.objects.get(user=request.user)
    for artwork in Artwork.objects.filter().order_by("-ending_auction"):
        buy_now = artwork.buy_now
        if profile.token_amount >= buy_now:

            if artwork.buyer != None:
                prev_offer = artwork.token_offer
                prev_buyer = artwork.buyer
                contract20.functions.transfer(
                    prev_buyer.address_g, w3.toWei(prev_offer, "ether")
                ).transact({"from": artwork.artist_address})
                prev_buyer.save()

            contract20.functions.transfer(
                artwork.artist_address, w3.toWei(buy_now, "ether")
            ).transact({"from": profile.address_g})
            messages.success(
                request,
                f"Your Buy-Now Choise Had Success. Congrats To Your Wonderfull Artwork Choise. Your Balance Now Is {profile.token_amount}",
            )

            # Transfer Artwork NFT
            contract1155.functions.safeTransferFrom(
                Recipient, profile.address_g, contract1155.functions.idmap(artwork.artwork_url).call(), 1, "")

            artwork.token_offer = buy_now
            artwork.buyer = profile
            artwork.status = "close"
            artwork.save()

            return redirect("app:home_auction")
        else:
            messages.error(
                request,
                "You Do Not Have Necessary Funds To Do This Transaction! We Are Sending You Back To The Offer Section !",
            )
            return redirect(f"/show_section/{artwork.pk}")
