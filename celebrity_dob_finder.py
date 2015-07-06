from datetime import datetime
from time import time as t
import argparse
import re
import requests
import sys
try:
   import cPickle as pickle
except:
   import pickle

DATABASE = {}

def clean_name(name):
	"""
	Takes in an input string from a user and returns a string formatted to be searched by the API.
	e.g. 'harry hill' becomes 'Harry_Hill'
	Args: param1 (str): name.
	Returns: (str): name_to_search  
	"""
	name_trailing_white_space_removed = name.strip()
	name_spaces_corrected = re.sub('\s+', '_', name_trailing_white_space_removed) # Replace multiple spaces with just one space
	name_to_search = name_spaces_corrected.title() # Capitalizes all First Letters of words
	return name_to_search


def request_json_from_api(clean_name_to_search):
	"""
	Takes in a clean name to search and queries the api returning a string of json data. 
	Args: param1 (str): clean_name_to_search
	Returns: (str): str(json)
	"""
	url_string = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=" + clean_name_to_search + "&rvprop=content&format=json"
	r = requests.get(url_string)
	full_json_result = str(r.json())
	return full_json_result


def get_birthdate_from_json_result(json_result):
	"""
	Takes in a string of json data and uses a regex to search for the date of birth
	Args: param1 (str): json
	Returns: (str): date of birth
	"""
	# Looks for case insensitive 'Birth Date' [with optional ' and age'] with '|' [with optinal 'mf=yes'] with 'YYYY|MM|DD'
	birthPattern = 'Birth date( and age)?\|(\w+=\w+\|)?(\d{1,4}\|\d{1,2}\|\d{1,2})'
	match = re.search(birthPattern, json_result, flags=re.IGNORECASE)
	result = ""
	for group in match.groups():
		if group:
			result = group
	birthdate_before_format = result
	birthdate = birthdate_before_format.replace('|', "/")
	birthdate = birthdate.replace("/0", "/")
	return birthdate

# Currently unused as also have to account for those who have passed away.
'''
def get_time_since_birthdate(birthdate):
	"""
	Used to get amount of time since birth date.
	"""
	celeb_birthdate = t.strptime('1987/09/11', '%Y/%m/%d')
	today_date = t.strptime(t.strftime("%Y/%m/%d"), '%Y/%m/%d')
	old_date = datetime(celeb_birthdate.tm_year, celeb_birthdate.tm_mon, celeb_birthdate.tm_mday)
	new_date = datetime(today_date.tm_year, today_date.tm_mon, today_date.tm_mday)
	datediff = datetime.timedelta(old_date.fromordinal(1970), new_date.fromordinal(1970))
	print datediff
'''

def print_result(name, birthdate):
	"""
	Takes in the name of the celebrity to be searched and their birthdate.
	Prints this info to the screen in a string.
	Args: param1 (str): name, param2 (str): birthdate
	prints: "NAME was born on YYYY/MM/DD"
	"""
	print "{} was born on {}".format(name, birthdate)


def find_related_birthdays(name, birthdate):
	"""
	Finds other celebrities in the database with the same birth month and date.
	"""
	dict_of_related_birthdays = {key:val for key, val in DATABASE.iteritems() if val[4:] == birthdate[4:] and key != name}
	if dict_of_related_birthdays:
		print "Other notable figures with the same birthday are:"
		for key, val in dict_of_related_birthdays.iteritems():
			print "{} - {}".format(key.replace("_", " "), val)


def open_database():
	"""
	Opens database or creates an empty database using pickle.
	"""
	try:
		with open('birthdate_database.p', 'r') as f:
			loaded_database = pickle.load(f)
			global DATABASE 
			DATABASE = loaded_database
	except:
		DATABASE = {}
		with open('birthdate_database.p', 'wb') as f:
			pickle.dump(DATABASE, f)


