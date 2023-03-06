"""Generate a config file per participant.

Participants come from:
  - participants_default
  - CSV from Google Forms named form.csv in the same dir as the script
"""

import configparser
from pathlib import Path
import random

import pandas as pd


participants_default = [
    "ivalaginja",
]

# Add user000 till nusers as backup
# in case somebody not in the form
nusers = 5
for i in range(nusers):
    username = f"user{i:03d}"
    participants_default.append(username)

animals_list = [
    "cat",
    "dog",
    "goat",
    "leopard",
    "lion",
    "bear",
    "camel",
    "cow",
    "coyote",
    "deer",
    "dolphin",
    "hyena",
    "horse",
    "bull",
    "cock",
    "raven",
]

# Create directory for user files
base_dir = Path(__file__).parent
pkg_dir = base_dir / "mypackage"
pkg_dir.mkdir(parents=True, exist_ok=True)

# Read the participants' Github handles from the form
form = base_dir / "form.csv"
responses = pd.read_csv(form)
participants = responses["GitHub handle (this is NOT a captcha - put in *your* handle)"].to_list()
participants.extend(participants_default)


def generate_file(participant):
    fname = participant + ".ini"
    fpath = pkg_dir / fname

    config = configparser.ConfigParser()
    config.read(fpath)
    section = "pet"
    if not config.has_section(section):
        config.add_section(section)
        k = 3  # Write all
    else:
        k = 2  # Write 2/3

    options = ["animal", "age", "weight"]
    choices = random.sample(options, k=k)
    if "animal" in choices:
        config.set(section, "animal", random.choice(animals_list))
    if "age" in choices:
        config.set(section, "age", str(random.randint(1, 100)))
    if "weight" in choices:
        config.set(section, "weight", "{:.3f}".format(abs(random.gauss(10, 10))))

    with open(fpath, "w") as f:
        config.write(f)


for participant in participants:
    print(participant)
    generate_file(participant)
