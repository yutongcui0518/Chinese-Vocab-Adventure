Chinese Word Island Adventure 🎮🌴
An 8-level Streamlit web game designed for beginning learners of Chinese to consolidate vocabulary across seven core categories: family, fruit, animal, verb, place, time, job.
Players move through different “regions” of the island, answering vocabulary questions and finally sorting all words by category to defeat the monster Lexor.
https://word-island-adventure.streamlit.app/
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Project Overview
Main ideas:
Built with Streamlit as a single-page app.
Uses a CSV-based word bank (word_bank.csv) as the data source.
Uses st.session_state to manage global game state (page, level, lives, etc.).

Implements 8 levels with different task types:
Levels 1–7: category-based selection tasks.
Level 8: final classification task (assign each word to the correct category).

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. Files & Dependencies
2.1 Required files
wordisland.py (the coding base)

word_bank.csv:
Columns: category, hanzi, pinyin, english
Used by: load_word_bank_from_csv(), all generate_* functions.

bgm_8bit_menu.mp3 (optional): background music file.
Used by: load_bgm().


2.2 External libraries
streamlit – UI framework and session state.
csv – loading the word bank.
random – sampling options for questions.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3. App Setup & Rerun Logic
3.1 Streamlit page configuration
Function / calls:
st.set_page_config(...)
Sets page title, favicon, and layout:
page_title="Chinese Word Island Adventure"
page_icon="🎮"
layout="centered"

Purpose:
Provides consistent look and feel in the browser (tab title, icon, layout).


3.2 Cross-version rerun helper
def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()
        
Purpose:
Wraps Streamlit’s rerun API for both newer (st.rerun) and older (st.experimental_rerun) versions.
Used whenever the game:
Moves between levels; Regenerates questions; Resets the whole adventure.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
4. Word Bank: Data Loading & Structure
4.1 CSV loader

Function:
def load_word_bank_from_csv(path: str):
    ...

Behavior:
Reads word_bank.csv with csv.DictReader.
Expects columns: category, hanzi, pinyin, english.
Strips whitespace from each field.

Builds a dict:

{
    "family": [ {"hanzi": ..., "pinyin": ..., "english": ...}, ... ],
    "fruit":  [ ... ],
    ...
}

Global constant:
WORD_BANK = load_word_bank_from_csv("word_bank.csv")

Purpose:
Provides a global word bank by category that all question-generation functions use.
Makes the game data-driven: editing the CSV updates the game content without code changes.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
5. Question Generation (Levels 1–7)

Each level has a dedicated helper that returns:
options: a list of word dicts ({"hanzi", "pinyin", "english"}).
correct_set: a set of correct hanzi values (or impostors in Level 3).
All of them rely on WORD_BANK.

5.1 Family (Level 1)
Function:
def generate_family_question():
    ...

Logic:
Samples 2 family words → correct_words.
Samples 2 words from all non-family categories → distractors.

Shuffles all 4 and returns:
options = correct_words + distractors (shuffled).
correct_set = {hanzi of correct_words}.


5.2 Fruit (Level 2)

Function:
def generate_fruit_question():
    ...

Logic:
Same pattern as Level 1:
2 fruit words + 2 non-fruit distractors.
Returns options and correct_set.


5.3 Animal / Impostor Task (Level 3)

Function:
def generate_animal_spy_question():
    ...

Logic:
Picks 4 animal words.
Picks 2 words from non-animal categories → impostors.
Shuffles and returns:
options = animals + impostors.
impostor_set = {hanzi of impostor words}.

Purpose:
Inverts the logic: player must find the two words that are NOT animals.


5.4 Verb (Level 4)
Function:
def generate_verb_question():
    ...

Logic:
2 verb words + 2 non-verb distractors.
Returns options, correct_set.


5.5 Place (Level 5)
Function:
def generate_place_question():
    ...

Logic:
2 place words + 2 non-place distractors.
Returns options, correct_set.


5.6 Time (Level 6)
Function:
def generate_time_question():
    ...

Logic:
2 time words + 2 non-time distractors.
Returns options, correct_set.


5.7 Job (Level 7)
Function:
def generate_job_question():
    ...

Logic:
2 job words + 2 non-job distractors.
Returns options, correct_set.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
6. Final Trial Word Generation (Level 8)
Function:
def generate_final_trial_words():
    ...

Logic:

Categories: ["family", "fruit", "animal", "verb", "place", "time", "job"].

For each category, randomly selects one word and adds a category field:

{
  "hanzi": ...,
  "pinyin": ...,
  "english": ...,
  "category": "family" | "fruit" | ...
}

Shuffles the final list and returns 7 words.

Purpose:
Provides the input for the Level 8 classification task, where each word must be mapped back to its category.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

7. Game State & Navigation
7.1 Session state initialization
Session keys:
st.session_state.page – "intro" or "game".

st.session_state.player_name – name entered on intro page.

st.session_state.lives – lives remaining (start at 3).

st.session_state.level – current level (1–8).

Code:
if "page" not in st.session_state:
    st.session_state.page = "intro"

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "level" not in st.session_state:
    st.session_state.level = 1



7.2 Resetting game state
Function:
def reset_game_state():
    ...

