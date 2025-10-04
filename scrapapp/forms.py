from django import forms
from .models import *
# from .utils import city_choices

city_choices = [
    # District: Thiruvananthapuram
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Neyyattinkara', 'Neyyattinkara'),
    ('Attingal', 'Attingal'),
    ('Nedumangad', 'Nedumangad'),
    ('Varkala', 'Varkala'),
    ('Kattakada', 'Kattakada'),
    ('Kazhakoottam', 'Kazhakoottam'),
    ('Kovalam', 'Kovalam'),
    ('Poovar', 'Poovar'),
    ('Vizhinjam', 'Vizhinjam'),
    ('Balaramapuram', 'Balaramapuram'),
    ('Chirayinkeezhu', 'Chirayinkeezhu'),
    ('Kilimanoor', 'Kilimanoor'),
    ('Vakkom', 'Vakkom'),
    ('Parassala', 'Parassala'),
    ('Ponmudi', 'Ponmudi'),
    ('Aruvikkara', 'Aruvikkara'),
    ('Karakulam', 'Karakulam'),
    ('Palode', 'Palode'),
    ('Vithura', 'Vithura'),
    ('Aryanad', 'Aryanad'),
    ('Nemom', 'Nemom'),
    ('Kadinamkulam', 'Kadinamkulam'),
    ('Anchuthengu', 'Anchuthengu'),
    ('Edava', 'Edava'),

    # District: Kollam
    ('Kollam', 'Kollam'),
    ('Karunagappally', 'Karunagappally'),
    ('Punalur', 'Punalur'),
    ('Chavara', 'Chavara'),
    ('Mayyanad', 'Mayyanad'),
    ('Paravur', 'Paravur'),
    ('Kundara', 'Kundara'),
    ('Kottarakkara', 'Kottarakkara'),
    ('Ochira', 'Ochira'),
    ('Chathannoor', 'Chathannoor'),
    ('Adichanallur', 'Adichanallur'),
    ('Elampallur', 'Elampallur'),
    ('Kottamkara', 'Kottamkara'),
    ('Thrikkovilvattom', 'Thrikkovilvattom'),
    ('Thazhuthala', 'Thazhuthala'),
    ('Thrikkadavoor', 'Thrikkadavoor'),
    ('Perinad', 'Perinad'),
    ('Meenad', 'Meenad'),
    ('Anchal', 'Anchal'),
    ('Kulathupuzha', 'Kulathupuzha'),
    ('Thenmala', 'Thenmala'),
    ('Sasthamkotta', 'Sasthamkotta'),
    ('Kunnathur', 'Kunnathur'),
    ('Pathanapuram', 'Pathanapuram'),
    ('Neendakara', 'Neendakara'),

    # District: Pathanamthitta
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Thiruvalla', 'Thiruvalla'),
    ('Adoor', 'Adoor'),
    ('Pandalam', 'Pandalam'),
    ('Mallappally', 'Mallappally'),
    ('Konni', 'Konni'),
    ('Kozhencherry', 'Kozhencherry'),
    ('Ranni', 'Ranni'),
    ('Aranmula', 'Aranmula'),
    ('Erviperoor', 'Erviperoor'),
    ('Kadapra', 'Kadapra'),
    ('Kumbanad', 'Kumbanad'),
    ('Pullad', 'Pullad'),
    ('Kuttoor', 'Kuttoor'),
    ('Kaviyoor', 'Kaviyoor'),
    ('Nedumpram', 'Nedumpram'),
    ('Vennikulam', 'Vennikulam'),
    ('Ezhumattoor', 'Ezhumattoor'),
    ('Kalloopara', 'Kalloopara'),
    ('Vadasserikara', 'Vadasserikara'),
    ('Athikayam', 'Athikayam'),
    ('Vechoochira', 'Vechoochira'),
    ('Thadiyoor', 'Thadiyoor'),
    ('Kidangannoor', 'Kidangannoor'),
    ('Kumbazha', 'Kumbazha'),

    # District: Alappuzha
    ('Alappuzha', 'Alappuzha'),
    ('Cherthala', 'Cherthala'),
    ('Kayamkulam', 'Kayamkulam'),
    ('Mavelikara', 'Mavelikara'),
    ('Chengannur', 'Chengannur'),
    ('Haripad', 'Haripad'),
    ('Ambalapuzha', 'Ambalapuzha'),
    ('Aroor', 'Aroor'),
    ('Thuravoor', 'Thuravoor'),
    ('Arookutty', 'Arookutty'),
    ('Ezhupunna', 'Ezhupunna'),
    ('Kanjikuzhy', 'Kanjikuzhy'),
    ('Arthunkal', 'Arthunkal'),
    ('Vayalar', 'Vayalar'),
    ('Kalavoor', 'Kalavoor'),
    ('Purakkad', 'Purakkad'),
    ('Aryad', 'Aryad'),
    ('Thumpoly', 'Thumpoly'),
    ('Valavanadu', 'Valavanadu'),
    ('Pathirappally', 'Pathirappally'),
    ('Punnapra', 'Punnapra'),
    ('Champakulam', 'Champakulam'),
    ('Edathua', 'Edathua'),
    ('Kainakary', 'Kainakary'),
    ('Thakazhy', 'Thakazhy'),

    # District: Kottayam
    ('Kottayam', 'Kottayam'),
    ('Changanassery', 'Changanassery'),
    ('Pala', 'Pala'),
    ('Ettumanoor', 'Ettumanoor'),
    ('Vaikom', 'Vaikom'),
    ('Erattupetta', 'Erattupetta'),
    ('Kanjirappally', 'Kanjirappally'),
    ('Kumarakom', 'Kumarakom'),
    ('Kaduthuruthy', 'Kaduthuruthy'),
    ('Ponkunnam', 'Ponkunnam'),
    ('Mundakayam', 'Mundakayam'),
    ('Erumeli', 'Erumeli'),
    ('Puthuppally', 'Puthuppally'),
    ('Manarcaud', 'Manarcaud'),
    ('Athirampuzha', 'Athirampuzha'),
    ('Bharanaganam', 'Bharanaganam'),
    ('Chempu', 'Chempu'),
    ('Njeezhoor', 'Njeezhoor'),
    ('Vadakkemuri', 'Vadakkemuri'),
    ('Pampady', 'Pampady'),
    ('Chingavanam', 'Chingavanam'),
    ('Ayarkunnam', 'Ayarkunnam'),
    ('Karukachal', 'Karukachal'),
    ('Vazhoor', 'Vazhoor'),
    ('Vakathanam', 'Vakathanam'),

    # District: Idukki
    ('Idukki', 'Idukki'),
    ('Thodupuzha', 'Thodupuzha'),
    ('Kattappana', 'Kattappana'),
    ('Munnar', 'Munnar'),
    ('Devikulam', 'Devikulam'),
    ('Nedumkandam', 'Nedumkandam'),
    ('Kumily', 'Kumily'),
    ('Painavu', 'Painavu'),
    ('Cheruthoni', 'Cheruthoni'),
    ('Adimali', 'Adimali'),
    ('Marayur', 'Marayur'),
    ('Kanthallur', 'Kanthallur'),
    ('Udumbanchola', 'Udumbanchola'),
    ('Peerumede', 'Peerumede'),
    ('Vandiperiyar', 'Vandiperiyar'),
    ('Thekkady', 'Thekkady'),
    ('Kuttikanam', 'Kuttikanam'),
    ('Peermade', 'Peermade'),
    ('Vagamon', 'Vagamon'),
    ('Elappara', 'Elappara'),
    ('Puliyanmala', 'Puliyanmala'),
    ('Rajakumari', 'Rajakumari'),
    ('Chinnakanal', 'Chinnakanal'),
    ('Bison Valley', 'Bison Valley'),
    ('Pallivasal', 'Pallivasal'),

    # District: Ernakulam
    ('Kochi', 'Kochi'),
    ('Aluva', 'Aluva'),
    ('Angamaly', 'Angamaly'),
    ('Perumbavoor', 'Perumbavoor'),
    ('Kothamangalam', 'Kothamangalam'),
    ('Muvattupuzha', 'Muvattupuzha'),
    ('Piravom', 'Piravom'),
    ('Koothattukulam', 'Koothattukulam'),
    ('Tripunithura', 'Tripunithura'),
    ('Kalamassery', 'Kalamassery'),
    ('Thrikkakara', 'Thrikkakara'),
    ('Maradu', 'Maradu'),
    ('Eloor', 'Eloor'),
    ('North Paravur', 'North Paravur'),
    ('Fort Kochi', 'Fort Kochi'),
    ('Mattancherry', 'Mattancherry'),
    ('Edappally', 'Edappally'),
    ('Kakkanad', 'Kakkanad'),
    ('Kalady', 'Kalady'),
    ('Chendamangalam', 'Chendamangalam'),
    ('Cheranallur', 'Cheranallur'),
    ('Choornikkara', 'Choornikkara'),
    ('Edathala', 'Edathala'),
    ('Elamkunnapuzha', 'Elamkunnapuzha'),
    ('Eramalloor', 'Eramalloor'),

    # District: Thrissur
    ('Thrissur', 'Thrissur'),
    ('Kodungallur', 'Kodungallur'),
    ('Irinjalakuda', 'Irinjalakuda'),
    ('Chalakudy', 'Chalakudy'),
    ('Guruvayoor', 'Guruvayoor'),
    ('Kunnamkulam', 'Kunnamkulam'),
    ('Wadakkanchery', 'Wadakkanchery'),
    ('Chavakkad', 'Chavakkad'),
    ('Mala', 'Mala'),
    ('Ollur', 'Ollur'),
    ('Peechi', 'Peechi'),
    ('Mannamangalam', 'Mannamangalam'),
    ('Mulayam', 'Mulayam'),
    ('Vellanikkara', 'Vellanikkara'),
    ('Athirappilly', 'Athirappilly'),
    ('Vazhachal', 'Vazhachal'),
    ('Cheruthuruthy', 'Cheruthuruthy'),
    ('Karalam', 'Karalam'),
    ('Katoor', 'Katoor'),
    ('Koratty', 'Koratty'),
    ('Moonupeedika', 'Moonupeedika'),
    ('Punnayur', 'Punnayur'),
    ('Talikulam', 'Talikulam'),
    ('Thanniyam', 'Thanniyam'),
    ('Vellangallur', 'Vellangallur'),

    # District: Palakkad
    ('Palakkad', 'Palakkad'),
    ('Ottapalam', 'Ottapalam'),
    ('Shornur', 'Shornur'),
    ('Chittur', 'Chittur'),
    ('Pattambi', 'Pattambi'),
    ('Cherpulassery', 'Cherpulassery'),
    ('Mannarkkad', 'Mannarkkad'),
    ('Alathur', 'Alathur'),
    ('Kollengode', 'Kollengode'),
    ('Vadakkanchery', 'Vadakkanchery'),
    ('Nenmara', 'Nenmara'),
    ('Koduvayur', 'Koduvayur'),
    ('Kozhinjamapara', 'Kozhinjamapara'),
    ('Malampuzha', 'Malampuzha'),
    ('Hemambikanagar', 'Hemambikanagar'),
    ('Pirayiri', 'Pirayiri'),
    ('Puthuppariyaram', 'Puthuppariyaram'),
    ('Marutharode', 'Marutharode'),
    ('Pudussery West', 'Pudussery West'),
    ('Pudussery Central', 'Pudussery Central'),
    ('Elappully', 'Elappully'),
    ('Keralassery', 'Keralassery'),
    ('Kodumba', 'Kodumba'),
    ('Kongad', 'Kongad'),
    ('Mankara', 'Mankara'),

    # District: Malappuram
    ('Malappuram', 'Malappuram'),
    ('Manjeri', 'Manjeri'),
    ('Perinthalmanna', 'Perinthalmanna'),
    ('Tirur', 'Tirur'),
    ('Ponnani', 'Ponnani'),
    ('Nilambur', 'Nilambur'),
    ('Kottakkal', 'Kottakkal'),
    ('Kondotty', 'Kondotty'),
    ('Tanur', 'Tanur'),
    ('Parappanangadi', 'Parappanangadi'),
    ('Valanchery', 'Valanchery'),
    ('Edappal', 'Edappal'),
    ('Areekode', 'Areekode'),
    ('Wandoor', 'Wandoor'),
    ('Kalikavu', 'Kalikavu'),
    ('Angadipuram', 'Angadipuram'),
    ('Vengara', 'Vengara'),
    ('Tirurangadi', 'Tirurangadi'),
    ('Kuttippuram', 'Kuttippuram'),
    ('Thirunavaya', 'Thirunavaya'),
    ('Maranchery', 'Maranchery'),
    ('Alamkode', 'Alamkode'),
    ('Tavanur', 'Tavanur'),
    ('Pandikkad', 'Pandikkad'),
    ('Chembrasseri', 'Chembrasseri'),

    # District: Kozhikode
    ('Kozhikode', 'Kozhikode'),
    ('Vadakara', 'Vadakara'),
    ('Koyilandy', 'Koyilandy'),
    ('Feroke', 'Feroke'),
    ('Beypore', 'Beypore'),
    ('Cheruvannur', 'Cheruvannur'),
    ('Kunnamangalam', 'Kunnamangalam'),
    ('Olavanna', 'Olavanna'),
    ('Kakkodi', 'Kakkodi'),
    ('Chelannur', 'Chelannur'),
    ('Ramanattukara', 'Ramanattukara'),
    ('Perumanna', 'Perumanna'),
    ('Kuruvattur', 'Kuruvattur'),
    ('Poolacode', 'Poolacode'),
    ('Mavoor', 'Mavoor'),
    ('Thalakkulathur', 'Thalakkulathur'),
    ('Peruvayal', 'Peruvayal'),
    ('Nanmanda', 'Nanmanda'),
    ('Kuttikkattoor', 'Kuttikkattoor'),
    ('Thazhecode', 'Thazhecode'),
    ('Pantheeramkavu', 'Pantheeramkavu'),
    ('Karuvanthuruthy', 'Karuvanthuruthy'),
    ('Thamarassery', 'Thamarassery'),
    ('Balussery', 'Balussery'),
    ('Mukkam', 'Mukkam'),

    # District: Wayanad
    ('Kalpetta', 'Kalpetta'),
    ('Sulthan Bathery', 'Sulthan Bathery'),
    ('Mananthavady', 'Mananthavady'),
    ('Vythiri', 'Vythiri'),
    ('Meppadi', 'Meppadi'),
    ('Pulpally', 'Pulpally'),
    ('Padinjarathara', 'Padinjarathara'),
    ('Pozhuthana', 'Pozhuthana'),
    ('Muttil', 'Muttil'),
    ('Thirunelli', 'Thirunelli'),
    ('Thavinjal', 'Thavinjal'),
    ('Thondernadu', 'Thondernadu'),
    ('Panamaram', 'Panamaram'),
    ('Ambalavayal', 'Ambalavayal'),
    ('Meenangadi', 'Meenangadi'),
    ('Noolpuzha', 'Noolpuzha'),
    ('Vellamunda', 'Vellamunda'),
    ('Kottathara', 'Kottathara'),
    ('Edakkal', 'Edakkal'),
    ('Lakkidi', 'Lakkidi'),
    ('Tholpetty', 'Tholpetty'),
    ('Kuruva', 'Kuruva'),
    ('Banasura', 'Banasura'),
    ('Cheeral', 'Cheeral'),
    ('Thavinhal', 'Thavinhal'),

    # District: Kannur
    ('Kannur', 'Kannur'),
    ('Thalassery', 'Thalassery'),
    ('Payyanur', 'Payyanur'),
    ('Taliparamba', 'Taliparamba'),
    ('Kuthuparamba', 'Kuthuparamba'),
    ('Mattannur', 'Mattannur'),
    ('Iritty', 'Iritty'),
    ('Anthoor', 'Anthoor'),
    ('Chirakkal', 'Chirakkal'),
    ('Thottada', 'Thottada'),
    ('Madayi', 'Madayi'),
    ('Puzhathi', 'Puzhathi'),
    ('Pappinisseri', 'Pappinisseri'),
    ('Elayavoor', 'Elayavoor'),
    ('Kalliasseri', 'Kalliasseri'),
    ('Cheruthazham', 'Cheruthazham'),
    ('Pallikkunnu', 'Pallikkunnu'),
    ('Azhikode South', 'Azhikode South'),
    ('Muzhappilangad', 'Muzhappilangad'),
    ('Ancharakandy', 'Ancharakandy'),
    ('Azhikode North', 'Azhikode North'),
    ('Munderi', 'Munderi'),
    ('Chelora', 'Chelora'),
    ('Ezhome', 'Ezhome'),
    ('Kadachira', 'Kadachira'),

    # District: Kasaragod
    ('Kasaragod', 'Kasaragod'),
    ('Kanhangad', 'Kanhangad'),
    ('Nileshwar', 'Nileshwar'),
    ('Uppala', 'Uppala'),
    ('Trikaripur', 'Trikaripur'),
    ('Manjeshwar', 'Manjeshwar'),
    ('Bekal', 'Bekal'),
    ('Hosdurg', 'Hosdurg'),
    ('Cheruvathur', 'Cheruvathur'),
    ('Padne', 'Padne'),
    ('Kumbla', 'Kumbla'),
    ('Badiadka', 'Badiadka'),
    ('Chemnad', 'Chemnad'),
    ('Chengala', 'Chengala'),
    ('Kudlu', 'Kudlu'),
    ('Koipady', 'Koipady'),
    ('Puthur', 'Puthur'),
    ('Kunjathur', 'Kunjathur'),
    ('Mangalpady', 'Mangalpady'),
    ('Madhur', 'Madhur'),
    ('Mogral', 'Mogral'),
    ('Shiribagilu', 'Shiribagilu'),
    ('Bangra Manjeshwar', 'Bangra Manjeshwar'),
    ('Shiriya', 'Shiriya'),
    ('Hosabettu', 'Hosabettu'),

]




