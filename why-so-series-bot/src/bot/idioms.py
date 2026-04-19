import re

# Common English idioms and phrases with meanings
IDIOMS = {
    "break a leg": "Good luck",
    "hit the sack": "Go to sleep",
    "under the weather": "Feeling sick",
    "bite the bullet": "Endure a painful situation",
    "spill the beans": "Reveal a secret",
    "let the cat out of the bag": "Accidentally reveal a secret",
    "cost an arm and a leg": "Very expensive",
    "once in a blue moon": "Very rarely",
    "piece of cake": "Something very easy",
    "beat around the bush": "Avoid the main topic",
    "blow off steam": "Release anger or stress",
    "by the skin of your teeth": "Just barely",
    "cut corners": "Do something the easy or cheap way",
    "give the benefit of the doubt": "Trust someone despite uncertainty",
    "go back to the drawing board": "Start over",
    "hang in there": "Don't give up",
    "hit the nail on the head": "Exactly right",
    "kill two birds with one stone": "Accomplish two things at once",
    "let sleeping dogs lie": "Don't stir up old problems",
    "miss the boat": "Miss an opportunity",
    "not my cup of tea": "Not something I enjoy",
    "on the fence": "Undecided",
    "pull someone's leg": "Joke or tease someone",
    "see eye to eye": "Agree with someone",
    "sit on the fence": "Avoid taking a side",
    "speak of the devil": "Said when someone appears just after being mentioned",
    "straight from the horse's mouth": "Directly from the source",
    "the best of both worlds": "Enjoy two advantages at once",
    "time flies": "Time passes quickly",
    "under the radar": "Going unnoticed",
    "up in the air": "Uncertain or undecided",
    "you can't judge a book by its cover": "Don't judge by appearances",
    "bite off more than you can chew": "Take on more than you can handle",
    "burning bridges": "Destroying relationships",
    "caught red-handed": "Caught in the act",
    "don't cry over spilled milk": "Don't worry about past mistakes",
    "every cloud has a silver lining": "Every bad situation has a positive side",
    "face the music": "Accept consequences",
    "get out of hand": "Lose control",
    "get the ball rolling": "Start something",
    "hit the books": "Study hard",
    "in hot water": "In trouble",
    "jump on the bandwagon": "Follow a trend",
    "keep your chin up": "Stay positive",
    "learn the ropes": "Learn the basics",
    "no pain no gain": "Hard work leads to success",
    "the elephant in the room": "An obvious problem no one mentions",
    "throw in the towel": "Give up",
    "under pressure": "Stressed or forced",
    "wrap your head around": "Understand something complex",
}


def find_idioms(text: str) -> list[dict]:
    """
    Search for known idioms in the subtitle text.
    Returns a list of dicts with 'phrase' and 'meaning'.
    """
    text_lower = text.lower()
    found = []

    for phrase, meaning in IDIOMS.items():
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, text_lower):
            found.append({
                'phrase': phrase,
                'meaning': meaning
            })

    return found
