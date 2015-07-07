# Celebrity Date Of Birth Finder
This script is run from the terminal and is passed a celebrity name in quotes.
<br><code>$ python celebrity_dob_finder.py -n "Halle Berry'</code>
This will run the file and load the database <code>birthdate_database.p</code> which already has multiple celebrities' data stored.
<br>

If the celebrity you search for already exists in the database, it will return their name and date of birth.<br>
If not, the script will query the Wikipedia API for this information.
<br><code>$ python celebrity_dob_finder.py -n "Halle Berry'</code>
<br><code>Halle Berry was born on 1966/8/14</code>
<br><code>Other notable figures with the same birthday are:</code>
<br><code>Gillian Taylforth - 1955/8/14</code>
<br><code>Spencer Pratt - 1983/8/14</code>
<br><code>Mila Kunis - 1983/8/14</code></code>

Halle Berry will then be added to the database pickle file after the query.
