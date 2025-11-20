import streamlit as st
import random
import csv

# ------------------------
# Basic page settings
# ------------------------
st.set_page_config(
    page_title="Chinese Word Island Adventure",
    page_icon="🎮",
    layout="centered",
)

# ------------------------
# Helper: safe rerun for different Streamlit versions
# ------------------------
def do_rerun():
    """Call Streamlit's rerun API (works for both old/new versions)."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# ============================================
# Load word bank from CSV file
# ============================================

def load_word_bank_from_csv(path: str):
    """
    Load word bank from a CSV file.

    CSV columns (header):
        category, hanzi, pinyin, english

    Returns:
        dict: {category: [ {hanzi, pinyin, english}, ... ]}
    """
    word_bank = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["category"].strip()
            entry = {
                "hanzi": row["hanzi"].strip(),
                "pinyin": row["pinyin"].strip(),
                "english": row["english"].strip(),
            }
            if category not in word_bank:
                word_bank[category] = []
            word_bank[category].append(entry)
    return word_bank


# 👇 Load your whole CSV word bank
WORD_BANK = load_word_bank_from_csv("word_bank.csv")


# ============================================
# Helpers: generate questions for Levels 1–7
# ============================================

def generate_family_question():
    """
    Level 1 (Family Village):
    Generate 4 words:
    - 2 words are family members
    - 2 words are from other categories (distractors)
    """
    family_words = WORD_BANK["family"]
    correct_words = random.sample(family_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "family"
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


def generate_fruit_question():
    """
    Level 2 (Fruit Manor):
    Generate 4 words:
    - 2 words are fruits
    - 2 words are from other categories (distractors)
    """
    fruit_words = WORD_BANK["fruit"]
    correct_words = random.sample(fruit_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "fruit"
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


def generate_animal_spy_question():
    """
    Level 3 (Zoo Spy):
    Generate 6 words total:
    - 4 words are animals
    - 2 words are NOT animals (impostors)
    Player must find the 2 impostors.
    """
    animal_words = WORD_BANK["animal"]
    animals = random.sample(animal_words, k=4)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "animal"
        for w in words
    ]
    impostors = random.sample(other_pool, k=2)

    options = animals + impostors
    random.shuffle(options)

    impostor_set = {w["hanzi"] for w in impostors}
    return options, impostor_set


def generate_verb_question():
    """
    Level 4 (Verb Volcano):
    Generate 4 words:
    - 2 words are action verbs
    - 2 words are from other categories (distractors)
    """
    verb_words = WORD_BANK["verb"]
    correct_words = random.sample(verb_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "verb"
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


def generate_place_question():
    """
    Level 5 (City Maze):
    Generate 4 words:
    - 2 words are places
    - 2 words are from other categories (distractors)
    """
    place_words = WORD_BANK["place"]
    correct_words = random.sample(place_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "place"
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


def generate_time_question():
    """
    Level 6 (Time Tunnel):
    Generate 4 words:
    - 2 words are time words
    - 2 words are from other categories (distractors)
    """
    time_words = WORD_BANK["time"]
    correct_words = random.sample(time_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "time"
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


def generate_job_question():
    """
    Level 7 (Career Town):
    Generate 4 words:
    - 2 words are jobs / professions
    - 2 words are from other categories (distractors)
    """
    job_words = WORD_BANK["job"]
    correct_words = random.sample(job_words, k=2)

    other_pool = [
        w
        for category, words in WORD_BANK.items()
        if category != "job"      
        for w in words
    ]
    distractors = random.sample(other_pool, k=2)

    options = correct_words + distractors
    random.shuffle(options)

    correct_set = {w["hanzi"] for w in correct_words}
    return options, correct_set


# ---------- Final Trial helper (Level 8) ----------

def generate_final_trial_words():
    """
    Level 8 (Final Trial: Vocabulary Chaos)

    Pick exactly 1 word from each category:
    family, fruit, animal, verb, place, time, job
    Total: 7 words, shuffled.

    Each item: {hanzi, pinyin, english, category}
    """
    categories = ["family", "fruit", "animal", "verb", "place", "time", "job"]
    final_words = []

    for cat in categories:
        base = random.choice(WORD_BANK[cat])
        final_words.append({
            "hanzi": base["hanzi"],
            "pinyin": base["pinyin"],
            "english": base["english"],
            "category": cat,
        })

    random.shuffle(final_words)
    return final_words


# ------------------------
# Initialize session state
# ------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"      # "intro" / "game"

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "level" not in st.session_state:
    st.session_state.level = 1           # 1..8


def reset_game_state():
    """Reset game-related state when starting or restarting."""
    st.session_state.lives = 3
    st.session_state.level = 1
    for key in [
        # Level 1
        "family_options", "family_correct",
        "level1_show_result", "level1_is_correct", "level1_correct_words",
        # Level 2
        "fruit_options", "fruit_correct",
        "level2_show_result", "level2_is_correct", "level2_correct_words",
        # Level 3
        "zoo_options", "zoo_impostors",
        "level3_show_result", "level3_is_correct", "level3_correct_impostors",
        # Level 4
        "verb_options", "verb_correct",
        "level4_show_result", "level4_is_correct", "level4_correct_words",
        # Level 5
        "place_options", "place_correct",
        "level5_show_result", "level5_is_correct", "level5_correct_words",
        # Level 6
        "time_options", "time_correct",
        "level6_show_result", "level6_is_correct", "level6_correct_words",
        # Level 7
        "job_options", "job_correct",
        "level7_show_result", "level7_is_correct", "level7_correct_words",
        # Level 8
        "final_words", "final_show_result", "final_is_correct_enough",
        "final_answers", "final_detailed_result", "final_accuracy",
    ]:
        if key in st.session_state:
            del st.session_state[key]


def go_to_game():
    """Move from intro page to game page (only if name is not empty)."""
    name = st.session_state.player_name.strip()
    if not name:
        st.warning("Please enter your explorer name first.")
    else:
        reset_game_state()
        st.session_state.page = "game"


# ------------------------
# Background image: island adventure
# ------------------------
BACKGROUND_URL = "https://f4.bcbits.com/img/a2060336255_16.jpg"

page_bg = f"""
<style>
.stApp {{
    background-image: url('{BACKGROUND_URL}');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Main content container: white translucent card so text is readable */
.block-container {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem 2.5rem;
    border-radius: 1.2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.20);
    margin-top: 2rem;
    margin-bottom: 2rem;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
# ------------------------
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------------
# Background music (play at top of page)
# ------------------------
def load_bgm():
    try:
        with open("bgm_8bit_menu.mp3", "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

bgm_bytes = load_bgm()

if bgm_bytes:
    st.audio(bgm_bytes, format="audio/mp3", start_time=0)

# ------------------------
# INTRO PAGE
# ------------------------
if st.session_state.page == "intro":
    st.title("Chinese Word Island Adventure")

    st.markdown(
        """
Welcome to the **Chinese Word Island!**  
All the Chinese words here once lived together in peace.

One day, a shadowy monster called **Lexor** 👺 descended on the island.  
He kidnapped families 👨‍👩‍👧‍👦, turned sweet fruits 🍎🍉 into cold stone 🪨,  
and pushed the animals 🐶🐱🐼 into a thick, swirling fog 😱...

Now, **only you** can save the island.  
Use your word power to defeat Lexor!🗡️
        """
    )

    st.markdown("---")

    st.markdown("### Enter your explorer name")
    st.session_state.player_name = st.text_input(
        "",
        value=st.session_state.player_name,
        placeholder="Type your name here...",
    )

    if st.button("Start Adventure"):
        go_to_game()


# ======================================================
# GAME PAGE: different content by level
# ======================================================
elif st.session_state.page == "game":
    name = st.session_state.player_name.strip() or "Explorer"

    # ------------- LEVEL 1: FAMILY VILLAGE -------------
    if st.session_state.level == 1:

        if "level1_show_result" not in st.session_state:
            st.session_state.level1_show_result = False
        if "level1_is_correct" not in st.session_state:
            st.session_state.level1_is_correct = False
        if "level1_correct_words" not in st.session_state:
            st.session_state.level1_correct_words = []

        if "family_options" not in st.session_state:
            options, correct_set = generate_family_question()
            st.session_state.family_options = options
            st.session_state.family_correct = correct_set

        options = st.session_state.family_options
        correct_set = st.session_state.family_correct

        st.markdown("### 👨‍👩‍👧‍👦 Level 1 · Family Village")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You arrive at **Family Village**.  
This used to be the peaceful place where you lived with your family.  

But **Lexor** has cast a spell and mixed your family into a pile of random words.  

To open the village gate, you must find **all the real family members** hidden below. 👀
"""
        )

        st.markdown("**Mission:**")   
        st.markdown("- Select **all** the words that are *family members*.")


        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the family members:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit_clicked = st.button("✅ Submit answer")

        if submit_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level1_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level1_correct_words = correct_words
                st.session_state.level1_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level1_is_correct = True
                else:
                    st.session_state.level1_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level1_show_result:
            correct_words = st.session_state.level1_correct_words

            if st.session_state.level1_is_correct:
                st.success(
                    "Great job! 🎉  \n"
                    "You quickly recognize your real family members.  \n"
                    "The village gate makes a loud **click** and opens wide. They are rescued! 🙌  \n"
                    "You step through and walk toward the mysterious **Fruit Manor**..."
                )

                st.markdown("**Family words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("🍎 Go to Level 2: Fruit Manor"):
                    st.session_state.level = 2
                    for key in [
                        "family_options", "family_correct",
                        "level1_show_result", "level1_is_correct",
                        "level1_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

            else:
                st.error(
                    "Oops! 😵  \n"
                    "You chose the wrong people. Lexor takes this chance to attack you,  \n"
                    "and you lose **one life**. ❤️ -1  \n\n"
                    "Take a deep breath and look again — who are your *real* family members?"
                )

                st.markdown("**Correct family members in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another family question"):
                        options, correct_set = generate_family_question()
                        st.session_state.family_options = options
                        st.session_state.family_correct = correct_set
                        st.session_state.level1_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone... The spell is too strong this time.  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 2: FRUIT MANOR -------------
    elif st.session_state.level == 2:

        if "level2_show_result" not in st.session_state:
            st.session_state.level2_show_result = False
        if "level2_is_correct" not in st.session_state:
            st.session_state.level2_is_correct = False
        if "level2_correct_words" not in st.session_state:
            st.session_state.level2_correct_words = []

        if "fruit_options" not in st.session_state:
            options, correct_set = generate_fruit_question()
            st.session_state.fruit_options = options
            st.session_state.fruit_correct = correct_set

        options = st.session_state.fruit_options
        correct_set = st.session_state.fruit_correct

        st.markdown("### 🍎 Level 2 · Fruit Manor")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You leave Family Village and enter the once colorful **Fruit Manor**.  
The trees here used to be full of sweet fruits 🍎🍌🍑,

but now many of them have turned into **cold stone fruits** because of Lexor's spell.  

Only by finding the **real fruits** can you break the spell and bring color back to the orchard.

**Mission:**  
- Select **all** the words that are *fruits*.  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the fruits:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit2_clicked = st.button("✅ Submit answer (Fruit Manor)")

        if submit2_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level2_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level2_correct_words = correct_words
                st.session_state.level2_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level2_is_correct = True
                else:
                    st.session_state.level2_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level2_show_result:
            correct_words = st.session_state.level2_correct_words

            if st.session_state.level2_is_correct:
                st.success(
                    "Amazing!🥳 \n"
                    "You pick out all the real fruits🍉🍌🍎.  \n"
                    "The stone spell shatters, and the whole orchard comes back to life.  \n"
                    "You know that Lexor can't be far away now..."
                )

                st.markdown("**Fruit words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("🐶 Go to Level 3: Zoo Spy"):
                    st.session_state.level = 3
                    for key in [
                        "fruit_options", "fruit_correct",
                        "level2_show_result", "level2_is_correct",
                        "level2_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another Fruit Manor question"):
                    options, correct_set = generate_fruit_question()
                    st.session_state.fruit_options = options
                    st.session_state.fruit_correct = correct_set
                    st.session_state.level2_show_result = False
                    do_rerun()

            else:
                st.error(
                    "Oh no!😥  \n"
                    "You also selected words that are **not** fruits.  \n"
                    "The magic backfires, the ground shakes, and you lose **one life**. ❤️ -1  \n\n"
                    "Think again: which words are fruits you can actually *eat*?"
                )

                st.markdown("**Correct fruits in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another Fruit Manor question"):
                        options, correct_set = generate_fruit_question()
                        st.session_state.fruit_options = options
                        st.session_state.fruit_correct = correct_set
                        st.session_state.level2_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone in Fruit Manor...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 3: ZOO SPY -------------
    elif st.session_state.level == 3:

        if "level3_show_result" not in st.session_state:
            st.session_state.level3_show_result = False
        if "level3_is_correct" not in st.session_state:
            st.session_state.level3_is_correct = False
        if "level3_correct_impostors" not in st.session_state:
            st.session_state.level3_correct_impostors = []

        if "zoo_options" not in st.session_state:
            options, impostor_set = generate_animal_spy_question()
            st.session_state.zoo_options = options
            st.session_state.zoo_impostors = impostor_set

        options = st.session_state.zoo_options
        impostor_set = st.session_state.zoo_impostors

        st.markdown("### 🐶 Level 3 · Zoo Spy")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You continue your journey and arrive at a strange **zoo** covered in fog.  
You can barely see the shapes of different animals behind the mist... 🐘🦒🐼  

But something is wrong — among these words, **two of them are NOT animals at all**.  
They are **impostors**, hiding in the crowd and scaring everyone. ❗

If you don't find them, the animals will keep living in fear and confusion.

**Mission:**  
- In the list below, **two words are NOT animals**.  
- **Select the two impostors.**  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 Choose the two words that are **NOT** animals:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit3_clicked = st.button("✅ Submit answer (Zoo Spy)")

        if submit3_clicked:
            if len(selected_indices) != 2:
                st.warning("Please select **exactly two** words — there are only two impostors.")
                st.session_state.level3_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_impostors = [w for w in options if w["hanzi"] in impostor_set]

                st.session_state.level3_correct_impostors = correct_impostors
                st.session_state.level3_show_result = True

                if selected_hanzi == impostor_set:
                    st.session_state.level3_is_correct = True
                else:
                    st.session_state.level3_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level3_show_result:
            correct_impostors = st.session_state.level3_correct_impostors

            if st.session_state.level3_is_correct:
                st.success(
                    "Nice work, detective! 🕵️‍♀️  \n"
                    "You spot both impostors hiding among the animals.  \n"
                    "The real animals cheer for you loudly, and the fog begins to fade. 👏  \n"
                    "Now you feel even more certain that you are getting closer to Lexor's lair..."
                )

                st.markdown("**The two impostors (NOT animals) in this question:**")
                for w in correct_impostors:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("🔥 Go to Level 4: Verb Volcano"):
                    st.session_state.level = 4
                    for key in [
                        "zoo_options", "zoo_impostors",
                        "level3_show_result", "level3_is_correct",
                        "level3_correct_impostors",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another Zoo Spy question"):
                    options, impostor_set = generate_animal_spy_question()
                    st.session_state.zoo_options = options
                    st.session_state.zoo_impostors = impostor_set
                    st.session_state.level3_show_result = False
                    do_rerun()

            else:
                st.error(
                    "Mission failed, detective.🤦🏻‍♀️ \n\n"
                    "You caught the wrong targets, the two real impostors slipped away, \n"
                    "and you lose **one life**. ❤️ -1  \n\n"
                    "Review the clues—Which words couldn’t possibly be animals? \n\n" 
                )

                st.markdown("**Correct impostors (the two words that are NOT animals):**")
                for w in correct_impostors:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another Zoo Spy question"):
                        options, impostor_set = generate_animal_spy_question()
                        st.session_state.zoo_options = options
                        st.session_state.zoo_impostors = impostor_set
                        st.session_state.level3_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone in the zoo...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 4: VERB VOLCANO -------------
    elif st.session_state.level == 4:

        if "level4_show_result" not in st.session_state:
            st.session_state.level4_show_result = False
        if "level4_is_correct" not in st.session_state:
            st.session_state.level4_is_correct = False
        if "level4_correct_words" not in st.session_state:
            st.session_state.level4_correct_words = []

        if "verb_options" not in st.session_state:
            options, correct_set = generate_verb_question()
            st.session_state.verb_options = options
            st.session_state.verb_correct = correct_set

        options = st.session_state.verb_options
        correct_set = st.session_state.verb_correct

        st.markdown("### 🔥 Level 4 · Verb Volcano")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You leave the foggy zoo behind and stand before a gigantic **Volcano of Words**. 🌋  

From the crater, Chinese characters and pinyin shoot out like streams of fire.  
This place is guarded by the power of **actions** — **verbs**.

Only by finding **all the action verbs** can you calm the volcano  
and open a rocky path that leads deeper into the Word Island.

**Mission:**  
- Select **all** the words that are **action verbs**.  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the action verbs:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit4_clicked = st.button("✅ Submit answer (Verb Volcano)")

        if submit4_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level4_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level4_correct_words = correct_words
                st.session_state.level4_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level4_is_correct = True
                else:
                    st.session_state.level4_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level4_show_result:
            correct_words = st.session_state.level4_correct_words

            if st.session_state.level4_is_correct:
                st.success(
                    "Awesome! 💥  \n"
                    "You pick out all the action verbs.  \n"
                    "The volcano calms down, and a rocky path appears at your feet,  \n"
                    "leading you toward a huge **City Maze**."
                )

                st.markdown("**Action verbs in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("🗺 Go to Level 5: City Maze"):
                    st.session_state.level = 5
                    for key in [
                        "verb_options", "verb_correct",
                        "level4_show_result", "level4_is_correct",
                        "level4_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another Verb Volcano question"):
                    options, correct_set = generate_verb_question()
                    st.session_state.verb_options = options
                    st.session_state.verb_correct = correct_set
                    st.session_state.level4_show_result = False
                    do_rerun()

            else:
                st.error(
                    "Uh-oh!🤯 \n"
                    "You chose some words that are not actions. The volcano erupts even higher 🌋,  \n"
                    "and a few sparks fly past you — you lose **one life**. ❤️ -1  \n\n"
                    "Think again: which words describe something you can actually **do**?"
                )

                st.markdown("**Correct action verbs in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another Verb Volcano question"):
                        options, correct_set = generate_verb_question()
                        st.session_state.verb_options = options
                        st.session_state.verb_correct = correct_set
                        st.session_state.level4_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone at the Verb Volcano...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 5: CITY MAZE (PLACE) -------------
    elif st.session_state.level == 5:

        if "level5_show_result" not in st.session_state:
            st.session_state.level5_show_result = False
        if "level5_is_correct" not in st.session_state:
            st.session_state.level5_is_correct = False
        if "level5_correct_words" not in st.session_state:
            st.session_state.level5_correct_words = []

        if "place_options" not in st.session_state:
            options, correct_set = generate_place_question()
            st.session_state.place_options = options
            st.session_state.place_correct = correct_set

        options = st.session_state.place_options
        correct_set = st.session_state.place_correct

        st.markdown("### 🗺 Level 5 · City Maze")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
At the end of the rocky path lies a giant **City Maze**. 🏙️ 
Lexor has scrambled all the **places** in this city —  

schools, hospitals, restaurants, homes... everything is lost and twisted.  

To walk through the maze, you must recognize which of the words below  
are **real places** that you can actually go to.

**Mission:**  
- Select **all** the words that are **places**.  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the places:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit5_clicked = st.button("✅ Submit answer (City Maze)")

        if submit5_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level5_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level5_correct_words = correct_words
                st.session_state.level5_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level5_is_correct = True
                else:
                    st.session_state.level5_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level5_show_result:
            correct_words = st.session_state.level5_correct_words

            if st.session_state.level5_is_correct:
                st.success(
                    "Hooray!The map lights up! ✨🌃 \n\n"
                    "Each time you pick a real place, that part of the city becomes clear.  \n"
                    "Finally, the whole city map glows softly, showing a shining **Time Tunnel** ahead."
                )

                st.markdown("**Place words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("⏳ Go to Level 6: Time Tunnel"):
                    st.session_state.level = 6
                    for key in [
                        "place_options", "place_correct",
                        "level5_show_result", "level5_is_correct",
                        "level5_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another City Maze question"):
                    options, correct_set = generate_place_question()
                    st.session_state.place_options = options
                    st.session_state.place_correct = correct_set
                    st.session_state.level5_show_result = False
                    do_rerun()

            else:
                st.error(
                    "The city goes dark again...🫨 \n"
                    "You selected some words that are **not** places.  \n"
                    "Street signs spin around, streetlights go out, and you lose **one life**. ❤️ -1  \n\n"
                    "Look again: which words are places you can actually **go to**?"
                )

                st.markdown("**Correct places in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another City Maze question"):
                        options, correct_set = generate_place_question()
                        st.session_state.place_options = options
                        st.session_state.place_correct = correct_set
                        st.session_state.level5_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone in the City Maze...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()
    # ------------- LEVEL 6: TIME TUNNEL -------------
    elif st.session_state.level == 6:

        if "level6_show_result" not in st.session_state:
            st.session_state.level6_show_result = False
        if "level6_is_correct" not in st.session_state:
            st.session_state.level6_is_correct = False
        if "level6_correct_words" not in st.session_state:
            st.session_state.level6_correct_words = []

        if "time_options" not in st.session_state:
            options, correct_set = generate_time_question()
            st.session_state.time_options = options
            st.session_state.time_correct = correct_set

        options = st.session_state.time_options
        correct_set = st.session_state.time_correct

        st.markdown("### ⏳ Level 6 · Time Tunnel")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
After crossing the city, you stand before a glowing **Time Tunnel**🕐.  
All kinds of **time words** float in the air —  

Lexor is trying to use **chaotic time** to stop you from going forward.

Only by recognizing the **real time words**  
can you pass through the tunnel and reach the heart of the Word Island✨.

**Mission:**  
- Select **all** the words that are **time words**.  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the time words:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit6_clicked = st.button("✅ Submit answer (Time Tunnel)")

        if submit6_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level6_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level6_correct_words = correct_words
                st.session_state.level6_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level6_is_correct = True
                else:
                    st.session_state.level6_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level6_show_result:
            correct_words = st.session_state.level6_correct_words

            if st.session_state.level6_is_correct:
                st.success(
                    "The Time Tunnel turns into a stable road of light,🪄  \n"
                    "carrying you straight toward the **Career Town** —  \n"
                    "the place where people live and work.👩🏻‍🚀🧑🏻‍💻👩🏻‍🎓"
                )

                st.markdown("**Time words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("🧑‍⚕️ Go to Level 7: Career Town"):
                    st.session_state.level = 7
                    for key in [
                        "time_options", "time_correct",
                        "level6_show_result", "level6_is_correct",
                        "level6_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another Time Tunnel question"):
                    options, correct_set = generate_time_question()
                    st.session_state.time_options = options
                    st.session_state.time_correct = correct_set
                    st.session_state.level6_show_result = False
                    do_rerun()

            else:
                st.error(
                    "Time is messed up!🫨  \n"
                    "You chose some words that are not time expressions.  \n"
                    "The timeline twists into a knot, a short storm of time swallows you,  \n"
                    "and you lose **one life**. ❤️ -1  \n\n"
                    "Think again: which words are like **today, tomorrow, now**?"
                )

                st.markdown("**Correct time words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another Time Tunnel question"):
                        options, correct_set = generate_time_question()
                        st.session_state.time_options = options
                        st.session_state.time_correct = correct_set
                        st.session_state.level6_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone in the Time Tunnel...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 7: CAREER TOWN -------------
    elif st.session_state.level == 7:

        if "level7_show_result" not in st.session_state:
            st.session_state.level7_show_result = False
        if "level7_is_correct" not in st.session_state:
            st.session_state.level7_is_correct = False
        if "level7_correct_words" not in st.session_state:
            st.session_state.level7_correct_words = []

        if "job_options" not in st.session_state:
            options, correct_set = generate_job_question()
            st.session_state.job_options = options
            st.session_state.job_correct = correct_set

        options = st.session_state.job_options
        correct_set = st.session_state.job_correct

        st.markdown("### 🧑‍⚕️ Level 7 · Career Town")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You pass through the Time Tunnel and arrive at **Career Town**.  
This town is where doctors, teachers, students and many others work and live.  

But now their identities are all mixed up.😵‍💫  
Only by finding the real **jobs / professions**  
can the town return to normal and its people help you fight Lexor.

**Mission:**  
- Select **all** the words that are **jobs / professions**.  
"""
        )

        indices = list(range(len(options)))
        selected_indices = st.multiselect(
            "👇 From the 4 words below, choose **all** the jobs / professions:",
            options=indices,
            format_func=lambda i: f"{options[i]['hanzi']}  {options[i]['pinyin']}",
        )

        submit7_clicked = st.button("✅ Submit answer (Career Town)")

        if submit7_clicked:
            if not selected_indices:
                st.warning("Please select at least one word before submitting.")
                st.session_state.level7_show_result = False
            else:
                selected_hanzi = {options[i]["hanzi"] for i in selected_indices}
                correct_words = [w for w in options if w["hanzi"] in correct_set]

                st.session_state.level7_correct_words = correct_words
                st.session_state.level7_show_result = True

                if selected_hanzi == correct_set:
                    st.session_state.level7_is_correct = True
                else:
                    st.session_state.level7_is_correct = False
                    st.session_state.lives = max(0, st.session_state.lives - 1)

        if st.session_state.level7_show_result:
            correct_words = st.session_state.level7_correct_words

            if st.session_state.level7_is_correct:
                st.success(
                    "Fantastic!😊  \n"
                    "You find all the real professions.  \n"
                    "The residents of Career Town decide to join you and chase Lexor together.  \n"
                    "And the **Final Trial** is waiting for you..."
                )

                st.markdown("**Job words in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                if st.button("💥 Go to Level 8: Final Trial"):
                    st.session_state.level = 8
                    for key in [
                        "job_options", "job_correct",
                        "level7_show_result", "level7_is_correct",
                        "level7_correct_words",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]
                    do_rerun()

                if st.button("🔁 Try another Career Town question"):
                    options, correct_set = generate_job_question()
                    st.session_state.job_options = options
                    st.session_state.job_correct = correct_set
                    st.session_state.level7_show_result = False
                    do_rerun()

            else:
                st.error(
                    "Yikes!😧 \n"
                    "Lexor secretly messed with you, and you chose some words that are not jobs.  \n"
                    "You lose **one life**. ❤️ -1  \n\n"
                    "Think again: who is really **working**? Who is just a relationship or a title?"
                )

                st.markdown("**Correct jobs / professions in this question:**")
                for w in correct_words:
                    st.markdown(f"- {w['hanzi']}  {w['pinyin']}  ({w['english']})")

                st.markdown(f"Remaining lives: **{st.session_state.lives} ❤️**")

                if st.session_state.lives > 0:
                    if st.button("🔁 Try another Career Town question"):
                        options, correct_set = generate_job_question()
                        st.session_state.job_options = options
                        st.session_state.job_correct = correct_set
                        st.session_state.level7_show_result = False
                        do_rerun()
                else:
                    st.warning(
                        "Your lives are all gone in Career Town...  \n"
                        "You can restart your adventure from the beginning."
                    )
                    if st.button("🔄 Restart from intro"):
                        st.session_state.page = "intro"
                        reset_game_state()
                        do_rerun()

    # ------------- LEVEL 8: FINAL TRIAL -------------
    elif st.session_state.level == 8:

        # Initialize flags
        if "final_show_result" not in st.session_state:
            st.session_state.final_show_result = False
        if "final_is_correct_enough" not in st.session_state:
            st.session_state.final_is_correct_enough = False

        # Generate 7 words (1 per category) with category field
        if "final_words" not in st.session_state:
            st.session_state.final_words = generate_final_trial_words()

        words = st.session_state.final_words

        CATEGORY_OPTIONS = ["Family", "Fruit", "Animal", "Verb", "Place", "Time", "Job"]
        CAT_DISPLAY = {
            "family": "Family",
            "fruit": "Fruit",
            "animal": "Animal",
            "verb": "Verb",
            "place": "Place",
            "time": "Time",
            "job": "Job",
        }

        st.markdown("### 💥 Level 8 · Final Trial: Vocabulary Chaos")
        st.markdown(f"**Explorer:** {name}  |  ❤️ Lives: **{st.session_state.lives}**")

        st.markdown(
            """
You finally reach the very center of the **Word Island**.  

Lexor stands on a throne made of Chinese characters.  
All the words you’ve seen before — **family, fruits, animals, verbs, places, time words, jobs** —  
are now floating in the air, completely mixed together.  

To defeat Lexor once and for all,  
you must **sort these words back into their correct categories**.🤔

**Mission:**  
Classify each word into the correct category:  
**Family / Fruit / Animal / Verb / Place / Time / Job.**
"""
        )

        # Keep student choices across reruns
        if "final_answers" not in st.session_state:
            st.session_state.final_answers = {
                i: "(Select category)" for i in range(len(words))
            }

        answers = {}
        st.markdown("#### Choose a category for each word:")

        options_for_select = ["(Select category)"] + CATEGORY_OPTIONS

        for i, w in enumerate(words):
            label = f"{w['hanzi']}  {w['pinyin']}"

            prev = st.session_state.final_answers.get(i, "(Select category)")
            try:
                default_index = options_for_select.index(prev)
            except ValueError:
                default_index = 0

            choice = st.selectbox(
                label,
                options_for_select,
                index=default_index,
                key=f"final_word_{i}",
            )
            answers[i] = choice

        submit_final = st.button("✅ Submit final trial")

        if submit_final:
            st.session_state.final_answers = answers

            correct_count = 0
            total = len(words)
            detailed_result = []

            for i, w in enumerate(words):
                true_cat_key = w["category"]               # "family" / "fruit" ...
                true_cat_display = CAT_DISPLAY[true_cat_key]

                student_choice = answers[i]
                is_correct = (student_choice == true_cat_display)
                if is_correct:
                    correct_count += 1

                detailed_result.append({
                    "word": w,
                    "true_cat_display": true_cat_display,
                    "student_choice": student_choice,
                    "is_correct": is_correct,
                })

            accuracy = correct_count / total if total > 0 else 0.0
            st.session_state.final_detailed_result = detailed_result
            st.session_state.final_accuracy = accuracy
            st.session_state.final_show_result = True
            st.session_state.final_is_correct_enough = (accuracy >= 0.7)


        # --------- Result area ---------
        if st.session_state.final_show_result:
            accuracy = st.session_state.final_accuracy
            detailed_result = st.session_state.final_detailed_result
            correct_num = sum(d["is_correct"] for d in detailed_result)

            st.markdown("---")
            st.markdown(
                f"**Your score:** {int(accuracy * 100)}% "
                f"({correct_num}/{len(detailed_result)})"
            )

            if st.session_state.final_is_correct_enough:
                # ✅ Victory ending
                st.success(
                    "Congratulations to your victory! 🎉  \n"
                    "Family members have returned to **Family Village**,  \n"
                    "fruits hang back on the trees in **Fruit Manor**,  \n"
                    "animals run freely in the zoo, **Career Town** is busy again,  \n"
                    "and time & places are all back on track.  \n\n"
                    "Lexor stares in shock:  \n"
                    "\"Impossible!😡 How can you remember all these words so clearly?!\"  \n"
                    "His shadow slowly fades away in the light.  \n\n"
                    "The Word Island is peaceful again…  \n"
                    "but your Chinese learning adventure has only just begun. 🌟"
                )
            else:
                st.error(
                    "You fought bravely all the way here, but the spell is not fully broken yet…  \n"
                    "Some words were still in the wrong categories.  \n\n"
                    "Press **Try the final trial again** to take this challenge one more time. ⛽💪 \n"
                    "Maybe next time, you'll remember even more words and go even further!"
                )

            st.markdown("### ✅ Correct categories")
            for item in detailed_result:
                w = item["word"]
                true_cat = item["true_cat_display"]
                st.markdown(
                    f"- {w['hanzi']} {w['pinyin']} ({w['english']}) → **{true_cat}**"
                )

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔁 Try the final trial again"):
            
                    st.session_state.final_words = generate_final_trial_words()
                    st.session_state.final_show_result = False
                    st.session_state.final_is_correct_enough = False
                    st.session_state.final_answers = {
                        i: "(Select category)"
                        for i in range(len(st.session_state.final_words))
                    }
                    do_rerun()

            with col2:
                if st.button("🌈 Restart the whole adventure"):
                    reset_game_state()            # lives=3, level=1
                    st.session_state.page = "game"
                    do_rerun()

# ------------------------
# Footer: Copyright notice
# ------------------------
st.markdown(
    """
    <div style='text-align:center; font-size:0.8rem; color:#666; margin-top:2rem; padding-top:1rem;'>
        © 2025 Yutong Cui (Carina). Chinese Word Island Adventure.<br>
        For educational use only. Please do not copy, redistribute, or modify without permission.
    </div>
    """,
    unsafe_allow_html=True,
)

