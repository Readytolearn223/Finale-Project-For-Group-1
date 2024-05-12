import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'account/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1,pass2)

        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Congrats! You now have an account.")
        return redirect('music_quiz')
    return render(request, 'account/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('music_quiz')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('music_quiz')
    else:
        return render(request, 'account/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully! ")
    return redirect('home')

artists_and_songs = { 
    'Indie/Alternative': {
        'Arcade Fire': ['Wake Up', 'The Suburbs', 'Rebellion (Lies)', 'Reflektor', 'No Cars Go'],
        'Tame Impala': ['The Less I Know the Better', 'Feels Like We Only Go Backwards', 'Elephant', 'Let It Happen', 'Borderline']
    },
    'Pop': {
        'Ariana Grande': ['thank u, next', '7 rings', 'God is a woman', 'Into You', 'no tears left to cry'],
        'Ed Sheeran': ['Shape of You', 'Thinking Out Loud', 'Castle on the Hill', 'Perfect', 'Photograph']
    },
    'Rap/Hip-Hop': {
        'J. Cole': ['No Role Modelz', 'Middle Child', 'Love Yourz', 'Wet Dreamz', 'Power Trip'],
        'Eminem': ['Lose Yourself', 'Stan', 'Not Afraid', 'The Real Slim Shady', 'Mockingbird']
    },
    'Rock': {
       'Kendrick Lamar': ['HUMBLE.', 'DNA.', 'Alright', 'Swimming Pools (Drank)', 'Money Trees'],
       'Drake': ['God"s Plan', 'Hotline Bling', 'In My Feelings', 'Started From the Bottom', 'One Dance']
    },
    'R&B': {
       'Beyoncé': ['Halo', 'Crazy in Love', 'Irreplaceable', 'Love On Top', 'Single Ladies (Put a Ring on It)'],
       'Frank Ocean': ['Thinkin Bout You', 'Nights', 'Pink + White', 'Solo', 'Chanel']
    }
}

def select_random_artist_and_song(recommended_artists_and_songs):
    random_artist = random.choice(list(recommended_artists_and_songs.keys()))
    random_song = random.choice(recommended_artists_and_songs[random_artist])
    return random_artist, random_song

def music_quiz(request):
    if request.method == 'POST':
        
        rap_hiphop = 0
        indie_alt = 0
        rb = 0
        pop = 0
        rock = 0
        answers = request.POST
        answer_q1 = answers.get('q1', '')
        if answer_q1 == 'A':
            rap_hiphop += 2
            rock += 2
            pop += 2
        elif answer_q1 == 'B':
            indie_alt += 2
            rb += 2
        elif answer_q1 == 'C':
            indie_alt += 2
            rb += 2
        else:
            rap_hiphop += 2
            pop += 2

        #Question 2
        answer_q2 = answers.get('q2', '')
        if answer_q2 == 'A':
            pop += 3
        elif answer_q2 == 'B':
            rap_hiphop += 3
        elif answer_q2 == 'C':
            indie_alt += 3
        elif answer_q2 == 'D':
            rb += 3
        else:
            rock += 3

        #Question 3
        answer_q3 = answers.get('q3', '')
        if answer_q3 == 'A':
            indie_alt += 1
        elif answer_q3 == 'B':
            indie_alt += 1
        elif answer_q3 == 'C':
            pop += 1
        elif answer_q3 == 'D':
            rb += 1
        elif answer_q3 =='E':
            rock += 1
        else:
            rap_hiphop += 1

    
        #Question 4
        answer_q4 = answers.get('q4', '')
        if answer_q4 == 'A':
            indie_alt += 2
            rb += 2
        else:
            pop += 2
            rock += 2
            rap_hiphop += 2


        #Question 5
        answer_q5 = answers.get('q5', '')
        if answer_q5 == 'A':
            indie_alt += 3
        elif answer_q5 == 'B':
            pop += 3
        elif answer_q5 == 'C':
            rap_hiphop += 3
        elif answer_q5 == 'D':
            rock += 3
        else:
            rb += 3

        genre_score = max(indie_alt, pop, rap_hiphop, rock, rb)

        if indie_alt == genre_score:
            recommended_genre = 'Indie/Alternative'
        elif pop == genre_score:
            recommended_genre = 'Pop'
        elif rap_hiphop == genre_score:
            recommended_genre = 'Rap/Hip-Hop'
        elif rock == genre_score:
            recommended_genre = 'Rock'
        else:
            recommended_genre = 'R&B'
        recommended_artists_and_songs = artists_and_songs[recommended_genre]
        random_artist, random_song = select_random_artist_and_song(recommended_artists_and_songs)
        return render(request, 'account/results.html', {
        'recommended_genre': recommended_genre,
        'random_artist': random_artist,
        'random_song': random_song
    })
    else:
        return render(request, 'account/music_quiz.html')