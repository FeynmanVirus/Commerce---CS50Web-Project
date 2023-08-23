from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Textarea
from .models import Listings

CATEGORIES = [
    ("N", "No category"),
    ("F", "Fasion"),
    ("T", "Toys"),
    ("E", "Electronics"),
    ("H", "Home"),
    ("HW", "Hardware")
]

class ListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Title here...",
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "rows": "2",
        "cols": "25",
        "placeholder": "Description for your product here..."
    }))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Price here. Please omit the $",
    }))
    image_link = forms.URLField(required=False, widget=forms.TextInput(attrs={
        "placeholder": "Product's image link here...",
    }))
    category = forms.ChoiceField(choices=CATEGORIES)
    
class BiddingForm(forms.Form):
    bid = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Bid Amount",
        "style": "width: 40%;"
    }))

class CommentsForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Share your thoughts through the comments",
        "rows": 1,
        "cols": 50,
        "style": "display: block;"
    })) 