from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,UserEditForm,LoginForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from app.models import Profile,Artwork
from django.utils import timezone
import random
from web3 import Web3
import json
#Connect to Ganache
ganache_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(ganache_url))

#Set first account as Faucet
w3.eth.defaultAccount = w3.eth.accounts[1]
Faucet = w3.eth.defaultAccount


#Contract for Token ERC20 is already deployed from remix
contractAddress20 = w3.toChecksumAddress('0xf5E2E53109776C2C7dF620B03ADC3af632dF7A32')
abi20 = json.loads('''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
contract = w3.eth.contract(address=contractAddress20, abi=abi20)

print(contract.functions.name().call())

def ip_control_view(request):

    return render(request, 'accounts/ip_control.html', )


def getIpAdd(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


def login_view(request):
    ip_address = getIpAdd(request)
    initial_data = {
        'ip_address': ip_address,
    }
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            try:
                user_info = Profile.objects.get(user=user)
                user_info.last_login = timezone.now()
            except:
                user_info = Profile.objects.create(user=user)
                user_info.last_login = timezone.now()
            user_info.save()

            ip_address = getIpAdd(request)

            if ip_address != user_info.ip_address:
                user_info.ip_address = ip_address
                user_info.save()
                return redirect(f"accounts:ip-control")

            else:
                return redirect('accounts:profile',user.pk)
    else:
        form = LoginForm(initial=initial_data)
    return render(request, 'accounts/login.html',{'form': form})





def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():


            address= form.cleaned_data.get('address')
            if Profile.objects.filter(address_g=address).exists():
                messages.error(request,'This address is already in the database')
                return redirect('accounts:register')
            user = form.save()
            user.refresh_from_db() #stiamo andando a ricaricare l'istanza del profilo che è stata generata dal signals

            newUser = Profile(user=user)
            tx = contract.functions.transfer(address,10000000000000000000).transact({'from': Faucet})
            addressBalance = contract.functions.balanceOf(address).call()
            tBalance = w3.fromWei(addressBalance, 'ether')
            newUser.dollar_amount= int(random.uniform(1000, 2000))
            newUser.ip_address=getIpAdd(request)
            newUser.last_login=timezone.now()
            newUser.address_g=address
            newUser.token_amount=tBalance
            newUser.save()


            row_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username,password=row_password)
            login(request,user)
            return redirect('accounts:profile',user.pk)
    else:
        form = RegistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})

    return render(request,'accounts/registration.html',{'form': form})

@login_required()
def profile(request,id):
    profile = get_object_or_404(Profile, user_id=id)
    profile_pocket = Profile.objects.get(user=request.user)
    ferotoken_balance = contract.functions.balanceOf(profile_pocket.address_g).call()
    profile_pocket.token_amount= w3.fromWei(ferotoken_balance, 'ether')
    profile_pocket.save()
    artwork = Artwork.objects.filter(buyer=profile).order_by('-ending_auction')

    return render(request, 'accounts/profile.html', {'profile': profile,'profile_pocket':profile_pocket,'artwork': artwork,})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid() :
            user_form.save()

            messages.success(request,'Your profile has been successfully edited')
            return redirect('accounts:profile', request.user.pk)
        else:
            messages.error(request,'The data entered is not valid',extra_tags='danger')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,'accounts/edit.html',{'user_form': user_form})