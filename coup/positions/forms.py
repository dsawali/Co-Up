from django import forms
from .models import Position, Comment


class PositionForm(forms.ModelForm):
    """
    This form simplifies the creation of a view and template
    for the addition of positions to user profiles.
    """
    class Meta:
        model = Position
        fields = (
            'company',
            'title',
            'start_year',
            'end_year',
            'start_month',
            'end_month',
            'location_addr',
            'location_lat',
            'location_lng'
        )

class CommentForm(forms.ModelForm):
    """
    This forms simplifies the creation of a view and template
    for the addition of comments on positions held by a certain user.
    """
    class Meta:
        model = Comment
        fields = (
            'comment',
        )