What it does:
Resets:
lives = 3
level = 1
Deletes all level-specific state keys, including:

Question options & correct sets per level (family_options, fruit_correct, etc.).

Result flags (levelX_show_result, levelX_is_correct, levelX_correct_words, etc.).

Final trial state (final_words, final_answers, final_detailed_result, final_accuracy, etc.).

Purpose:
Ensures a truly clean restart, with no leftover data from previous runs.



7.3 Page transition from intro → game
Function:
def go_to_game():
    ...

Logic:
Checks st.session_state.player_name: If empty: shows st.warning(...). If non-empty: Calls reset_game_state().
Sets st.session_state.page = "game".

Purpose:
Prevents starting the adventure without a name.
Guarantees game state is clean whenever a new run starts.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
8. UI, Styling & Media
8.1 Background image and card layout
Constant:
BACKGROUND_URL = "https://f4.bcbits.com/img/a2060336255_16.jpg"

CSS injection:
page_bg = f"""
<style>
.stApp {{
    background-image: url('{BACKGROUND_URL}');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
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

Purpose:
Sets a full-page island background.
Wraps the main content in a translucent card for readability.



8.2 Background music
Function:
def load_bgm():
    try:
        with open("bgm_8bit_menu.mp3", "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

Usage:

bgm_bytes = load_bgm()
if bgm_bytes:
    st.audio(bgm_bytes, format="audio/mp3", start_time=0)

Purpose:
Loads a local MP3 file and plays it at the top of the page.
Wrapped in a try/except so the app still runs if the file is missing.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

9. Page & Level Logic
The main control flow:
if st.session_state.page == "intro":
    ...  # Intro screen
elif st.session_state.page == "game":
    name = ...
    if level == 1: ...
    elif level == 2: ...
    ...
    elif level == 8: ...

9.1 Intro Page
Title & narrative story (st.title, st.markdown).

Name input:
st.session_state.player_name = st.text_input(...)

Button:
if st.button("Start Adventure"):
    go_to_game()

Purpose:
Introduce storyline.
Collect player name and transition into the game.



9.2 Levels 1–7 (Pattern)
Each level block:
Initializes level-specific state keys if missing:

if "levelX_show_result" not in st.session_state:
    st.session_state.levelX_show_result = False
...
if "<category>_options" not in st.session_state:
    options, correct_set = generate_<category>_question()
    st.session_state.<category>_options = options
    st.session_state.<category>_correct = correct_set


Displays narrative and mission description with st.markdown.
Renders a st.multiselect for answer choices:
Uses indices (0..3 or 0..5) and format_func to show hanzi + pinyin.
On submit (st.button(...)):
Validates selection (e.g., “select exactly two” in Zoo Spy).

Computes:
Selected hanzi set.
correct_words list for feedback.

Sets:
levelX_show_result
levelX_is_correct
Updates lives if wrong.

Result section:
If correct:
st.success with story-based feedback.
Shows all correct words.

Buttons:
Go to next level → update st.session_state.level and clear this level’s state → do_rerun().
(Sometimes) Try another question of the same level → regenerate question and do_rerun().

If incorrect:
st.error with story-based negative feedback and ❤️ -1.
Shows correct answers.
If lives > 0: allow retry with a new question.
If lives == 0: show restart option (back to intro) and call reset_game_state().



9.3 Level 8: Final Trial
State:
st.session_state.final_words – 7 words (1 per category).
st.session_state.final_answers – maps each index to a chosen category string.
st.session_state.final_detailed_result – list of per-word result dicts.
st.session_state.final_accuracy – numeric accuracy.
st.session_state.final_show_result, st.session_state.final_is_correct_enough – control showing feedback and passing threshold.

UI flow:
Generate final_words with generate_final_trial_words() if not yet created.
For each word, render a st.selectbox:
Options: ["(Select category)", "Family", "Fruit", ...].
Key: f"final_word_{i}".
Default is pulled from st.session_state.final_answers.

On submit:
submit_final = st.button("✅ Submit final trial")
Saves current answers into final_answers.
Compares each student_choice with the true category (w["category"] mapped via CAT_DISPLAY).
Computes correct_count, accuracy.

Sets final_show_result = True and:
final_is_correct_enough = (accuracy >= 0.7).

Result:
Shows score: "{int(accuracy*100)}% ({correct_num}/7)".
If accuracy >= 0.7:
st.success with victory ending narrative.

Else:
st.error with encouragement to retry.
Shows a summary list of all words with their correct categories.

Buttons:
"🔁 Try the final trial again":
Regenerates final_words.
Resets final-trial-related session state.
Calls do_rerun().
"🌈 Restart the whole adventure":
Calls reset_game_state().
Sets page = "game" (starting from Level 1).
Calls do_rerun().

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
10. Footer

Code:
st.markdown(
    """
    <div style='text-align:center; font-size:0.8rem; color:#666; margin-top:2rem; padding-top:1rem;'>
        © 2025 Yutong Cui (Carina). Chinese Word Island Adventure.<br>
        For educational use only. Please do not copy, redistribute, or modify without permission.
    </div>
    """,
    unsafe_allow_html=True,
)

Purpose:
Adds a simple copyright and usage note at the bottom of the app.
