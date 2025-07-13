import time
import keyboard
import vlc
from os import path
# from random import randrange  ## optional, possible implement for parsing through dialogue_sound.

key_input_list = []  ## list of all the keys that have been input.
syllables_int = 0  ## syllables, determines how many times the vlc object is played.
music_vlc = None  ## vlc MediaPlayer object for playing dialogue audio.
typing_bool = False  ## determines if beeps should be played when text is input.
full_bool = False  ## while typing_bool, determines if extra inputs can be appended.

repeat_a_bool = False
repeat_b_bool = False

## USER-MODIFIABLE VARIABLES

input_delay = 0.04  ## the amount of time in-between recording keyboard inputs.
typing_limit_int = 10  ## while not typing_bool, the hard-coded input limit
dialogue_delay = 0.09  ## the amount of time in-between dialogue sounds being played.
dialogue_sound = "SYN_BEEP-2.mp3"  ## the sound file (within folder "sounds") used for "dialogue".
dialogue_limit_int = -1  ## while typing_bool, the hard-coded input limit


def get_syllables(letters_list):
    # vowels = ["a", "e", "i", "o", "u", "y"]  # UNUSED

    syllables = 0  # final return val
    word_list = []  # letters joined to make a list in a sentence
    word_str = ""  # final string from word_list
    word_str_len = 0  # length of word_str (for simplification)
    for letter in letters_list:
        if letter in ["space", "enter"]:  ## space/enter does not account for any syllable
            ## dodgy way of doing it, but it works for a small project
            if letter == "space":
                letters_list.pop(letters_list.index("space"))
            elif letter == "enter":
                letters_list.pop(letters_list.index("enter"))
            else:
                pass

            word_str = "".join(word_list)
            word_str_len = len(word_str)
            if word_str_len >= 1:
                syllables += 1

            ## apply syllable rules here [below]

            if word_str_len <= 4:
                pass
            else:
                syllables += word_str_len / 3
                if syllables % 1 != 0:
                    syllables = syllables // 1
                else:
                    syllables -= 1

                ## rather than using fancy syllable rules, i assumed each/any syllable would
                ## be approx. 3 characters long. hence, any remainders from a division of 3
                ## can be accounted for as an "excess"/+1 to the syllable counter.
                ## this... doesn't work for the word "mitochondria", but it IS cheap to deploy.
                ## (vowels exists due to having another idea for implementation).

            word_list.clear()
        else:
            word_list.append(letter)
    return syllables


while True:

    while syllables_int >= 1:
        # print(f"NEED TO GET RID OF THIS {syllables_int}!")
        if music_vlc is not None:  # something is playing
            if music_vlc.get_length() > 0 and music_vlc.is_playing() == 0:  # -> when it loads
                # print(music_vlc.is_playing())
                # print(music_vlc.get_time())
                # print(music_vlc.get_length())

                ## one very stupid thing i'd like to note here:
                ## apparently, even when the vlc library has loaded in a media file and even
                ## when that media file has been given the command to play, vlc will still
                ## mark the media file as "not playing" when checking via .is_playing() function.
                ## and an even stupider thing is that .is_playing() returns a binary 1 or 0
                ## rather than bool.
                ## hence, that explains the tedious "pause()/play()" functions you will see.

                if int(music_vlc.get_time()) >= (int(music_vlc.get_length()) - 400):  # acc 4 error
                    music_vlc.pause()
                    music_vlc = None
                    time.sleep(dialogue_delay)
        else:  # something is not playing (so play something)
            music_vlc = vlc.MediaPlayer(path.join("sounds", dialogue_sound))

            ## the below would add differing pitches, but apparently this code borks it up :p
            # music_vlc.set_rate(round(randrange(1, 21, 1) / 100, 2))

            music_vlc.play()
            syllables_int -= 1

    if syllables_int == 0:  ## this should ideally be done above/already.
        music_vlc = None
    else:
        pass

    if len(key_input_list) > typing_limit_int and not typing_bool:
        key_input_list = []
    elif len(key_input_list) > dialogue_limit_int > 0 and typing_bool:
        full_bool = True
    else:
        full_bool = False

    if not repeat_a_bool and not repeat_b_bool:  ## "workaround" for multiple recorded key inputs.
        if not full_bool:
            key_input_list.append(str(keyboard.read_event().name))
    elif repeat_a_bool:
        repeat_a_bool = not repeat_b_bool
    else:
        repeat_b_bool = not repeat_b_bool

    # print(repeat_a_bool, repeat_b_bool, key_input_list)
    time.sleep(input_delay)
    # print(key_input_list[0])

    # print(key_input_list[-2:-1])
    # print(key_input_list[-3:-2])

    if key_input_list[-1:] == ["/"]:
        typing_bool = True  ## enabled with "/", actually recorded.
        key_input_list = []
        print("++You are now typing!++")
    else:
        pass

    if key_input_list[-1:] == ["enter"] and typing_bool:
        typing_bool = False  ## and disabled with enter, i.e., when you enter the text.
        print("--You are no longer typing!--")
        syllables_int = get_syllables(key_input_list) + 1  # +1 makes it sound better, from tests.
        print(syllables_int)
        key_input_list.clear()
    elif key_input_list[-1:] == ["backspace"] and len(key_input_list) > 1:
        # if key_input_list[-2:-1] == ["ctrl"] or key_input_list[-3:-2] == ["ctrl"]:
        if ["ctrl"] in [key_input_list[-2:-1], key_input_list[-3:-2]] and len(key_input_list) > 2:
            print(key_input_list[-2:-1])
            print(key_input_list[-3:-2])
            if key_input_list[-2:-1] == ["a"]:
                key_input_list = []  ## get rid of everything (ctrl + a + backspace)
            ## ctrl + a functionality can bug out where 2 "a" inputs are detected.
            else:
                key_input_list.pop()  ## get rid of backspace
                key_input_list.pop()  ## get rid of ctrl
                while key_input_list[-1:] != ["space"]:
                    key_input_list.pop()  ## get rid of entire element stack (ctrl + backspace)
        else:
            key_input_list.pop()  ## get rid of backspace
            key_input_list.pop()  ## get rid of one element (backspace)
