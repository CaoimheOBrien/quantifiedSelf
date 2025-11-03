import json
from collections import Counter
from collections import defaultdict
import csv
import glob #global
import sys

#======================================================================================================================================================
#Getting the data
#Loading in JSON data
sys.stdout= open("InfoFromSpotify.txt", "w")  # writes everything from the shell into a text file
data = [] # empty data set 
for file in glob.glob("StreamingHistory*.json"): # loads all the JSON files into one big file bc there are 3 
    with open(file, 'r', encoding='utf-8') as f:
        data.extend(json.load(f))

trackCounts = Counter() #Getting Count plays / track & artist  pair

for entry in data:
    artist = entry.get("artistName") # gets every artist in the file
    track = entry.get("trackName") # gets every track name in the file
    if artist and track: # data validation check for incomplete entries (just to be safe)
        trackCounts[(track, artist)] +=1 # adds to the track counter
        
#======================================================================================================================================================
#Data by plays
# What are my top 50 by plays 
top50plays = trackCounts.most_common(50)
        
print("My top 50 tracks by plays are: \n")
for i , ((track, artist), count)in enumerate(top50plays, start=1): # writes as a numbered list
    print(f"{i:2d}. {track} — {artist} ({count} plays)")
print("\n")

artistsPlays = Counter()

for (track, artist), count in trackCounts.items():
    artistsPlays[artist] += count
    
top5ArtistPlays = artistsPlays.most_common(5)

print ("\nMost listened-to artist by plays:")
for artist, plays in top5ArtistPlays:
    print(f"{artist} ({plays} plays)")
    
print("\n")

hozierSongsPlays = [(track, artist, count) for (track, artist), count in top50plays if "hozier" in artist.lower()] # filters out just the hozier songs
print ("My Hozier top tracks by plays:")
for track, artist, count in hozierSongsPlays:
    print (f"-{track} ({count} plays)")

sabrinaSongsPlays= [(track, artist, count) for (track, artist), count in top50plays if "sabrina carpenter" in artist.lower()] # filters out just the sabrina carpenter songs
print ("\nMy Sabrina Carpenter top tracks by plays:")
for track, artist, count in sabrinaSongsPlays:
    print (f"-{track} ({count} plays)")

print("\n\n")

#======================================================================================================================================================
# By total Time played
listeningTime = defaultdict(int)

for entry in data: 
    artist = entry.get("artistName") # gets artist name like last time
    track = entry.get("trackName") #gets track name like last time
    msPlayed = entry.get("msPlayed", 0) # Also gets the ms played to how long I've played each track
    if artist and track:
        listeningTime[(track, artist)] += msPlayed # if this track and artist have been counted already, it will add this new entry of msPlayed onto the old value
        
top50time = sorted(listeningTime.items(), key=lambda x: x[1], reverse=True)[:50] # converts to minutes then put into a new var
  
print("My top 50 tracks by ms played are: ")
for i , ((track, artist), count)in enumerate(top50time, start=1): # writes as a numbered list 
    print(f"{i:2d}. {track} — {artist} ({count} ms)")

artistTime = defaultdict(int)

for (track, artist), ms in listeningTime.items():
    artistTime[artist] += ms

artistTimeMinutes = {artist: round(ms / 60000, 2) for artist, ms in artistTime.items()}

top5ArtistsTime = sorted(artistTimeMinutes.items(), key=lambda x: x[1], reverse=True)[:5]

print ("\nMost listened-to artist by time:")
for artist, minutes in top5ArtistsTime:
    print(f"{artist} : {minutes} minutes")
    
print("\n")

hozierSongsTime = [(track, artist, count) for (track, artist), count in top50time if "hozier" in artist.lower()] # filters out just the hozier songs
print ("My Hozier top tracks by time played:")
for track, artist, count in hozierSongsTime:
    print (f"-{track} ({count} seconds)")


sabrinaSongsTime = [(track, artist, count) for (track, artist), count in top50time if "sabrina carpenter" in artist.lower()] # filters out just the sabrina carpenter songs
print ("\nMy Sabrina Carpenter top tracks by time played:")
for track, artist, count in sabrinaSongsTime:
    print (f"-{track} ({count} seconds)")
 
#Comparing both:
playsSet = set((track, artist) for track, artist, _ in hozierSongsPlays) # extracts artist and track name from the hozier songs by plays list

timeSet = set((track, artist) for track, artist, _ in hozierSongsTime) # extracts the same from the hozier songs by time list

inBoth = playsSet & timeSet # intersection
onlyInPlays = playsSet - timeSet #songs that only appear in plays
onlyInTime = timeSet - playsSet # songs only in times set


print(f"\nHozier songs ranked by plays: {len(playsSet)}")
print(f"Hozier songs ranked by listening time: {len(timeSet)}")
print(f"Songs appearing in both: {len(inBoth)}")

if onlyInPlays: # prints if  songs are only in plays
    print("\nSongs only in plays list:")
    for t, a in onlyInPlays:
        print("-", t)
else:
    print ("\nNo songs only in plays list")
    
if onlyInTime: # prints songs that are only in time list
    print("\nSongs only in listening time list:")
    for t, a in onlyInTime:
        print("-", t)
else:
    print ("\nNo songs only in time list")
    

#Put into a CSV
top50TimeMinutes = [(track, artist, round(ms/60000, 2)) for (track, artist), ms in top50time] # converts into minutes
allTracks = set((track, artist) for (track, artist), _ in top50plays) | set((track, artist) for (track, artist), _ in top50time)

with open("hozierComparison.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Track", "Artist", "Plays", "Minutes Listened", "isHozier"])
    
    for trackName, artistName in allTracks:
        plays = next((count for (t, a), count in top50plays if t == trackName and a == artistName), 0) # Get plays
        minutes = next((m for t, a, m in top50TimeMinutes if t == trackName and a == artistName), 0) # Get minutes
        isHozier = "Yes" if "Hozier" in artistName else "No"  # checks if hozier
        writer.writerow([trackName, artistName, plays, minutes, isHozier]) # writes row into CSV file

sys.stdout.close()
print("\n\nhozierComparison.csv saved successfully!")
