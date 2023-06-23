from django import forms
from ItemMasterData.models import Item,Warehouse
class SalesOrderForm(forms.Form):
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')

class SalesOrderNumberForm(forms.Form):
    order_number = forms.IntegerField(label='Order Number')
    class Meta:
        fields = ['order_number']    
    def __init__(self, *args, **kwargs):
        super(SalesOrderNumberForm, self).__init__(*args, **kwargs)


     
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })  

class ItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)


    class Meta:
        model = Item
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):


        super(ItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })    
            
            
class SearchForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['description'].required = False

     
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })  