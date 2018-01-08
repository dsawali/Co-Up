from django import forms

from ..users.models import User, getChoices
from ..positions.models import Position

class UserSearchForm(forms.ModelForm):
    """
    Form to be rendered in submitting filters
    when searching for users.
    """
    fullname = forms.CharField(max_length = 30,\
        required = False)

    field_order = ['username',\
        'fullname',\
        'faculty',\
        'program'
    ] 

    labels = {
        'fullname' : 'Name'
    }

    class Meta:
        """
        Uses the fields of the User model as search fields.
        """
        model = User
        fields = ['username',\
            'faculty',\
            'program',\
        ]

    def __init__(self,\
                 *args,\
                 **kwargs):
        """
        Overload default field settings of User model.
        """
        super(UserSearchForm, self).\
            __init__(*args, **kwargs)
        self.order_fields(self.field_order) 
        self.fields['username'].required = False
        self.fields['username'].help_text = None

        
class PositionSearchForm(forms.ModelForm):
    """
    Form to be rendered in submitting filters 
    when searching for users / interview questions 
    associated with a specific position
    """
    class Meta:
        """
        Uses the fields of Position model as search fields. 
        """
        model = Position
        fields = ['company',\
            'title',\
            'start_year',\
            'start_month',\
            'end_year',\
            'end_month',\
            'location_addr',\
            'location_lat',\
            'location_lng',\
        ]

    def __init__(self, *args, **kwargs):
        """
        Fields of parent can be overloaded by
        first calling parent constructor
        """
        super(PositionSearchForm, self).__init__(*args,\
            **kwargs)
        self.fields['company'].required = False
        self.fields['title'].required = False
        self.fields['start_year'].required = False
        self.fields['start_month'].required = False
        self.fields['location_lat'].required = False


            
