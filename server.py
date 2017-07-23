from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Getting our list of MOST LOVED MELONS
MOST_LOVED_MELONS = {
    'cren': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimRegular/crenshaw.jpg',
        'name': 'Crenshaw',
        'num_loves': 584,
    },
    'jubi': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg',
        'name': 'Jubilee Watermelon',
        'num_loves': 601,
    },
    'sugb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Sugar-Baby-Watermelon-web.jpg',
        'name': 'Sugar Baby Watermelon',
        'num_loves': 587,
    },
    'texb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Texas-Golden-2-Watermelon-web.jpg',
        'name': 'Texas Golden Watermelon',
        'num_loves': 598,
    },
}

# YOUR ROUTES GO HERE
@app.route("/")
def index():
    """Return homepage."""

    if session.get("user_name"):
        return redirect("/top-melons")
    elif not session.get("user_name"):
        return render_template("homepage.html")


@app.route("/get-name", methods=["GET"])
def get_name():
    """Gets user's name and adds to session."""

    name = request.args.get("my_name")
    session["user_name"] = name
    return redirect("/top-melons")


@app.route("/top-melons")
def show_top_melons():
    """Displays top melons."""

    if session.get("user_name"):
        return render_template("top-melons.html", melon_dict=MOST_LOVED_MELONS)
    elif not session.get("user_name"):
        return redirect("/")


@app.route("/love-melon", methods=["POST"])
def love_a_melon():
    """Increases num_loves count for a melon."""

    fav_melon = request.form.get("favmelon")

    MOST_LOVED_MELONS[fav_melon]["num_loves"] = MOST_LOVED_MELONS[fav_melon].get("num_loves") + 1
    
    return redirect("/top-melons")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
