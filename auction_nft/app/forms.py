from django import forms
from .models import Profile, Artwork


class NFT(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "name",
            "symbol",
            "image",
            "description",
            "artwork_url",
            "artist_address",
            "starting_price",
            "buy_now",
            "ending_auction",
        ]
        labels = {
            "name": "Name",
            "symbol": "Set a 10 Letter Max Symbol",
            "description": "description",
            "artwork_url": "Your Image Url",
            "artist_address": "Your Address",
            "starting_price": "Set Initial Price",
            "buy_now": "Price buy now",
            "ending_auction": "Auction Ending On",
        }


class Conversion(forms.Form):
    convert_dollar = forms.FloatField(
        label="convert_dollar($)", widget=forms.TextInput(attrs={"class": "black-text"})
    )

    def clean(self):
        cleaned_data = super().clean()
        convert_dollar = self.cleaned_data.get("convert_dollar")
        if convert_dollar < 0:
            raise forms.ValidationError("")  # display messages.error instead
        return cleaned_data


class Make_an_offer(forms.Form):
    offer = forms.FloatField(
        label="offer($)", widget=forms.TextInput(attrs={"class": "black-text"})
    )

    def clean(self):
        cleaned_data = super().clean()
        offer = self.cleaned_data.get("offer")
        if offer < 0:
            raise forms.ValidationError("")  # display messages.error instead
        return cleaned_data