def populate_database():
	"""
	This function populates the database with
	"""
	open_database()
	DATABASE.update({
	'Gary_Busey':'1944/6/29',
	'George_Clooney':'1961/5/6',
	'Sandra_Bullock':'1964/7/26',
	'Harrison_Ford':'1942/7/13',
	'Julia_Robert':'1967/10/28',
	'Zach_Galifianaki':'1969/10/1',
	'Jerry_Hall':'1956/7/2',
	'Will_Ferrell':'1967/7/16',
	'Kelly_Rowland':'1981/2/11',
	'Frankie_Sandford':'1989/1/14',
	'Charlie_Sheen':'1965/9/3',
	'Bradley_Cooper':'1975/1/5',
	'Harry_Style':'1994/2/1',
	'Lindsay_Lohan':'1986/7/2',
	'Keanu_Reeves':'1964/9/2',
	'Vin_Diesel':'1967/7/18',
	'Jet_Li':'1963/4/26',
	'Dani_Harmer':'1989/2/8',
	'Marilyn_Monroe':'1926/6/1',
	'Rosie_Huntington-Whiteley':'1987/4/18',
	'Dannii_Minogue':'1971/10/20',
	'Kylie_Minogue':'1968/5/28',
	'Bruce_Forsyth':'1928/2/22',
	'Bruce_Willis':'1955/3/19',
	'Vanessa_Hudgens':'1988/12/14',
	'Demi_Moore':'1962/11/11',
	'Lauren_Goodger':'1986/9/19',
	'Solange_Knowles':'1986/6/24',
	'Morgan_Freeman':'1937/6/1',
	'Christopher_Maloney':'1969/3/22',
	'Tom_Hiddleston':'1981/2/9',
	'Brad_Pitt':'1963/12/18',
	'Marlon_Brando':'1924/4/3',
	'Michelle_Keegan':'1987/6/3',
	'Mariah_Carey':'1969/3/27',
	'Sarah_Harding':'1981/11/17',
	'Johnny_Depp':'1963/6/9',
	'Cory_Monteith':'1982/5/11',
	'Darcey_Bussell':'1969/4/27',
	'Jessica_Simpson':'1980/7/10',
	'Adam_Sandler':'1966/9/9',
	'Miley_Cyrus':'1992/11/23',
	'Jason_Statham':'1967/7/26',
	'Harry_Hill':'1964/10/1',
	'Emma_Stone':'1988/11/6',
	'Heidi_Montag':'1986/9/15',
	'Tom_Cruise':'1962/7/3',
	'Daniel_Radcliffe':'1989/7/23',
	'Gillian_Taylforth':'1955/8/14',
	'Natasha_Richardson':'1963/5/11',
	'Rihanna':'1988/2/20',
	'Colin_Baker':'1943/6/8',
	'Owen_Wilson':'1968/11/18',
	'Nicolas_Cage':'1964/1/7',
	'Jason_Biggs':'1978/5/12',
	'Victoria_Pendleton':'1980/9/24',
	'Steve_Jobs':'1955/2/24',
	'Neil_Ruddock':'1968/5/9',
	'Kendall_Jenner':'1995/11/3',
	'Selena_Gomez':'1992/7/22',
	'Reese_Witherspoon':'1976/3/22',
	'Mark_Wahlberg':'1971/6/5',
	'Channing_Tatum':'1980/4/26',
	'Bill_Murray':'1950/9/21',
	'Nicky_Byrne':'1978/10/9',
	'Taylor_Swift':'1989/12/13',
	'Cheryl_Fergison':'1965/8/27',
	'Coleen_Rooney':'1986/4/3',
	'Pixie_Lott':'1991/1/12',
	'Demi_Lovato':'1992/8/20',
	'Tom_Hank':'1956/7/9',
	'Natalie_Portman':'1981/6/9',
	'Katie_Holmes':'1978/12/18',
	'David_Walliams':'1971/8/20',
	'Kristen_Stewart':'1990/4/9',
	'Kate_Winslet':'1975/10/5',
	'Sid_Owens':'1972/1/12',
	'Pierce_Brosnan':'1953/5/16',
	'Justin_Bieber':'1994/3/1',
	'Benedict_Cumberbatch':'1976/7/19',
	'Brendan_Fraser':'1968/12/3',
	'Miranda_Kerr':'1983/4/20',
	'Mollie_King':'1987/6/4',
	'Jennifer_Lawrence':'1990/8/15',
	'Denzel_Washington':'1954/12/28',
	'Russell_Crowe':'1964/4/7',
	'Justin_Timberlake':'1981/1/31',
	'Kate_Beckinsale':'1973/7/26',
	'Amitabh_Bachchan':'1942/10/11',
	'Colin_Salmon':'1962/12/6',
	'Sienna_Miller':'1981/12/28',
	'Lucy_Spraggan':'1991/7/21',
	'Peter_Jackson':'1961/10/31',
	'David_Haye':'1980/10/13',
	'Len_Goodman':'1944/4/25',
	'Steve_Carell':'1962/8/16',
	'Rylan_Clark':'1988/10/25',
	'Bruno_Tonioli':'1955/11/25',
	'Olivia_Palermo':'1986/2/28',
	'Christina_Aguilera':'1980/12/18',
	'Lea_Michele':'1986/8/29',
	'Lady_Gaga':'1986/3/28',
	'Caroline_Flack':'1979/11/9',
	'Daniel_Craig':'1968/3/2',
	'Cheryl_Cole':'1983/6/30',
	'Robert_Downey_Jr.':'1965/4/4',
	'Susanna_Reid':'1970/12/10',
	'Lauren_Bacall':'1924/9/16',
	'Louis_Walsh':'1952/8/5',
	'Lisa_Riley':'1976/7/13',
	'Bruno_Mars':'1985/10/8',
	'Ben_Affleck':'1972/8/15',
	'Ryan_Gosling':'1980/11/12',
	'Jean-Claude_Van_Damme':'1960/10/18',
	'Dwayne_Johnson':'1972/5/2',
	'Arnold_Schwarzenegger':'1947/7/30',
	'Antonio_Bandera':'1960/8/10',
	'Louis_Tomlinson':'1991/12/24',
	'Pasha_Kovalev':'1980/1/19',
	'Danica_Thrall':'1988/3/30',
	'Christian_Bale':'1974/1/30',
	'Ben_Haenow':'1985/1/6',
	'Calvin_Harri':'1984/1/17',
	'Kate_Moss':'1974/1/16',
	'Jessie_J':'1988/3/27',
	'Hugh_Jackman':'1968/10/12',
	'Peaches_Geldof':'1989/3/13',
	'Britney_Spears':'1981/12/2',
	'Eva_Longoria':'1975/3/15',
	'Mel_B':'1975/5/29',
	'Jay_Z':'1969/12/4',
	'Sean_Connery':'1930/8/25',
	'Ashton_Kutcher':'1978/2/7',
	'Sam_Robertson':'1985/10/11',
	'Zac_Efron':'1987/10/18',
	'Ella_Henderson':'1996/1/12',
	'Anne_Hathaway':'1982/11/12',
	'Kate_Upton':'1992/6/10',
	'Paris_Hilton':'1981/2/17',
	'Claudia_Winkleman':'1972/1/15',
	'Megan_Fox':'1986/5/16',
	'Rowan_Atkinson':'1955/1/6',
	'Amy_Childs':'1990/6/7',
	'Pamela_Anderson':'1967/7/1',
	'Charlotte_Church':'1986/2/21',
	'Whitney_Houston':'1963/8/9',
	'Nicole_Scherzinger':'1978/6/29',
	'Fearne_Cotton':'1981/9/3',
	'Paula_Hamilton':'1961/1/23',
	'Claire_Richards':'1977/8/17',
	'Clint_Eastwood':'1930/5/31',
	'Kourtney_Kardashian':'1979/4/18',
	'Jessica_Alba':'1981/4/28',
	'Cher_Lloyd':'1993/7/28',
	'Bruce_Lee':'1940/11/27',
	'John_Travolta':'1954/2/18',
	'Macaulay_Culkin':'1980/8/26',
	'Fern_Britton':'1957/7/17',
	'Gary_Barlow':'1971/1/20',
	'Ben_Stiller':'1965/11/30',
	'Sigourney_Weaver':'1949/10/8',
	'Kevin_Spacey':'1959/7/26',
	'David_Beckham':'1975/5/2',
	'Ed_Sheeran':'1991/2/17',
	'Olly_Murs':'1984/5/14',
	'Kanye_West':'1977/6/8',
	'Orlando_Bloom':'1977/1/13',
	'Katie_Price':'1978/5/22',
	'Nicki_Minaj':'1982/12/8',
	'Elizabeth_Taylor':'1932/2/27',
	'Alesha_Dixon':'1978/10/7',
	'Nicola_Robert':'1985/10/5',
	'Lacey_Banghard':'1992/4/28',
	'Helen_Flanagan':'1990/8/7',
	'Nelson_Mandela':'1918/7/18',
	'Holly_Willoughby':'1981/2/10',
	'Pippa_Middleton':'1983/9/6',
	'Craig_Revel_Horwood':'1965/1/4',
	'Mel_Gibson':'1956/1/3',
	'Alice_Eve':'1982/2/6',
	'Edward_Norton':'1969/8/18',
	'Prince_Harry':'1984/9/15',
	'Eddie_Redmayne':'1982/1/6',
	'Mila_Kunis':'1983/8/14',
	'Jackie_Chan':'1954/4/7',
	'Samuel_L._Jackson':'1948/12/21',
	'Victoria_Beckham':'1974/4/17',
	'James_Franco':'1978/4/19',
	'Tim_Allen':'1953/6/13',
	'Charlie_Brooks':'1981/5/3',
	'Robin_Williams':'1951/7/21',
	'Paul_Walker':'1973/9/12',
	'Hayden_Panettiere':'1989/8/21',
	'Jim_Carrey':'1962/1/17',
	'Thom_Evans':'1985/4/2',
	'Diana_Vickers':'1991/7/30',
	'Katy_Perry':'1984/10/25',
	'Will_Smith':'1968/9/25',
	'Dougie_Poynter':'1987/11/30',
	'Emma_Watson':'1990/4/15',
	'Taylor_Lautner':'1992/2/11',
	'Jennifer_Lopez':'1969/7/24',
	'Michael_Vaughan':'1974/10/29',
	'Harry_Judd':'1985/12/23',
	'Coleen_Nolan':'1965/3/12',
	'Simon_Cowell':'1959/10/7',
	'Adele':'1988/5/5',
	'Gwyneth_Paltrow':'1972/9/27',
	'Jennifer_Aniston':'1969/2/11',
	'Farrah_Fawcett':'1947/2/2',
	'Tommy_Lee_Jone':'1946/9/15',
	'James_Cameron':'1954/8/16',
	'Shirley_Temple':'1928/4/23',
	'Una_Healy':'1981/10/10',
	'Kara_Tointon':'1983/8/5',
	'Johnny_Ball':'1938/5/23',
	'Patrick_Swayze':'1952/8/18',
	'Cameron_Diaz':'1972/8/30',
	'Beth_Tweddle':'1985/4/1',
	'Spencer_Pratt':'1983/8/14',
	'Kelly_Brook':'1979/11/23',
	'Carolynne_Poole':'1980/8/5',
	'Michael_Jackson':'1958/8/29',
	'Nigella_Lawson':'1960/1/6',
	'Kerry_Katona':'1980/9/6',
	'Kamal_Haasan':'1954/11/7',
	'Nadine_Dorrie':'1957/5/21',
	'Matt_Lapinskas':'1989/2/27',
	'Drew_Barrymore':'1975/2/22',
	'Frankie_Dettori':'1970/12/15',
	'Kimberley_Walsh':'1981/11/20',
	'Keira_Knightley':'1985/3/26',
	'Matt_Damon':'1970/10/8',
	'Blake_Lively':'1987/8/25',
	'Al_Pacino':'1940/4/25',
	'Robbie_Williams':'1974/2/13',
	'Tricia_Penrose':'1970/4/9',
	'Adolf_Hitler':'1889/4/20',
	'Linda_Robson':'1958/3/13',
	'Ryan_Reynolds':'1976/10/23',
	'Chris_Hemsworth':'1983/8/11',
	'Angelina_Jolie':'1975/6/4',
	'Sylvester_Stallone':'1946/7/6',
	'Kelly_Osbourne':'1984/10/27',
	'Kim_Kardashian':'1980/10/21',
	'Eric_Bristow':'1957/4/25',
	'Steven_Spielberg':'1946/12/18',
	'Cara_Delevingne':'1992/8/12',
	'Shah_Rukh_Khan':'1965/11/2',
	'Katie_Hopkins':'1975/2/13',
	'Philip_Seymour_Hoffman':'1967/7/23',
	'Scarlett_Johansson':'1984/11/22',
	'Eva_Mendes':'1974/3/5',
	'Peter_Andre':'1973/2/27',
	'Jessica_Chastain':'1977/3/24',
	'Liam_Neeson':'1952/6/7',
	'Rosamund_Pike':'1979/1/27',
	'Lily_Allen':'1985/5/2',
	'Halle_Berry':'1966/8/14',
	'Jake_Gyllenhaal':'1980/12/19',
	'Ashley_Roberts':'1981/9/14',
	'Seann_William_Scott':'1976/10/3',
	'Shayne_Ward':'1984/10/16',
	'Rochelle_Hume':'1989/3/21',
	'Nicole_Richie':'1981/9/21',
	'Tess_Daly':'1969/4/27',
	'Robert_De_Niro':'1943/8/17',
	'Russell_Brand':'1975/6/4',
	'Robert_Pattinson':'1986/5/13',
	'Heath_Ledger':'1979/4/4'
	})
	with open('birthdate_database.p', 'w') as f:
			pickle.dump(DATABASE, f)
	print "Database updated."


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--name", help="The name of a celebrity whose Date of Birth you want", type=str)
	args = parser.parse_args()
	if args.name:
		open_database()
		searched_name = clean_name(args.name)
		output_name = searched_name.replace("_", " ")
		try:
			if DATABASE.has_key(searched_name):
				print_result(output_name, DATABASE[searched_name])
				find_related_birthdays(searched_name, DATABASE[searched_name])
			else:
				json = request_json_from_api(searched_name)
				birthdate = get_birthdate_from_json_result(json)
				print_result(output_name, birthdate)
				DATABASE[searched_name] = birthdate
				find_related_birthdays(searched_name, DATABASE[searched_name])
				# get_time_since_birthdate(birthdate)
		except:
			print "Sorry, could not find {}'s Date of Birth".format(args.name)
		with open('birthdate_database.p', 'w') as f:
				pickle.dump(DATABASE, f)
	else:
		raise ValueError("No input name received.\nPlease execute file with arg -n 'Celebrity Name'.")

if __name__ == "__main__":
	main()