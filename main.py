import requests, bs4, re, json

##CONSTANTS
main_url = "https://www.pro-football-reference.com"
phi_2017 = "/boxscores/201709100was.htm#all_team_stats"

##FUNCTIONS
def find_team_stats(search_text):
    regex = "<table class=\"stats_table\" id=\"team_stats\""
    x = re.search(regex, search_text)
    return search_text[x.start():]

def get_team_stats(soup, team):
    out_json = {}
    exceptions = ["Rush-Yds-TDs","Cmp-Att-Yd-TD-INT","Sacked-Yards", \
            "Fumbles-Lost", "Penalties-Yards", "Third Down Conv.", \
            "Fourth Down Conv.", "Time of Possession"]
    table = soup.select("table[id='team_stats']")[0]
    #get vis home teams
    main_team = ""
    away_team = ""
    for a in table.tr.select("th"):
        if a.get_text() == team:
            main_team = a.attrs["data-stat"]
    if main_team == "vis_stat":
        away_team = "home_stat"
    else:
        away_team = "vis_stat"
    for a in table.tbody.find_all("tr"):
        header = a.th.get_text()
        if header not in exceptions:
            for b in a.find_all("td"):
                cur_team = b.attrs["data-stat"]
                if main_team == cur_team:
                    temp_tag = "{}_{}".format(team, header)
                    temp_val = b.get_text()
                    out_json[temp_tag]=temp_val
                else:
                    temp_tag = "{}_{}".format("OPP", header)
                    temp_val = b.get_text()
                    out_json[temp_tag]=temp_val
        else:
            if header == "Rush-Yds-TDs":
                for b in a.find_all("td"):
                    cur_team = b.attrs["data-stat"]
                    if main_team != cur_team:
                        cur_team = "OPP"
                    else:
                        cur_team = team
                    temp_tag = "{}_{}".format(cur_team, "Yds\\Rush")
                    raw_val = b.get_text()
                    raw_val = raw_val.split("-")
                    ##CONVERT TO FLOAT
                    for c in range(0,len(raw_val)):
                        raw_val[c] = float(raw_val[c])
                    temp_val = raw_val[1] / raw_val[0]
                    out_json[temp_tag] = temp_val
                    temp_tag = "{}_{}".format(cur_team, "Rush Attempts")
                    temp_val = raw_val[0]
                    out_json[temp_tag] = temp_val
                    temp_tag = "{}_{}".format(cur_team, "Rush TDs")
                    temp_val = raw_val[2]
                    out_json[temp_tag] = temp_val
            elif header == "Cmp-Att-Yd-TD-INT":
                for b in a.find_all("td"):
                    cur_team = b.attrs["data-stat"]
                    if main_team != cur_team:
                        cur_team = "OPP"
                    else:
                        cur_team = team
                    temp_tag = "{}_{}".format(cur_team, "Cmp\\Attempt")
                    raw_val = b.get_text()
                    raw_val = raw_val.split("-")
                    ##CONVERT TO FLOAT
                    for c in range(0,len(raw_val)):
                        raw_val[c] = float(raw_val[c])
                    temp_val = raw_val[0] / raw_val[1]
                    out_json[temp_tag] = temp_val
                    temp_tag = "{}_{}".format(cur_team, "Passing TDs")
                    temp_val = raw_val[3]
                    out_json[temp_tag] = temp_val
                    temp_tag = "{}_{}".format(cur_team, "Interceptions")
                    temp_val = raw_val[4]
                    out_json[temp_tag] = temp_val
            elif header == "Sacked-Yards":
                for b in a.find_all("td"):
                    cur_team = b.attrs["data-stat"]
                    if main_team != cur_team:
                        cur_team = "OPP"
                    else:
                        cur_team = team
                    temp_tag = "{}_{}".format(cur_team, "Sacked")
                    raw_val = b.get_text()
                    raw_val = raw_val.split("-")
                    ##CONVERT TO FLOAT
                    for c in range(0,len(raw_val)):
                        raw_val[c] = float(raw_val[c])
                    temp_val = raw_val[0]
                    out_json[temp_tag] = temp_val
            elif header == "Fumbles-Lost":
                for b in a.find_all("td"):
                    cur_team = b.attrs["data-stat"]
                    if main_team != cur_team:
                        cur_team = "OPP"
                    else:
                        cur_team = team
                    temp_tag = "{}_{}".format(cur_team, "Fumbles")
                    raw_val = b.get_text()
                    raw_val = raw_val.split("-")
                    ##CONVERT TO FLOAT
                    for c in range(0,len(raw_val)):
                        raw_val[c] = float(raw_val[c])
                    temp_val = raw_val[0]
                    out_json[temp_tag] = temp_val
            elif header == "Penalties-Yards":
                for b in a.find_all("td"):
                    cur_team = b.attrs["data-stat"]
                    if main_team != cur_team:
                        cur_team = "OPP"
                    else:
                        cur_team = team
                    temp_tag = "{}_{}".format(cur_team, "Fumbles")
                    raw_val = b.get_text()
                    raw_val = raw_val.split("-")
                    ##CONVERT TO FLOAT
                    for c in range(0,len(raw_val)):
                        raw_val[c] = float(raw_val[c])
                    temp_val = raw_val[0]
                    out_json[temp_tag] = temp_val

    print(out_json)
    return out_json

##test run
res = requests.get(main_url+phi_2017)
table_grab = find_team_stats(res.text)
table_soup = bs4.BeautifulSoup(table_grab, "html.parser")
data_dump = get_team_stats(table_soup, "PHI")
print(json.dumps(data_dump, sort_keys=True, indent=4))
