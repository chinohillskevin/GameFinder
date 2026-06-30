import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
 api_key = st.secrets["key"]
)

st.title("GameFinder", False)
st.write("Finds the best games for you.")

with st.form("GameFinder"):

    genre = st.multiselect(
        "What is your favorite video game genre?", 
        ["Shooter", "RPG", "Adventure", "Sandbox", "Racing", "Gambling", "Card/Board Games", "Horror"],
        accept_new_options= True
        )

    system = st.multiselect(
        "What devices/system(s) do you play on?",
        ["PC", "PS5", "PS4", "Nintendo Switch", "Phone", "Ipad/Tablet", "Xbox"],
        accept_new_options= True
    )

    budget = st.number_input(
        "What is your budget?(in US dollars)",
        min_value = 0, max_value = 100)

    other_games = st.text_area("What games do you already play?")

    time = st.text_input("What is the preferable amount of time you would play a game in one sitting?")

    indie_game = st.segmented_control("Would you indie games?", ["Only Indie", "Both Indie and Non-Indie", "No Indie"], default = "Both Indie and Non-Indie")

    requirements = st.text_area("Are there any other requirements you would like to add?")

    submitted = st.form_submit_button("SUBMIT")




if submitted:
    user_prompt = f"""

    Suggest a list of video games the user would enjoy to playif their favorite genre is {genre}, they play on {system}, their budget is {budget}, they already play {other_games}, they would preferably spend {time} playing a game in one sitting, and suggest {indie_game} games.
    The requirements are: {requirements}
    

    """
    system_prompt = """
    Return in JSON format.
    This is the format of the JSON object you should return:

    {"recommendations":
        [
            {
                "title": "title",
                "description": "description",
                "price": "price",
                "indie": true,
                "device": ["device"],
                "genre": ["genre"],
                "link": "link"
                "reason": "reason"
            }
        ]
    }

    There should be 3 to 10 recommendations in the JSON array.
    The link should be a link to the game's official website.
    The reason should be a short explanation of why the game was recommended to the user based on their preferences.

    """
    response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )

    things = (json.loads(response.choices[0].message.content))["recommendations"]
    st.header("These are your game reccomendations:", False)
    for thing in things:
        with st.container(border = True):
            st.subheader(thing["title"], False)
            st.write(thing["description"])

            st.badge(f"Price: {thing['price']}", color = "green")

            if thing['indie']:
                st.badge(f"1️⃣ Indie", color = "red")

            devices = ""
            for device in thing['device']:
                devices += f":gray-badge[{device}] "
            st.markdown(devices)

            genres = ""
            for genre in thing['genre']:
                genres += f":yellow-badge[{genre}] "
            st.markdown(genres)

            reason = st.caption(thing["reason"])

            link = st.link_button("Learn More", thing["link"])
