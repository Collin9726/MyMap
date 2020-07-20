import folium
import random
import string
from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .email import send_signup_email_admin, send_signup_email_resident
from .models import Admin_Profile, Neighbourhood, Resident_Profile, Facility, Business
from .forms import AdminProfileForm, NeighbourhoodForm, AddResidentForm, FacilityForm

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    admin_profile = None
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        pass

    resident_profile = None
    try:
        resident_profile = Resident_Profile.objects.get(this_user = current_user)
    except Resident_Profile.DoesNotExist:
        pass

    if admin_profile:
        return redirect(my_admin_profile)
    elif resident_profile:
        return redirect(my_user_profile)
    else:
        raise Http404    

@login_required(login_url='/accounts/login/')
def send_email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_signup_email_admin(name, email)
    return redirect(create_profile_admin)


@login_required(login_url='/accounts/login/')
def create_profile_admin(request):
    current_user = request.user
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.this_user = current_user
            profile.save()
        return redirect(create_hood)

    else:
        form = AdminProfileForm()
      
    title = "Admin profile "
    return render(request, 'create-profile-admin.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def create_hood(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()

    my_hood = None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        pass

    if my_hood:
        return redirect(my_admin_profile)

    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = admin_profile
            hood.save()
        return redirect(my_admin_profile)

    else:
        form = NeighbourhoodForm()
      
    title = "Create Hood"
    return render(request, 'create-hood.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def my_admin_profile(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()

    my_hood =None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    if my_hood:
        longitude = my_hood.location[0]
        latitude = my_hood.location[1]
    

    m = folium.Map(location=[latitude, longitude], zoom_start=17)
    folium.Marker([latitude,longitude],
                    popup='<h5>My neighbourhood.</h5>',
                    tooltip=f'{my_hood.hood_name}',
                    icon=folium.Icon(icon='glyphicon-home', color='blue')).add_to(m),
    hospitals = Facility.objects.filter(category='hospital')
    police_posts = Facility.objects.filter(category='police')
    for hospital in hospitals:
        hosp_longitude = hospital.location[0]
        hosp_latitude = hospital.location[1]
        folium.Marker([hosp_latitude,hosp_longitude],
                    popup=f'<p>{hospital.contact}</p>',
                    tooltip=f'{hospital.facility_name}',
                    icon=folium.Icon(icon='glyphicon-plus-sign', color='purple')).add_to(m), 
    for post in police_posts:
        post_longitude = post.location[0]
        post_latitude = post.location[1]
        folium.Marker([post_latitude,post_longitude],
                    popup=f'<p>{post.contact}</p>',
                    tooltip=f'{post.facility_name}',
                    icon=folium.Icon(icon='glyphicon-flag', color='darkgreen')).add_to(m), 

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=200,
        popup=f'{my_hood.hood_name}',
        color='#428bca',
        fill=True,
        fill_color='#428bca'
    ).add_to(m),

    map_page = m._repr_html_()    
      
    title = admin_profile.this_user.username
    return render(request, 'my-admin-profile.html', {"profile": admin_profile, "title": title, "hood": my_hood, "map_page":map_page})


@login_required(login_url='/accounts/login/')
def add_resident(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()

    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        form = AddResidentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            this_resident =User.objects.create_user(username, email, password)
            resident_profile = Resident_Profile(full_name=name, this_user=this_resident, username=username, hood=my_hood)
            resident_profile.save()
            my_hood.occupants_count = len(Resident_Profile.objects.filter(hood = my_hood))+1
            my_hood.save()
            send_signup_email_resident(name, username, password,admin_profile.full_name, my_hood.hood_name, email)
            
        return redirect(my_admin_profile)

    else:
        form = AddResidentForm()
      
    title = "Add resident"
    return render(request, 'add-resident.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def update_hood(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        pass

    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            my_hood.hood_name = form.cleaned_data['hood_name']
            my_hood.location = form.cleaned_data['location']
            my_hood.save()
        return redirect(my_admin_profile)

    else:
        form = NeighbourhoodForm()
      
    title = "Update Hood"
    return render(request, 'update-hood.html', {"form": form, "title": title})



@login_required(login_url='/accounts/login/')
def delete_hood(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        pass

    admin_profile.delete()
    current_user.delete()

    return redirect(index)



@login_required(login_url='/accounts/login/')
def add_facility(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        pass    

    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.hood = my_hood
            facility.save()
        return redirect(my_admin_profile)

    else:
        form = FacilityForm()
      
    title = "Add Facility"
    return render(request, 'add-facility.html', {"form": form, "title": title})



@login_required(login_url='/accounts/login/')
def my_user_profile(request):
    current_user = request.user
    try:
        resident_profile = Resident_Profile.objects.get(this_user = current_user)
    except Resident_Profile.DoesNotExist:
        raise Http404()

    my_hood = resident_profile.hood
    longitude = my_hood.location[0]
    latitude = my_hood.location[1]       

    m = folium.Map(location=[latitude, longitude], zoom_start=17)
    folium.Marker([latitude,longitude],
                    popup='<h5>My neighbourhood.</h5>',
                    tooltip=f'{my_hood.hood_name}',
                    icon=folium.Icon(icon='glyphicon-home', color='blue')).add_to(m),
    hospitals = Facility.objects.filter(category='hospital')
    police_posts = Facility.objects.filter(category='police')
    for hospital in hospitals:
        hosp_longitude = hospital.location[0]
        hosp_latitude = hospital.location[1]
        folium.Marker([hosp_latitude,hosp_longitude],
                    popup=f'<p>{hospital.contact}</p>',
                    tooltip=f'{hospital.facility_name}',
                    icon=folium.Icon(icon='glyphicon-plus-sign', color='purple')).add_to(m), 
    for post in police_posts:
        post_longitude = post.location[0]
        post_latitude = post.location[1]
        folium.Marker([post_latitude,post_longitude],
                    popup=f'<p>{post.contact}</p>',
                    tooltip=f'{post.facility_name}',
                    icon=folium.Icon(icon='glyphicon-flag', color='darkgreen')).add_to(m), 

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=200,
        popup=f'{my_hood.hood_name}',
        color='#428bca',
        fill=True,
        fill_color='#428bca'
    ).add_to(m),

    map_page = m._repr_html_()    
      
    title = resident_profile.username
    return render(request, 'my-user-profile.html', {"profile": resident_profile, "title": title, "hood": my_hood, "map_page":map_page})


@login_required(login_url='/accounts/login/')
def delete_resident_profile(request):
    current_user = request.user
    try:
        resident_profile = Resident_Profile.objects.get(this_user = current_user)
    except Resident_Profile.DoesNotExist:
        raise Http404()
    resident_profile.delete()
    current_user.delete()
    
    return redirect(index)