class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )
    city = forms.ChoiceField(
        choices=[('', 'Select a city')] + city_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'city', 'role', 'password']
        labels = {
            'role': 'Are you a dealer/seller?',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            # 'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password"
    )

class ProfileForm(forms.ModelForm):
    city = forms.ChoiceField(
        choices=[('', 'Select a city')] + city_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'city', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            # 'city': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
        
class ScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = ScrapCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }

class DealerRateForm(forms.ModelForm):
    class Meta:
        model = DealerRate
        fields = ['category', 'rate_per_kg']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'rate_per_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₹ per KG'}),
        }


class PickupRequestForm(forms.ModelForm):
    city = forms.ChoiceField(
        choices=[('', 'Select a city')] + city_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    preferred_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        label="Preferred pickup date & time (optional)"
    )
    class Meta:
        model = PickupRequest
        fields = ['address', 'city', 'preferred_datetime']
        widgets = {
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class PickupItemForm(forms.ModelForm):
    class Meta:
        model = PickupItem
        fields = ['category', 'approx_weight']
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "approx_weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
        }


class DealerPickupForm(forms.ModelForm):
    class Meta:
        model = DealerPickup
        fields = ['recyclable_total', 'verified_total']
        widgets = {
            "recyclable_total": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "verified_total": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
        }

class DealerPickupItemForm(forms.ModelForm):
    class Meta:
        model = DealerPickupItem
        fields = ['category', 'actual_weight']
        widgets = {
            "category": forms.Select(attrs={"class": "form-control", "readonly": "readonly"}),
            "actual_weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
        }

class DealerScheduleForm(forms.ModelForm):
    scheduled_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"})
    )
    class Meta:
        model = DealerPickup
        fields = ['scheduled_datetime']

class SellerRescheduleForm(forms.ModelForm):
    requested_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"})
    )
    class Meta:
        model = RescheduleRequest
        fields = ['requested_datetime', 'reason']
        widgets = {'reason': forms.Textarea(attrs={'class':'form-control','rows':3})}
        
class PickupFeedbackForm(forms.ModelForm):
    class Meta:
        model = PickupFeedback
        fields = ["fair", "action_against_dealer", "satisfied", "thoughts"]
        widgets = {
            "thoughts": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Share your thoughts..."}),
        }