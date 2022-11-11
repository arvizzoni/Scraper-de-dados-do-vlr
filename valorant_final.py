import mechanicalsoup
import os
import re
import pandas
import time

# GET MATCH LINKS
list_links = []
with open ('valorant match links.txt', 'r') as f:
    list_links.append(f.read().split('\n'))
browser = mechanicalsoup.StatefulBrowser()
browser.open('https://www.vlr.gg/matches/results')
match_link_soup = browser.get_current_page()

match_link_sub_soup = match_link_soup.find('div', class_='col mod-1')
total_pages = match_link_sub_soup.find_all('a', href = True)[-1].text

l_page_links = []
l_match_links = []
links = match_link_sub_soup.find_all('a', href = True)
link = [l_match_links.append('https://www.vlr.gg'+l['href']) for l in links[2:-4]]

for page_num in range(1,int(total_pages)+1):
    l_page_links.append(f'https://www.vlr.gg/matches/results/?page={page_num}')

for match_link_in_page_num in l_page_links:
    browser.open(match_link_in_page_num)
    match_link_soup = browser.get_current_page()
    match_link_sub_soup = match_link_soup.find('div', class_='col mod-1')

    match_links = match_link_sub_soup.find_all('a', href=True)
    match_link = ['https://www.vlr.gg' + l['href'] for l in match_links]
    for link_of_match in match_link:
        if re.search('^https://www.vlr.gg/matches', link_of_match):
            continue
        l_match_links.append(link_of_match)
    print(match_link_in_page_num)

l_new_links = []
for link in list_links:
    for links in l_match_links:
        if links in link:
            break
        else:
            l_new_links.append(links)

with open('valorant match links.txt', 'w') as f:
    for link in l_new_links:
        f.write(link+'\n')
    f.close()

list_links = []
list_link = []

with open ('valorant match links.txt', 'r') as f:
    list_links.append(f.read().split())

for links in list_links:
    for link in links:
        list_link.append(link)

# CREATE MAIN FOLDER -- "VALORANT"
try:
    os.makedirs('valorant')
except Exception as e:
    pass

for valorant_match_link in list_link:
    print(valorant_match_link)
    valorant_browser = mechanicalsoup.StatefulBrowser()

    try:
        valorant_browser.open(valorant_match_link)
    except:
        time.sleep(30)
        try:
            print('Second try')
            valorant_browser.open(valorant_match_link)
        except:
            time.sleep(30)
            try:
                print('Third try')
                valorant_browser.open(valorant_match_link)
            except:
                time.sleep(30)
                print('Fourth try')
                valorant_browser.open(valorant_match_link)
    valorant_soup = valorant_browser.get_current_page()

    # MATCH ID
    id_match = valorant_browser.get_url().split('/')[3].strip()

    # CREATE SUB FOLDER -- NAME -- MATCH ID
    try:
        os.makedirs(f'valorant/{id_match}')
    except OSError as e:
        pass

    # MATCH HEADER DATA
    ## MATCH NAME STAGE AND TYPR
    match_name = valorant_soup.find('title').text.strip().split('|')[1].strip()
    match_stage = valorant_soup.find('title').text.strip().split('|')[2].strip()
    match_type = valorant_soup.find('div', class_='match-header-event-series').text.strip().split('\n')[-1].strip()

    ## MATCH DATE AND TIME
    soup_header_date_and_time = valorant_soup.find('div', class_='match-header-date')
    match_date = soup_header_date_and_time.find_all('div')[0].text.strip()
    try:
        match_time = soup_header_date_and_time.find_all('div')[1].text.strip()
    except:
        continue

    ## MATCH HEADER -- TOP AND BOTTOM OF 'VS' -- NOTE
    match_header_vs_note_top = valorant_soup.find_all('div', class_='match-header-vs-note')[0].text.strip()
    match_header_vs_note_bottom = valorant_soup.find_all('div', class_='match-header-vs-note')[1].text.strip()

    ## FIRST TEAM DATA
    first_team_name = valorant_soup.find_all('div', class_='wf-title-med')[0].text.strip()
    first_team_elo_number = valorant_soup.find_all('div', class_='match-header-link-name-elo')[0].text.strip()
    first_team_score = valorant_soup.find('div', class_='js-spoiler').text.strip().split('\n')[0].strip()

    ## SECOND TEAM DATA
    second_team_name = valorant_soup.find_all('div', class_='wf-title-med')[1].text.strip()
    second_team_elo_number = valorant_soup.find_all('div', class_='match-header-link-name-elo')[1].text.strip()
    second_team_score = valorant_soup.find('div', class_='js-spoiler').text.strip().split('\n')[-1].strip()

    ## BETTING SECTION
    list_betting_data = []
    list_betting_final_data = []

    try:
        valorant_soup.find('a', class_='wf-card mod-dark match-bet-item')
        for betting_data in valorant_soup.find('a', class_='wf-card mod-dark match-bet-item').text.strip().split('\n'):
            list_betting_data.append(betting_data)

        for betting_data_num in range(len(list_betting_data)):
            list_betting_final_data.append(list_betting_data[betting_data_num].strip())

        betting_line = list_betting_final_data[0] + ' '
        for n in range(1, len(list_betting_final_data)):
            betting_line += (list_betting_final_data[n] + ' ')

        list_betting_data.clear()
        list_betting_final_data.clear()
    except:
        betting_line = 'Visit GG BET for valorant bets'

    # SAVE HEADER DATA TO FILES
    team_data = {
        'Team': [first_team_name, second_team_name],
        'Score': [first_team_score, second_team_score],
        'ELO Number': [first_team_elo_number, second_team_elo_number]
    }

    match_header_dataframe = pandas.DataFrame(team_data)
    match_header_dataframe.to_excel(rf'valorant/{id_match}/Team score.xlsx', index=False)
    with open(rf'valorant/{id_match}/header data.txt', 'w', encoding="utf-8") as f:
        f.write(
            str('Match Id: ' + id_match + '\n''Match Name: ' + match_name + '\n''Match Stage: ' + match_stage + '\n''Match Type: ' + match_type + '\n''Match Date: ' + match_date + '\n''Match Time: ' + match_time + '\n''Match Score Type: ' + match_header_vs_note_top + '\n''Match Note: ' + match_header_vs_note_bottom + '\n\n'))
        f.write(
            str('Team1: ' + first_team_name + ', Score: ' + first_team_score + ', Elo Number: ' + first_team_elo_number + '\n\n'))
        f.write(
            str('Team2: ' + second_team_name + ', Score: ' + second_team_score + ', Elo Number: ' + second_team_elo_number + '\n\n'))
        f.write(str('Betting line: ' + betting_line))

    # MATCH LINKS -- OVERVIEW, PERFORMANCE AND ECONOMY
    soup_table_top_category = valorant_soup.find('div', class_='vm-stats-tabnav')
    link_overview = 'https://www.vlr.gg' + soup_table_top_category.find_all('a')[0]['href']
    link_performance = 'https://www.vlr.gg' + soup_table_top_category.find_all('a')[1]['href']
    link_economy = 'https://www.vlr.gg' + soup_table_top_category.find_all('a')[2]['href']
    try:
        soup_name_of_maps = valorant_soup.find('div', class_='vm-stats-gamesnav')
        try:
            soup_name_of_maps.find('div').text.strip()
            # NAME OF MAPS
            list_name_of_maps_all_names = []
            list_name_of_maps = []
            name_of_allmaps_tab = soup_name_of_maps.find('div').text.strip()

            names_of_maps = soup_name_of_maps.find_all('div')[1:]
            name_of_map = [list_name_of_maps_all_names.append(map.text.strip().split('\n')[-1].strip()) for map in
                           names_of_maps]
            for map_name in list_name_of_maps_all_names:
                list_name_of_maps.append(map_name)

            list_name_of_maps.insert(2, name_of_allmaps_tab)
            list_name_of_maps.insert(2, name_of_allmaps_tab)



            # .................................................................................OVERVIEW...................................................................



            # CREATE OVERVIEW FOLDER
            try:
                os.makedirs(f'valorant/{id_match}/overview')
            except OSError as e:
                pass

            valorant_browser.open(link_overview)

            # OVERVIEW TABLES -- ALL CATEGORY

            for num in range(0, ((int(first_team_score) + int(second_team_score) + 1) * 2), 2):
                tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num]
                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                l_name = []
                l_team = []
                l_char_name_1 = []
                l_char_name_2 = []
                l_char_name_3 = []
                l_char_name_4 = []
                l_char_name_5 = []
                l_acs = []
                l_k = []
                l_d = []
                l_a = []
                l_p_or_m = []
                l_kast = []
                l_adr = []
                l_hs = []
                l_fk = []
                l_fd = []
                l_p_or_m1 = []

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 0:
                            char_name_1 = '-'
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        elif len(char_name) == 5:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[0]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[0]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[0]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[0]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[0]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[0]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split('\n')[0]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[0]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')
                        try:
                            fk = data[d_num][10].split('\n')[0]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[0]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[0]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num + 1]
                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 0:
                            char_name_1 = '-'
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'

                        elif len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        elif len(char_name) == 5:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[0]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[0]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[0]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[0]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[0]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[0]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split('\n')[0]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[0]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')
                        try:
                            fk = data[d_num][10].split('\n')[0]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[0]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[0]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                data_overview_all = {
                    'Name': l_name,
                    'Team': l_team,
                    'Character 1': l_char_name_1,
                    'Character 2': l_char_name_2,
                    'Character 3': l_char_name_3,
                    'Character 4': l_char_name_4,
                    'Character 5': l_char_name_5,
                    'ACS': l_acs,
                    'K': l_k,
                    'D': l_d,
                    'A': l_a,
                    '+/-': l_p_or_m,
                    'KAST': l_kast,
                    'ADR': l_adr,
                    'HS%': l_hs,
                    'FK': l_fk,
                    'FD': l_fd,
                    "'+/-'": l_p_or_m1
                }

                df = pandas.DataFrame(data_overview_all)
                df.drop_duplicates(inplace=True)

                try:
                    os.makedirs(f'valorant/{id_match}/overview/{list_name_of_maps[num]}')
                except OSError as e:
                    pass

                df.to_excel(rf'valorant/{id_match}/overview/{list_name_of_maps[num]}/all.xlsx', index=False)

                l_name.clear()
                l_team.clear()
                l_char_name_1.clear()
                l_char_name_2.clear()
                l_char_name_3.clear()
                l_char_name_4.clear()
                l_char_name_5.clear()
                l_acs.clear()
                l_k.clear()
                l_d.clear()
                l_a.clear()
                l_p_or_m.clear()
                l_kast.clear()
                l_adr.clear()
                l_hs.clear()
                l_fk.clear()
                l_fd.clear()
                l_p_or_m1.clear()

            # OVERVIEW TABLES -- "ATTACK" CATEGORY
            try:
                for num in range(0, ((int(first_team_score) + int(second_team_score) + 1) * 2), 2):
                    tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num]
                    data = []
                    for content in tables.find_all('tr'):
                        row_data = content.find_all('td')
                        row = [l.text.strip() for l in row_data]
                        data.append(row)

                    l_name = []
                    l_team = []
                    l_char_name_1 = []
                    l_char_name_2 = []
                    l_char_name_3 = []
                    l_char_name_4 = []
                    l_char_name_5 = []
                    l_acs = []
                    l_k = []
                    l_d = []
                    l_a = []
                    l_p_or_m = []
                    l_kast = []
                    l_adr = []
                    l_hs = []
                    l_fk = []
                    l_fd = []
                    l_p_or_m1 = []

                    for d_num in range(1, 6):
                        for table_num in range(3):
                            player_name = data[d_num][0].split('\n')[0].strip()
                            l_name.append(player_name)

                            player_team = data[d_num][0].split('\n')[-1].strip()
                            l_team.append(player_team)

                            char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                            char_name = [l['alt'] for l in char_names]

                            if len(char_name) == 1:
                                char_name_1 = char_name[0]
                                char_name_2 = '-'
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 2:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 3:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 4:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = '-'
                            else:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = char_name[4]

                            l_char_name_1.append(char_name_1)
                            l_char_name_2.append(char_name_2)
                            l_char_name_3.append(char_name_3)
                            l_char_name_4.append(char_name_4)
                            l_char_name_5.append(char_name_5)

                            try:
                                acs = data[d_num][2].split('\n')[1]
                                l_acs.append(acs)
                            except:
                                l_acs.append('-')

                            try:
                                k = data[d_num][3].split('\n')[1]
                                l_k.append(k)
                            except:
                                l_k.append('-')

                            try:
                                d = data[d_num][4].replace('/', '').strip().split('\n')[1]
                                l_d.append(d)
                            except:
                                l_d.append('-')

                            try:
                                a = data[d_num][5].split('\n')[1]
                                l_a.append(a)
                            except:
                                l_a.append('-')

                            try:
                                p_or_m = data[d_num][6].split('\n')[1]
                                l_p_or_m.append(p_or_m)
                            except:
                                l_p_or_m.append('-')

                            try:
                                kast = data[d_num][7].split('\n')[1]
                                l_kast.append(kast)
                            except:
                                l_kast.append('-')

                            try:
                                adr = data[d_num][8].split()[1]
                                l_adr.append(adr)
                            except:
                                l_adr.append('-')

                            try:
                                hs = data[d_num][9].split('\n')[1]
                                l_hs.append(hs)
                            except:
                                l_hs.append('-')

                            try:
                                fk = data[d_num][10].split('\n')[1]
                                l_fk.append(fk)
                            except:
                                l_fk.append('-')

                            try:
                                fd = data[d_num][11].split('\n')[1]
                                l_fd.append(fd)
                            except:
                                l_fd.append('-')

                            try:
                                p_or_m1 = data[d_num][12].split('\n')[1]
                                l_p_or_m1.append(p_or_m1)
                            except:
                                l_p_or_m1.append('-')

                    tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num + 1]
                    data = []
                    for content in tables.find_all('tr'):
                        row_data = content.find_all('td')
                        row = [l.text.strip() for l in row_data]
                        data.append(row)

                    for d_num in range(1, 6):
                        for table_num in range(3):
                            player_name = data[d_num][0].split('\n')[0].strip()
                            l_name.append(player_name)

                            player_team = data[d_num][0].split('\n')[-1].strip()
                            l_team.append(player_team)

                            char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                            char_name = [l['alt'] for l in char_names]

                            if len(char_name) == 1:
                                char_name_1 = char_name[0]
                                char_name_2 = '-'
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 2:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 3:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 4:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = '-'
                            else:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = char_name[4]

                            l_char_name_1.append(char_name_1)
                            l_char_name_2.append(char_name_2)
                            l_char_name_3.append(char_name_3)
                            l_char_name_4.append(char_name_4)
                            l_char_name_5.append(char_name_5)

                            try:
                                acs = data[d_num][2].split('\n')[1]
                                l_acs.append(acs)
                            except:
                                l_acs.append('-')

                            try:
                                k = data[d_num][3].split('\n')[1]
                                l_k.append(k)
                            except:
                                l_k.append('-')

                            try:
                                d = data[d_num][4].replace('/', '').strip().split('\n')[1]
                                l_d.append(d)
                            except:
                                l_d.append('-')

                            try:
                                a = data[d_num][5].split('\n')[1]
                                l_a.append(a)
                            except:
                                l_a.append('-')

                            try:
                                p_or_m = data[d_num][6].split('\n')[1]
                                l_p_or_m.append(p_or_m)
                            except:
                                l_p_or_m.append('-')

                            try:
                                kast = data[d_num][7].split('\n')[1]
                                l_kast.append(kast)
                            except:
                                l_kast.append('-')

                            try:
                                adr = data[d_num][8].split()[1]
                                l_adr.append(adr)
                            except:
                                l_adr.append('-')

                            try:
                                hs = data[d_num][9].split('\n')[1]
                                l_hs.append(hs)
                            except:
                                l_hs.append('-')

                            try:
                                fk = data[d_num][10].split('\n')[1]
                                l_fk.append(fk)
                            except:
                                l_fk.append('-')

                            try:
                                fd = data[d_num][11].split('\n')[1]
                                l_fd.append(fd)
                            except:
                                l_fd.append('-')

                            try:
                                p_or_m1 = data[d_num][12].split('\n')[1]
                                l_p_or_m1.append(p_or_m1)
                            except:
                                l_p_or_m1.append('-')

                    data_overview_all_maps_all = {
                        'Name': l_name,
                        'Team': l_team,
                        'Character 1': l_char_name_1,
                        'Character 2': l_char_name_2,
                        'Character 3': l_char_name_3,
                        'Character 4': l_char_name_4,
                        'Character 5': l_char_name_5,
                        'ACS': l_acs,
                        'K': l_k,
                        'D': l_d,
                        'A': l_a,
                        '+/-': l_p_or_m,
                        'KAST': l_kast,
                        'ADR': l_adr,
                        'HS%': l_hs,
                        'FK': l_fk,
                        'FD': l_fd,
                        "'+//-'": l_p_or_m1
                    }

                    df = pandas.DataFrame(data_overview_all_maps_all)
                    df.drop_duplicates(inplace=True)
                    df.to_excel(rf'valorant/{id_match}/overview/{list_name_of_maps[num]}/attack.xlsx', index=False)

                    l_name.clear()
                    l_team.clear()
                    l_char_name_1.clear()
                    l_char_name_2.clear()
                    l_char_name_3.clear()
                    l_char_name_4.clear()
                    l_char_name_5.clear()
                    l_acs.clear()
                    l_k.clear()
                    l_d.clear()
                    l_a.clear()
                    l_p_or_m.clear()
                    l_kast.clear()
                    l_adr.clear()
                    l_hs.clear()
                    l_fk.clear()
                    l_fd.clear()
                    l_p_or_m1.clear()
            except:
                pass

            # OVERVIEW TABLES -- "DEFEND" CATEGORY
            try:
                for num in range(0, ((int(first_team_score) + int(second_team_score) + 1) * 2), 2):
                    tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num]

                    data = []
                    for content in tables.find_all('tr'):
                        row_data = content.find_all('td')
                        row = [l.text.strip() for l in row_data]
                        data.append(row)

                    l_name = []
                    l_team = []
                    l_char_name_1 = []
                    l_char_name_2 = []
                    l_char_name_3 = []
                    l_char_name_4 = []
                    l_char_name_5 = []
                    l_acs = []
                    l_k = []
                    l_d = []
                    l_a = []
                    l_p_or_m = []
                    l_kast = []
                    l_adr = []
                    l_hs = []
                    l_fk = []
                    l_fd = []
                    l_p_or_m1 = []

                    for d_num in range(1, 6):
                        for table_num in range(3):
                            player_name = data[d_num][0].split('\n')[0].strip()
                            l_name.append(player_name)

                            player_team = data[d_num][0].split('\n')[-1].strip()
                            l_team.append(player_team)

                            char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                            char_name = [l['alt'] for l in char_names]

                            if len(char_name) == 1:
                                char_name_1 = char_name[0]
                                char_name_2 = '-'
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 2:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 3:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 4:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = '-'
                            else:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = char_name[4]

                            l_char_name_1.append(char_name_1)
                            l_char_name_2.append(char_name_2)
                            l_char_name_3.append(char_name_3)
                            l_char_name_4.append(char_name_4)
                            l_char_name_5.append(char_name_5)

                            try:
                                acs = data[d_num][2].split('\n')[2]
                                l_acs.append(acs)
                            except:
                                l_acs.append('-')

                            try:
                                k = data[d_num][3].split('\n')[2]
                                l_k.append(k)
                            except:
                                l_k.append('-')

                            try:
                                d = data[d_num][4].replace('/', '').strip().split('\n')[2]
                                l_d.append(d)
                            except:
                                l_d.append('-')

                            try:
                                a = data[d_num][5].split('\n')[2]
                                l_a.append(a)
                            except:
                                l_a.append('-')

                            try:
                                p_or_m = data[d_num][6].split('\n')[2]
                                l_p_or_m.append(p_or_m)
                            except:
                                l_ - p_or_m.append('-')

                            try:
                                kast = data[d_num][7].split('\n')[2]
                                l_kast.append(kast)
                            except:
                                l_kast.append('-')

                            try:
                                adr = data[d_num][8].split()[2]
                                l_adr.append(adr)
                            except:
                                l_adr.append('-')

                            try:
                                hs = data[d_num][9].split('\n')[2]
                                l_hs.append(hs)
                            except:
                                l_hs.append('-')

                            try:
                                fk = data[d_num][10].split('\n')[2]
                                l_fk.append(fk)
                            except:
                                l_fk.append('-')

                            try:
                                fd = data[d_num][11].split('\n')[2]
                                l_fd.append(fd)
                            except:
                                l_fd.append('-')
                            try:
                                p_or_m1 = data[d_num][12].split('\n')[2]
                                l_p_or_m1.append(p_or_m1)
                            except:
                                l_p_or_m1.append('-')

                    tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[num + 1]

                    data = []
                    for content in tables.find_all('tr'):
                        row_data = content.find_all('td')
                        row = [l.text.strip() for l in row_data]
                        data.append(row)

                    for d_num in range(1, 6):
                        for table_num in range(3):
                            player_name = data[d_num][0].split('\n')[0].strip()
                            l_name.append(player_name)

                            player_team = data[d_num][0].split('\n')[-1].strip()
                            l_team.append(player_team)

                            char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                            char_name = [l['alt'] for l in char_names]

                            if len(char_name) == 1:
                                char_name_1 = char_name[0]
                                char_name_2 = '-'
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 2:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = '-'
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 3:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = '-'
                                char_name_5 = '-'
                            elif len(char_name) == 4:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = '-'
                            else:
                                char_name_1 = char_name[0]
                                char_name_2 = char_name[1]
                                char_name_3 = char_name[2]
                                char_name_4 = char_name[3]
                                char_name_5 = char_name[4]

                            l_char_name_1.append(char_name_1)
                            l_char_name_2.append(char_name_2)
                            l_char_name_3.append(char_name_3)
                            l_char_name_4.append(char_name_4)
                            l_char_name_5.append(char_name_5)

                            try:
                                acs = data[d_num][2].split('\n')[2]
                                l_acs.append(acs)
                            except:
                                l_acs.append('-')

                            try:
                                k = data[d_num][3].split('\n')[2]
                                l_k.append(k)
                            except:
                                l_k.append('-')

                            try:
                                d = data[d_num][4].replace('/', '').strip().split('\n')[2]
                                l_d.append(d)
                            except:
                                l_d.append('-')

                            try:
                                a = data[d_num][5].split('\n')[2]
                                l_a.append(a)
                            except:
                                l_a.append('-')

                            try:
                                p_or_m = data[d_num][6].split('\n')[2]
                                l_p_or_m.append(p_or_m)
                            except:
                                l_ - p_or_m.append('-')

                            try:
                                kast = data[d_num][7].split('\n')[2]
                                l_kast.append(kast)
                            except:
                                l_kast.append('-')

                            try:
                                adr = data[d_num][8].split()[2]
                                l_adr.append(adr)
                            except:
                                l_adr.append('-')

                            try:
                                hs = data[d_num][9].split('\n')[2]
                                l_hs.append(hs)
                            except:
                                l_hs.append('-')

                            try:
                                fk = data[d_num][10].split('\n')[2]
                                l_fk.append(fk)
                            except:
                                l_fk.append('-')

                            try:
                                fd = data[d_num][11].split('\n')[2]
                                l_fd.append(fd)
                            except:
                                l_fd.append('-')
                            try:
                                p_or_m1 = data[d_num][12].split('\n')[2]
                                l_p_or_m1.append(p_or_m1)
                            except:
                                l_p_or_m1.append('-')

                    data_overview_all_maps_all = {
                        'Name': l_name,
                        'Team': l_team,
                        'Character 1': l_char_name_1,
                        'Character 2': l_char_name_2,
                        'Character 3': l_char_name_3,
                        'Character 4': l_char_name_4,
                        'Character 5': l_char_name_5,
                        'ACS': l_acs,
                        'K': l_k,
                        'D': l_d,
                        'A': l_a,
                        '+/-': l_p_or_m,
                        'KAST': l_kast,
                        'ADR': l_adr,
                        'HS%': l_hs,
                        'FK': l_fk,
                        'FD': l_fd,
                        "'+//-'": l_p_or_m1
                    }

                    df = pandas.DataFrame(data_overview_all_maps_all)
                    df.drop_duplicates(inplace=True)
                    df.to_excel(rf'valorant/{id_match}/overview/{list_name_of_maps[num]}/defend.xlsx', index=False)

                    l_name.clear()
                    l_team.clear()
                    l_char_name_1.clear()
                    l_char_name_2.clear()
                    l_char_name_3.clear()
                    l_char_name_4.clear()
                    l_char_name_5.clear()
                    l_acs.clear()
                    l_k.clear()
                    l_d.clear()
                    l_a.clear()
                    l_p_or_m.clear()
                    l_kast.clear()
                    l_adr.clear()
                    l_hs.clear()
                    l_fk.clear()
                    l_fd.clear()
                    l_p_or_m1.clear()
            except:
                pass

            # OVERVIEW MAP HEAD DATA
            list_map_head_team_names = []
            list_map_head_team_scores = []
            list_map_head_team_slash_scores = []
            list_map_head_map_name = []
            list_map_head_match_duration = []

            for map_head_data_num in range(int(first_team_score) + int(second_team_score)):

                soup_table_head = valorant_soup.find_all('div', class_='vm-stats-game-header')[map_head_data_num]

                name_team1_table_head = soup_table_head.find_all('div', class_='team-name')[0].text.strip()
                list_map_head_team_names.append(name_team1_table_head)

                team1_score_table_head = soup_table_head.find_all('div', class_='score')[0].text.strip()
                list_map_head_team_scores.append(team1_score_table_head)

                team1_slash_score = soup_table_head.find('div', class_='team').find_all('span')

                slash_score1 = [l.text for l in team1_slash_score]

                if team1_slash_score[0]['class'] == ['mod-ct']:
                    if team1_slash_score[1]['class'] == ['mod-t']:
                        if len(slash_score1) == 2:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[green]' + '/' + slash_score1[1] + '[red]')
                        elif len(slash_score1) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[green]' + '/' + slash_score1[1] + '[red]' + '/' + slash_score1[2])
                    else:
                        if len(slash_score1) == 2:
                            list_map_head_team_slash_scores.append(slash_score1[0] + '[green]' + '/' + slash_score1[1])
                        elif len(slash_score1) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[green]' + '/' + slash_score1[1] + '/' + slash_score1[2] + '[red]')
                elif team1_slash_score[0]['class'] == ['mod-t']:
                    if team1_slash_score[1]['class'] == ['mod-ct']:
                        if len(slash_score1) == 2:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[red]' + '/' + slash_score1[1] + '[green]')
                        elif len(slash_score1) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[red]' + '/' + slash_score1[1] + '[green]' + '/' + slash_score1[2])
                    else:
                        if len(slash_score1) == 2:
                            list_map_head_team_slash_scores.append(slash_score1[0] + '[red]' + '/' + slash_score1[1])
                        elif len(slash_score1) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score1[0] + '[red]' + '/' + slash_score1[1] + '/' + slash_score1[2] + '[green]')
                else:
                    if len(slash_score1) == 2:
                        list_map_head_team_slash_scores.append(slash_score1[0] + '/' + slash_score1[1])
                    elif len(slash_score1) == 3:
                        list_map_head_team_slash_scores.append(slash_score1[0] + '/' + slash_score1[1] + '/' + slash_score1[2])

                name_team2_table_head = soup_table_head.find_all('div', class_='team-name')[1].text.strip()
                list_map_head_team_names.append(name_team2_table_head)

                team2_score_table_head = soup_table_head.find_all('div', class_='score')[1].text.strip()
                list_map_head_team_scores.append(team2_score_table_head)

                team2_slash_score = soup_table_head.find('div', class_='team mod-right').find_all('span')

                slash_score2 = [l.text for l in team2_slash_score]

                if team2_slash_score[0]['class'] == ['mod-ct']:
                    if team2_slash_score[1]['class'] == ['mod-t']:
                        if len(slash_score2) == 2:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[green]' + '/' + slash_score2[1] + '[red]')
                        elif len(slash_score2) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[green]' + '/' + slash_score2[1] + '[red]' + '/' + slash_score2[2])
                    else:
                        if len(slash_score2) == 2:
                            list_map_head_team_slash_scores.append(slash_score2[0] + '[green]' + '/' + slash_score2[1])
                        elif len(slash_score2) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[green]' + '/' + slash_score2[1] + '/' + slash_score2[2] + '[red]')
                elif team2_slash_score[0]['class'] == ['mod-t']:
                    if team2_slash_score[1]['class'] == ['mod-ct']:
                        if len(slash_score2) == 2:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[red]' + '/' + slash_score2[1] + '[green]')
                        elif len(slash_score2) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[red]' + '/' + slash_score2[1] + '[green]' + '/' + slash_score2[2])
                    else:
                        if len(slash_score2) == 2:
                            list_map_head_team_slash_scores.append(slash_score2[0] + '[red]' + '/' + slash_score2[1])
                        elif len(slash_score2) == 3:
                            list_map_head_team_slash_scores.append(
                                slash_score2[0] + '[red]' + '/' + slash_score2[1] + '/' + slash_score2[2] + '[green]')
                else:
                    if len(slash_score2) == 2:
                        list_map_head_team_slash_scores.append(slash_score2[0] + '/' + slash_score2[1])
                    elif len(slash_score2) == 3:
                        list_map_head_team_slash_scores.append(slash_score2[0] + '/' + slash_score2[1] + '/' + slash_score2[2])

                map_name_table_head = soup_table_head.find('div', class_='map').text.strip().split('\n')[0].strip()
                list_map_head_map_name.append(map_name_table_head)
                list_map_head_map_name.append(map_name_table_head)

                match_duration_table_head = soup_table_head.find('div', class_='map').text.strip().split('\n')[-1].strip()
                list_map_head_match_duration.append(match_duration_table_head)
                list_map_head_match_duration.append(match_duration_table_head)

            map_head_data_dct = {
                'Map Name': list_map_head_map_name,
                'Match Duration': list_map_head_match_duration,
                'Team Name': list_map_head_team_names,
                'Score': list_map_head_team_scores,
                'Slash Score': list_map_head_team_slash_scores
            }

            map_head_dataframe = pandas.DataFrame(map_head_data_dct)

            try:
                os.makedirs(f'valorant/{id_match}/overview/#table head data')
            except OSError as e:
                pass
            map_head_dataframe.to_excel(f'valorant/{id_match}/overview/#table head data/table head data.xlsx', index=False)

            list_map_head_map_name.clear()
            list_map_head_match_duration.clear()
            list_map_head_team_names.clear()
            list_map_head_team_scores.clear()
            list_map_head_team_slash_scores.clear()

            # OVERVIEW MAP HEAD TABLES
            try:
                os.makedirs(f'valorant/{id_match}/overview/#map head tables')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            list_data_mapheadtable_team1 = []
            list_data_mapheadtable_team2 = []

            for map_head_table_num in range(int(first_team_score) + int(second_team_score)):
                soup_map_head_table = valorant_soup.find_all('div', class_='vlr-rounds')[map_head_table_num]
                map_head_table_total_num_of_col = int(
                    soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[-1].find('div',
                                                                                              class_='rnd-num').text.strip())

                try:
                    for map_head_col_num in range(1, map_head_table_total_num_of_col + 4):
                        map_head_table_col = soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[map_head_col_num]
                        if soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[map_head_col_num]['class'] == [
                            'vlr-rounds-row-col', 'mod-spacing']:
                            continue
                        elif \
                        soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[map_head_col_num].find_all('div')[1][
                            'class'] == ['team']:
                            continue
                        elif map_head_table_col.find('div', class_='rnd-num').find_next_sibling()['class'] == ['rnd-sq']:
                            list_data_mapheadtable_team1.append('-')
                            action_string = \
                            map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find_next_sibling().find(
                                'img')['src']
                            action_name = action_string.split('/')[-1].split('.')[0]
                            if \
                            map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find_next_sibling()['class'][
                                2] == 'mod-ct':
                                list_data_mapheadtable_team2.append(action_name + '[green]')
                            else:
                                list_data_mapheadtable_team2.append(action_name + '[red]')
                        else:
                            action_string = map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find('img')[
                                'src']
                            action_name = action_string.split('/')[-1].split('.')[0]
                            if map_head_table_col.find('div', class_='rnd-num').find_next_sibling()['class'][2] == 'mod-ct':
                                list_data_mapheadtable_team1.append(action_name + '[green]')
                            else:
                                list_data_mapheadtable_team1.append(action_name + '[red]')
                            list_data_mapheadtable_team2.append('-')
                except Exception as e:
                    pass

                try:
                    map_head_tables_dataframe = pandas.DataFrame({
                        f'{first_team_name}': list_data_mapheadtable_team1,
                        f'{second_team_name}': list_data_mapheadtable_team2
                    })
                except:
                    map_head_tables_dataframe = pandas.DataFrame({
                        f'{first_team_name}': list_data_mapheadtable_team1[:len(list_data_mapheadtable_team1) - 1],
                        f'{second_team_name}': list_data_mapheadtable_team2
                    })
                map_head_tables_dataframe.to_excel(
                    f'valorant/{id_match}/overview/#map head tables/{list_name_of_maps_all_names[::2][map_head_table_num]}.xlsx',
                    index=False)

                list_data_mapheadtable_team1.clear()
                list_data_mapheadtable_team2.clear()



            # .............................................................................PERFORMANCE.................................................................



            # CREATE PERFORMANCE FOLDER
            try:
                os.makedirs(f'valorant/{id_match}/performance')
            except OSError as e:
                pass

            valorant_browser.open(link_performance)
            performance_soup = valorant_browser.get_current_page()

            # PERFORMANCE TABLES -- "ALL KILLS" CATEGORY
            list_performance_name_maps = list_name_of_maps_all_names[::2]
            list_performance_name_maps.insert(0, name_of_allmaps_tab)

            list_performance_header = []
            list_performance_index = []

            try:
                performance_allkills_headersoup = \
                performance_soup.find_all('table', class_='wf-table-inset mod-matrix mod-normal')[0]

                performance_headstag = performance_allkills_headersoup.find('tr')
                performance_headings = performance_headstag.find_all('td')
                performance_head = [l.text.strip() for l in performance_headings]

                for performance_heading in performance_head:
                    if len(performance_heading) == 0:
                        continue
                    list_performance_header.append(
                        performance_heading.split('\n')[0].strip() + str([performance_heading.split('\n')[1].strip()]))

                performance_first_row = performance_allkills_headersoup.find_all('tr')[1]
                performance_second_row = performance_allkills_headersoup.find_all('tr')[2]
                performance_third_row = performance_allkills_headersoup.find_all('tr')[3]
                performance_fourth_row = performance_allkills_headersoup.find_all('tr')[4]
                performance_fifth_row = performance_allkills_headersoup.find_all('tr')[5]

                list_performance_index.append(performance_first_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                    [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_second_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(performance_third_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                    [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_fourth_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(performance_fifth_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                    [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))

                list_performance_firstrow = []
                list_performance_secondrow = []
                list_performance_thirdrow = []
                list_performance_fourthrow = []
                list_performance_fifthrow = []
                for map_per_top_table_num in range(int(first_team_score) + int(second_team_score) + 1):
                    if performance_soup.find_all('div', class_='vm-stats-game')[map_per_top_table_num].find('table'):
                        performance_toptable_soup = performance_soup.find_all('div', class_='vm-stats-game')[
                            map_per_top_table_num]
                        performance_allkills_tablesoup = performance_toptable_soup.find('table',
                                                                                        class_='wf-table-inset mod-matrix mod-normal')

                        # 1st row
                        performance_allkills_first_row = performance_allkills_tablesoup.find_all('tr')[1]
                        for firstrownum in performance_allkills_first_row.find_all('td')[1:]:
                            for data in firstrownum:
                                if firstrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                                    list_performance_firstrow.append([0, 0, '-'])
                                    break
                                if len(data.text.strip()) == 0:
                                    continue
                                firstrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                                     data.text.strip().split('\n')[2].strip(),
                                                     data.text.strip().split('\n')[4].strip()))
                                list_performance_firstrow.append(firstrow)

                        # 2nd row
                        performance_allkills_second_row = performance_allkills_tablesoup.find_all('tr')[2]
                        for secondrownum in performance_allkills_second_row.find_all('td')[1:]:
                            for data in secondrownum:
                                if secondrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                                    list_performance_secondrow.append([0, 0, '-'])
                                    break
                                if len(data.text.strip()) == 0:
                                    continue
                                secondrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                                      data.text.strip().split('\n')[2].strip(),
                                                      data.text.strip().split('\n')[4].strip()))
                                list_performance_secondrow.append(secondrow)

                        # 3rd row
                        performance_allkills_third_row = performance_allkills_tablesoup.find_all('tr')[3]
                        for thirdrownum in performance_allkills_third_row.find_all('td')[1:]:
                            for data in thirdrownum:
                                if thirdrownum.find_all('div', class_='stats-sq')[0].text == '\n':
                                    list_performance_thirdrow.append(['-', '-', '-'])
                                    break
                                if thirdrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                                    list_performance_thirdrow.append([0, 0, '-'])
                                    break
                                if len(data.text.strip()) == 0:
                                    continue
                                thirdrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                                     data.text.strip().split('\n')[2].strip(),
                                                     data.text.strip().split('\n')[4].strip()))
                                list_performance_thirdrow.append(thirdrow)

                        # 4th row
                        performance_allkills_fourth_row = performance_allkills_tablesoup.find_all('tr')[4]
                        for fourthrownum in performance_allkills_fourth_row.find_all('td')[1:]:
                            for data in fourthrownum:
                                if fourthrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                                    list_performance_fourthrow.append([0, 0, '-'])
                                    break
                                if len(data.text.strip()) == 0:
                                    continue
                                fourthrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                                      data.text.strip().split('\n')[2].strip(),
                                                      data.text.strip().split('\n')[4].strip()))
                                list_performance_fourthrow.append(fourthrow)

                        # 5th row
                        performance_allkills_fifth_row = performance_allkills_tablesoup.find_all('tr')[5]
                        for fifthrownum in performance_allkills_fifth_row.find_all('td')[1:]:

                            for data in fifthrownum:
                                if fifthrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                                    list_performance_fifthrow.append([0, 0, '-'])
                                    break
                                if len(data.text.strip()) == 0:
                                    continue
                                fifthrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                                     data.text.strip().split('\n')[2].strip(),
                                                     data.text.strip().split('\n')[4].strip()))
                                list_performance_fifthrow.append(fifthrow)

                        performance_allkills_toptable_dataframe = pandas.DataFrame((list_performance_firstrow,
                                                                                    list_performance_secondrow,
                                                                                    list_performance_thirdrow,
                                                                                    list_performance_fourthrow,
                                                                                    list_performance_fifthrow),
                                                                                   index=list_performance_index)

                        try:
                            os.makedirs(f'valorant/{id_match}/performance/{list_performance_name_maps[map_per_top_table_num]}')
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise

                        performance_allkills_toptable_dataframe.to_excel(
                            f'valorant/{id_match}/performance/{list_performance_name_maps[map_per_top_table_num]}/all kills.xlsx',
                            header=list_performance_header)

                        list_performance_firstrow.clear()
                        list_performance_secondrow.clear()
                        list_performance_thirdrow.clear()
                        list_performance_fourthrow.clear()
                        list_performance_fifthrow.clear()

                    elif performance_soup.find_all('div', class_='vm-stats-game')[map_per_top_table_num].find('table') == None:
                        try:
                            os.makedirs(f'valorant/{id_match}/performance/{list_performance_name_maps[map_per_top_table_num]}')
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
            except:
                with open(rf'valorant/{id_match}/match cancelled.txt', 'w') as f:
                    f.write('MATCH CANCELLED!!!')

            # PERFORMANCE TABLES -- "FIRST KILLS" CATRGORY
            list_performance_firstkills_firstrow = []
            list_performance_firstkills_secondrow = []
            list_performance_firstkills_thirdrow = []
            list_performance_firstkills_fourthrow = []
            list_performance_firstkills_fifthrow = []

            for map_per_firstkills_top_table_num in range(int(first_team_score) + int(second_team_score) + 1):
                if performance_soup.find_all('div', class_='vm-stats-game')[map_per_firstkills_top_table_num].find('table'):
                    performance_toptable_soup = performance_soup.find_all('div', class_='vm-stats-game')[
                        map_per_firstkills_top_table_num]
                    performance_firstkills_tablesoup = performance_toptable_soup.find('table',
                                                                                      class_='wf-table-inset mod-matrix mod-fkfd')
                    # 1st row
                    performance_firstkills_first_row = performance_firstkills_tablesoup.find_all('tr')[1]
                    for n in range(0, 15, 3):
                        if performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                            n].text == '\n':
                            list_performance_firstkills_firstrow.append(['-', '-', '-'])
                        performance_firstkills_tab_firstvalue = \
                            performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                                n].text.strip()
                        performance_firstkills_tab_secondvalue = \
                            performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                                n + 1].text.strip()
                        performance_firstkills_tab_thirdvalue = \
                            performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                                n + 2].text.strip()

                        list_performance_firstkills_firstrow.append(
                            [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                             performance_firstkills_tab_thirdvalue])

                    for nested_list in list_performance_firstkills_firstrow:
                        if nested_list[0] == '':
                            list_performance_firstkills_firstrow.remove(nested_list)

                    # 2nd row
                    performance_firstkills_second_row = performance_firstkills_tablesoup.find_all('tr')[2]
                    for n in range(0, 15, 3):
                        if performance_firstkills_second_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_firstkills_secondrow.append(['-', '-', '-'])
                        performance_firstkills_tab_firstvalue = \
                        performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_firstkills_tab_secondvalue = \
                        performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_firstkills_tab_thirdvalue = \
                        performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_firstkills_secondrow.append(
                            [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                             performance_firstkills_tab_thirdvalue])
                    for nested_list in list_performance_firstkills_secondrow:
                        if nested_list[0] == '':
                            list_performance_firstkills_secondrow.remove(nested_list)

                    # 3rd row
                    performance_firstkills_third_row = performance_firstkills_tablesoup.find_all('tr')[3]
                    for n in range(0, 15, 3):
                        if performance_firstkills_third_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_firstkills_thirdrow.append(['-', '-', '-'])
                        performance_firstkills_tab_firstvalue = \
                        performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_firstkills_tab_secondvalue = \
                        performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_firstkills_tab_thirdvalue = \
                        performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_firstkills_thirdrow.append(
                            [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                             performance_firstkills_tab_thirdvalue])

                    for nested_list in list_performance_firstkills_thirdrow:
                        if nested_list[0] == '':
                            list_performance_firstkills_thirdrow.remove(nested_list)

                    # 4th row
                    performance_firstkills_fourth_row = performance_firstkills_tablesoup.find_all('tr')[4]
                    for n in range(0, 15, 3):
                        if performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_firstkills_fourthrow.append(['-', '-', '-'])
                        performance_firstkills_tab_firstvalue = \
                        performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_firstkills_tab_secondvalue = \
                        performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_firstkills_tab_thirdvalue = \
                        performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_firstkills_fourthrow.append(
                            [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                             performance_firstkills_tab_thirdvalue])

                    for nested_list in list_performance_firstkills_fourthrow:
                        if nested_list[0] == '':
                            list_performance_firstkills_fourthrow.remove(nested_list)

                    # 5th row
                    performance_firstkills_fifth_row = performance_firstkills_tablesoup.find_all('tr')[5]
                    for n in range(0, 15, 3):
                        if performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_firstkills_fifthrow.append(['-', '-', '-'])
                        performance_firstkills_tab_firstvalue = \
                        performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_firstkills_tab_secondvalue = \
                        performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_firstkills_tab_thirdvalue = \
                        performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_firstkills_fifthrow.append(
                            [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                             performance_firstkills_tab_thirdvalue])

                    for nested_list in list_performance_firstkills_fifthrow:
                        if nested_list[0] == '':
                            list_performance_firstkills_fifthrow.remove(nested_list)

                    performance_firstkills_toptable_dataframe = pandas.DataFrame((list_performance_firstkills_firstrow,
                                                                                  list_performance_firstkills_secondrow,
                                                                                  list_performance_firstkills_thirdrow,
                                                                                  list_performance_firstkills_fourthrow,
                                                                                  list_performance_firstkills_fifthrow),
                                                                                 index=list_performance_index)

                    performance_firstkills_toptable_dataframe.to_excel(
                        rf'valorant/{id_match}/performance/{list_performance_name_maps[map_per_firstkills_top_table_num]}/first kills.xlsx',
                        header=list_performance_header)

                    list_performance_firstkills_firstrow.clear()
                    list_performance_firstkills_secondrow.clear()
                    list_performance_firstkills_thirdrow.clear()
                    list_performance_firstkills_fourthrow.clear()
                    list_performance_firstkills_fifthrow.clear()

                elif performance_soup.find_all('div', class_='vm-stats-game')[map_per_firstkills_top_table_num].find(
                        'table') == None:
                    continue

            # PERFORMANCE TABLES -- "OP KILLS" CATEGORY
            list_performance_opkills_firstrow = []
            list_performance_opkills_secondrow = []
            list_performance_opkills_thirdrow = []
            list_performance_opkills_fourthrow = []
            list_performance_opkills_fifthrow = []

            for map_per_opkills_top_table_num in range(int(first_team_score) + int(second_team_score) + 1):
                if performance_soup.find_all('div', class_='vm-stats-game')[map_per_opkills_top_table_num].find('table'):
                    performance_toptable_soup = performance_soup.find_all('div', class_='vm-stats-game')[
                        map_per_opkills_top_table_num]
                    performance_opkills_tablesoup = performance_toptable_soup.find('table',
                                                                                   class_='wf-table-inset mod-matrix mod-op')

                    # 1st row
                    performance_opkills_first_row = performance_opkills_tablesoup.find_all('tr')[1]
                    for n in range(0, 15, 3):
                        if performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_opkills_firstrow.append(['-', '-', '-'])
                        performance_opkills_tab_firstvalue = \
                        performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n].text.strip()
                        performance_opkills_tab_secondvalue = \
                        performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n + 1].text.strip()
                        performance_opkills_tab_thirdvalue = \
                        performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n + 2].text.strip()

                        list_performance_opkills_firstrow.append(
                            [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                             performance_opkills_tab_thirdvalue])

                    for nested_list in list_performance_opkills_firstrow:
                        if nested_list[0] == '':
                            list_performance_opkills_firstrow.remove(nested_list)

                    # 2nd row
                    performance_opkills_second_row = performance_opkills_tablesoup.find_all('tr')[2]
                    for n in range(0, 15, 3):
                        if performance_opkills_second_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_opkills_secondrow.append(['-', '-', '-'])
                        performance_opkills_tab_firstvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_opkills_tab_secondvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_opkills_tab_thirdvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_opkills_secondrow.append(
                            [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                             performance_opkills_tab_thirdvalue])
                    for nested_list in list_performance_opkills_secondrow:
                        if nested_list[0] == '':
                            list_performance_opkills_secondrow.remove(nested_list)

                    # 3rd row
                    performance_opkills_third_row = performance_opkills_tablesoup.find_all('tr')[3]
                    for n in range(0, 15, 3):
                        if performance_opkills_third_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_opkills_thirdrow.append(['-', '-', '-'])
                        performance_opkills_tab_firstvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_opkills_tab_secondvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_opkills_tab_thirdvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_opkills_thirdrow.append(
                            [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                             performance_opkills_tab_thirdvalue])

                    for nested_list in list_performance_opkills_thirdrow:
                        if nested_list[0] == '':
                            list_performance_opkills_thirdrow.remove(nested_list)

                    # 4th row
                    performance_opkills_fourth_row = performance_opkills_tablesoup.find_all('tr')[4]
                    for n in range(0, 15, 3):
                        if performance_opkills_fourth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_opkills_fourthrow.append(['-', '-', '-'])
                        performance_opkills_tab_firstvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_opkills_tab_secondvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_opkills_tab_thirdvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_opkills_fourthrow.append(
                            [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                             performance_opkills_tab_thirdvalue])

                    for nested_list in list_performance_opkills_fourthrow:
                        if nested_list[0] == '':
                            list_performance_opkills_fourthrow.remove(nested_list)

                    # 5th row
                    performance_opkills_fifth_row = performance_opkills_tablesoup.find_all('tr')[5]
                    for n in range(0, 15, 3):
                        if performance_opkills_fifth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                            list_performance_opkills_fifthrow.append(['-', '-', '-'])
                        performance_opkills_tab_firstvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                            n].text.strip()
                        performance_opkills_tab_secondvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                        performance_opkills_tab_thirdvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                        list_performance_opkills_fifthrow.append(
                            [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                             performance_opkills_tab_thirdvalue])

                    for nested_list in list_performance_opkills_fifthrow:
                        if nested_list[0] == '':
                            list_performance_opkills_fifthrow.remove(nested_list)

                    performance_opkills_toptable_dataframe = pandas.DataFrame((list_performance_opkills_firstrow,
                                                                               list_performance_opkills_secondrow,
                                                                               list_performance_opkills_thirdrow,
                                                                               list_performance_opkills_fourthrow,
                                                                               list_performance_opkills_fifthrow),
                                                                              index=list_performance_index)

                    performance_opkills_toptable_dataframe.to_excel(
                        rf'valorant/{id_match}/performance/{list_performance_name_maps[map_per_opkills_top_table_num]}/op kills.xlsx',
                        header=list_performance_header)

                    list_performance_opkills_firstrow.clear()
                    list_performance_opkills_secondrow.clear()
                    list_performance_opkills_thirdrow.clear()
                    list_performance_opkills_fourthrow.clear()
                    list_performance_opkills_fifthrow.clear()

                elif performance_soup.find_all('div', class_='vm-stats-game')[map_per_opkills_top_table_num].find(
                        'table') == None:
                    continue

            # PERFORMANCE -- BOTTOM TABLE
            list_performance_bottomtable_index = []
            list_performance_bottomtable_row_data = []
            list_performance_bottomtable_headers = []

            for map_per_bottom_table_num in range(int(first_team_score) + int(second_team_score) + 1):
                if performance_soup.find_all('div', class_='vm-stats-game')[map_per_bottom_table_num].find('table',
                                                                                                           class_='wf-table-inset mod-adv-stats'):
                    performance_bottomtablesoup = performance_soup.find_all('div', class_='vm-stats-game')[
                        map_per_bottom_table_num]
                    performance_bottomtable_soup = performance_bottomtablesoup.find('table',
                                                                                    class_='wf-table-inset mod-adv-stats')

                    for header_data in performance_bottomtable_soup.find_all('th'):
                        for data in header_data:
                            heads = data.text
                            list_performance_bottomtable_headers.append(heads)
                    list_performance_bottomtable_headers.insert(0, 'character name')

                    for num in range(1, 11):
                        performance_bottom_table_row = performance_bottomtable_soup.find_all('tr')[num]
                        performance_bottomtable_char = \
                        performance_bottom_table_row.find_all('td')[1].find('img')['src'].split('/')[-1].split('.')[0]
                        performance_bottomtable_vals = performance_bottom_table_row.find_all('td')[2:]
                        performance_bottomtable_val = [data.text.strip().split('\n')[0].strip() for data in
                                                       performance_bottomtable_vals]
                        performance_bottomtable_val.insert(0, performance_bottomtable_char)

                        performance_bottomtable_player = performance_bottom_table_row.find('td').text.strip().split('\n')[
                                                             0].strip() + str(
                            [performance_bottom_table_row.find('td').text.strip().split('\n')[1].strip()])

                        list_performance_bottomtable_index.append(performance_bottomtable_player)
                        list_performance_bottomtable_row_data.append(performance_bottomtable_val)

                    performance_bottomtable_dataframe = pandas.DataFrame((
                        list_performance_bottomtable_row_data[0],
                        list_performance_bottomtable_row_data[1],
                        list_performance_bottomtable_row_data[2],
                        list_performance_bottomtable_row_data[3],
                        list_performance_bottomtable_row_data[4],
                        list_performance_bottomtable_row_data[5],
                        list_performance_bottomtable_row_data[6],
                        list_performance_bottomtable_row_data[7],
                        list_performance_bottomtable_row_data[8],
                        list_performance_bottomtable_row_data[9]), index=list_performance_bottomtable_index)

                    performance_bottomtable_dataframe.to_excel(
                        rf'valorant/{id_match}/performance/{list_performance_name_maps[map_per_bottom_table_num]}/#bottom table.xlsx',
                        header=list_performance_bottomtable_headers)

                    list_performance_bottomtable_index.clear()
                    list_performance_bottomtable_row_data.clear()
                    list_performance_bottomtable_headers.clear()
                elif performance_soup.find_all('div', class_='vm-stats-game')[map_per_bottom_table_num].find('table',
                                                                                                             class_='wf-table-inset mod-adv-stats') == None:
                    continue



            # ..............................................................................ECONOMY......................................................................



            # CREATE ECONOMY FOLDER
            try:
                os.makedirs(f'valorant/{id_match}/economy')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            valorant_browser.open(link_economy)
            economy_soup = valorant_browser.get_current_page()

            # ECONOMY -- TOP TABLE
            list_name_maps_economy = list_name_of_maps_all_names

            index_for_allmaps_tab = len(list_name_maps_economy) + 1
            list_name_maps_economy.insert(index_for_allmaps_tab, name_of_allmaps_tab)
            list_name_maps_economy.insert(index_for_allmaps_tab, name_of_allmaps_tab)

            list_singlename_maps_economy = list_name_maps_economy[::2]

            try:
                valorant_soup.find('div', class_='vm-stats-gamesnav-item js-map-switch mod-disabled')
                num_of_disabled_map = len(
                    valorant_soup.find_all('div', class_='vm-stats-gamesnav-item js-map-switch mod-disabled'))
                for disabled_map_num in range(num_of_disabled_map):
                    disabled_map_name = \
                    valorant_soup.find_all('div', class_='vm-stats-gamesnav-item js-map-switch mod-disabled')[
                        disabled_map_num].text.strip().split('\n')[-1].strip()
                    list_name_maps_economy.remove(disabled_map_name)
                    list_name_maps_economy.remove(disabled_map_name)
            except:
                pass

            list_economy_toptable_header = []
            economy_toptable_firstrow_vals_list = []
            economy_toptable_secondrow_vals_list = []
            list_economy_toptable_index = []

            for map_economy_top_table_num in range(int(first_team_score) + int(second_team_score) + 2):
                try:
                    if economy_soup.find_all('div', class_='vm-stats-game')[map_economy_top_table_num].find('table',
                                                                                                            class_='wf-table-inset mod-econ'):
                        economy_toptablesoup = economy_soup.find_all('div', class_='vm-stats-game')[map_economy_top_table_num]
                        economy_toptable_soup = economy_toptablesoup.find('table', class_='wf-table-inset mod-econ')

                        for header_data in economy_toptable_soup.find_all('th'):
                            for data in header_data:
                                economy_heads = data.text.strip()
                                list_economy_toptable_header.append(economy_heads)

                        economy_toptable_firstrow = economy_toptable_soup.find_all('tr')[1]

                        economy_toptable_firstrow_vals = economy_toptable_firstrow.find_all('div', class_='stats-sq')
                        economy_toptable_firstrow_val = [l.text.strip() for l in economy_toptable_firstrow_vals]

                        economy_toptable_firstrow_vals_list.append(economy_toptable_firstrow_val[0])
                        for val in economy_toptable_firstrow_val[1:]:
                            economy_toptable_firstrow_vals_list.append(val.split('\t')[0] + val.split('\t')[-1])

                        economy_toptable_secondrow = economy_toptable_soup.find_all('tr')[2]

                        economy_toptable_secondrow_vals = economy_toptable_secondrow.find_all('div', class_='stats-sq')
                        economy_toptable_secondrow_val = [l.text.strip() for l in economy_toptable_secondrow_vals]

                        economy_toptable_secondrow_vals_list.append(economy_toptable_secondrow_val[0])
                        for val in economy_toptable_secondrow_val[1:]:
                            economy_toptable_secondrow_vals_list.append(val.split('\t')[0] + val.split('\t')[-1])

                        list_economy_toptable_index.append(first_team_name)
                        list_economy_toptable_index.append(second_team_name)

                        economy_toptable_dataframe = pandas.DataFrame((
                            economy_toptable_firstrow_vals_list,
                            economy_toptable_secondrow_vals_list), index=list_economy_toptable_index)

                        try:
                            os.makedirs(
                                f'valorant/{id_match}/economy/{list_singlename_maps_economy[map_economy_top_table_num]}')
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise

                        economy_toptable_dataframe.to_excel(
                            f'valorant/{id_match}/economy/{list_singlename_maps_economy[map_economy_top_table_num]}/#economy top table.xlsx')

                        list_economy_toptable_header.clear()
                        economy_toptable_firstrow_vals_list.clear()
                        economy_toptable_secondrow_vals_list.clear()
                        list_economy_toptable_index.clear()
                    elif economy_soup.find_all('div', class_='vm-stats-game')[map_economy_top_table_num].find('table',
                                                                                                              class_='wf-table-inset mod-econ') == None:
                        continue
                except:
                    pass

            # ECONOMY -- BOTTOM TABLE
            list_economy_bottomtable_both_headers = []
            list_economy_bottomtable_both_data = []
            list_economy_bottomtable_index = []

            list_economy_bottomtable_index.append(first_team_name)
            list_economy_bottomtable_index.append(second_team_name)
            list_economy_bottomtable_index.append(' ')

            for map_economy_bottom_table_num in range(int(first_team_score) + int(second_team_score) + 1):
                try:
                    economy_soup.find_all('div', class_='vm-stats-game')[map_economy_bottom_table_num].find_all('table',
                                                                                                                class_='wf-table-inset mod-econ')[
                        1]
                    economy_toptablesoup = economy_soup.find_all('div', class_='vm-stats-game')[map_economy_bottom_table_num]
                    economy_bottomtable_soup = economy_toptablesoup.find_all('table', class_='wf-table-inset mod-econ')[1]

                    length_of_table = len(economy_bottomtable_soup.find_all('td'))

                    for economy_header_num in range(1, length_of_table):

                        if economy_header_num == 13:
                            continue
                        elif economy_header_num == 26:
                            continue
                        elif economy_header_num == 39:
                            continue

                        for header_num in range(2):
                            economy_bottomtable_header = \
                            economy_bottomtable_soup.find_all('td')[economy_header_num].find_all('div', class_='bank')[
                                header_num].text.strip()
                            list_economy_bottomtable_both_headers.append(economy_bottomtable_header)

                    list_economy_bottomtable_top_headers = list_economy_bottomtable_both_headers[::2]
                    list_economy_bottomtable_bottom_headers = list_economy_bottomtable_both_headers[1::2]

                    for economy_bottomtable_data_num in range(1, length_of_table):

                        if economy_bottomtable_data_num == 13:
                            continue
                        elif economy_bottomtable_data_num == 26:
                            continue
                        elif economy_bottomtable_data_num == 39:
                            continue

                        for data_num in range(2):
                            economy_bottomtable_data = \
                            economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                           class_='rnd-sq')[
                                data_num].text.strip()
                            if 'mod-t' in economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                                         class_='rnd-sq')[
                                data_num]['class']:
                                list_economy_bottomtable_both_data.append(economy_bottomtable_data + '[red]')
                            elif 'mod-ct' in \
                                    economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                                   class_='rnd-sq')[
                                        data_num]['class']:
                                list_economy_bottomtable_both_data.append(economy_bottomtable_data + '[green]')
                            else:
                                list_economy_bottomtable_both_data.append(economy_bottomtable_data)

                    list_economy_bottomtable_top_data = list_economy_bottomtable_both_data[::2]
                    list_economy_bottomtable_bottom_data = list_economy_bottomtable_both_data[1::2]

                    economy_bottomtable_dataframe = pandas.DataFrame((
                        list_economy_bottomtable_top_data,
                        list_economy_bottomtable_bottom_data,
                        list_economy_bottomtable_bottom_headers), index=list_economy_bottomtable_index)

                    economy_bottomtable_dataframe.to_excel(
                        f'valorant/{id_match}/economy/{list_singlename_maps_economy[map_economy_bottom_table_num]}/economy bottom table.xlsx',
                        header=list_economy_bottomtable_top_headers)

                    list_economy_bottomtable_both_headers.clear()
                    list_economy_bottomtable_both_data.clear()
                except:
                    continue

        except:
            try:
                os.makedirs(f'valorant/{id_match}/overview')
            except OSError as e:
                continue

            # OVERVIEW MAP HEAD DATA
            list_map_head_team_names = []
            list_map_head_team_scores = []
            list_map_head_team_slash_scores = []
            list_map_head_map_name = []
            list_map_head_match_duration = []

            soup_table_head = valorant_soup.find('div', class_='vm-stats-game-header')

            name_team1_table_head = soup_table_head.find_all('div', class_='team-name')[0].text.strip()
            list_map_head_team_names.append(name_team1_table_head)

            team1_score_table_head = soup_table_head.find_all('div', class_='score')[0].text.strip()
            list_map_head_team_scores.append(team1_score_table_head)

            team1_slash_score = soup_table_head.find('div', class_='team').find_all('span')

            slash_score1 = [l.text for l in team1_slash_score]

            if team1_slash_score[0]['class'] == ['mod-ct']:
                if team1_slash_score[1]['class'] == ['mod-t']:
                    if len(slash_score1) == 2:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[green]' + '/' + slash_score1[1] + '[red]')
                    elif len(slash_score1) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[green]' + '/' + slash_score1[1] + '[red]' + '/' + slash_score1[2])
                else:
                    if len(slash_score1) == 2:
                        list_map_head_team_slash_scores.append(slash_score1[0] + '[green]' + '/' + slash_score1[1])
                    elif len(slash_score1) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[green]' + '/' + slash_score1[1] + '/' + slash_score1[2] + '[red]')
            elif team1_slash_score[0]['class'] == ['mod-t']:
                if team1_slash_score[1]['class'] == ['mod-ct']:
                    if len(slash_score1) == 2:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[red]' + '/' + slash_score1[1] + '[green]')
                    elif len(slash_score1) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[red]' + '/' + slash_score1[1] + '[green]' + '/' + slash_score1[2])
                else:
                    if len(slash_score1) == 2:
                        list_map_head_team_slash_scores.append(slash_score1[0] + '[red]' + '/' + slash_score1[1])
                    elif len(slash_score1) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score1[0] + '[red]' + '/' + slash_score1[1] + '/' + slash_score1[2] + '[green]')
            else:
                if len(slash_score1) == 2:
                    list_map_head_team_slash_scores.append(slash_score1[0] + '/' + slash_score1[1])
                elif len(slash_score1) == 3:
                    list_map_head_team_slash_scores.append(slash_score1[0] + '/' + slash_score1[1] + '/' + slash_score1[2])

            name_team2_table_head = soup_table_head.find_all('div', class_='team-name')[1].text.strip()
            list_map_head_team_names.append(name_team2_table_head)

            team2_score_table_head = soup_table_head.find_all('div', class_='score')[1].text.strip()
            list_map_head_team_scores.append(team2_score_table_head)

            team2_slash_score = soup_table_head.find('div', class_='team mod-right').find_all('span')

            slash_score2 = [l.text for l in team2_slash_score]

            if team2_slash_score[0]['class'] == ['mod-ct']:
                if team2_slash_score[1]['class'] == ['mod-t']:
                    if len(slash_score2) == 2:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[green]' + '/' + slash_score2[1] + '[red]')
                    elif len(slash_score2) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[green]' + '/' + slash_score2[1] + '[red]' + '/' + slash_score2[2])
                else:
                    if len(slash_score2) == 2:
                        list_map_head_team_slash_scores.append(slash_score2[0] + '[green]' + '/' + slash_score2[1])
                    elif len(slash_score2) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[green]' + '/' + slash_score2[1] + '/' + slash_score2[2] + '[red]')
            elif team2_slash_score[0]['class'] == ['mod-t']:
                if team2_slash_score[1]['class'] == ['mod-ct']:
                    if len(slash_score2) == 2:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[red]' + '/' + slash_score2[1] + '[green]')
                    elif len(slash_score2) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[red]' + '/' + slash_score2[1] + '[green]' + '/' + slash_score2[2])
                else:
                    if len(slash_score2) == 2:
                        list_map_head_team_slash_scores.append(slash_score2[0] + '[red]' + '/' + slash_score2[1])
                    elif len(slash_score2) == 3:
                        list_map_head_team_slash_scores.append(
                            slash_score2[0] + '[red]' + '/' + slash_score2[1] + '/' + slash_score2[2] + '[green]')
            else:
                if len(slash_score2) == 2:
                    list_map_head_team_slash_scores.append(slash_score2[0] + '/' + slash_score2[1])
                elif len(slash_score2) == 3:
                    list_map_head_team_slash_scores.append(slash_score2[0] + '/' + slash_score2[1] + '/' + slash_score2[2])

            map_name_table_head = soup_table_head.find('div', class_='map').text.strip().split('\n')[0].strip()
            list_map_head_map_name.append(map_name_table_head)
            list_map_head_map_name.append(map_name_table_head)

            match_duration_table_head = soup_table_head.find('div', class_='map').text.strip().split('\n')[-1].strip()
            list_map_head_match_duration.append(match_duration_table_head)
            list_map_head_match_duration.append(match_duration_table_head)

            map_head_data_dct = {
                'Map Name': list_map_head_map_name,
                'Match Duration': list_map_head_match_duration,
                'Team Name': list_map_head_team_names,
                'Score': list_map_head_team_scores,
                'Slash Score': list_map_head_team_slash_scores
            }

            map_head_dataframe = pandas.DataFrame(map_head_data_dct)

            try:
                os.makedirs(f'valorant/{id_match}/overview/#table head data')
            except OSError as e:
                continue
            map_head_dataframe.to_excel(f'valorant/{id_match}/overview/#table head data/table head data.xlsx', index=False)

            list_map_head_map_name.clear()
            list_map_head_match_duration.clear()
            list_map_head_team_names.clear()
            list_map_head_team_scores.clear()
            list_map_head_team_slash_scores.clear()

            # OVERVIEW TABLES -- "ALL" CATEGORY
            data = []
            l_name = []
            l_team = []
            l_char_name_1 = []
            l_char_name_2 = []
            l_char_name_3 = []
            l_char_name_4 = []
            l_char_name_5 = []
            l_acs = []
            l_k = []
            l_d = []
            l_a = []
            l_p_or_m = []
            l_kast = []
            l_adr = []
            l_hs = []
            l_fk = []
            l_fd = []
            l_p_or_m1 = []

            try:
                tables = valorant_soup.find('table', class_='wf-table-inset mod-overview')
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 0:
                            char_name_1 = '-'
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        elif len(char_name) == 5:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[0]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[0]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[0]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[0]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[0]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[0]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split('\n')[0]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[0]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')
                        try:
                            fk = data[d_num][10].split('\n')[0]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[0]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[0]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')
            except:
                continue

            try:
                tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[1]
                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 0:
                            char_name_1 = '-'
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'

                        elif len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        elif len(char_name) == 5:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[0]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[0]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[0]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[0]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[0]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[0]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split('\n')[0]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[0]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')
                        try:
                            fk = data[d_num][10].split('\n')[0]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[0]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[0]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')
            except:
                continue

            data_overview_all = {
                'Name': l_name,
                'Team': l_team,
                'Character 1': l_char_name_1,
                'Character 2': l_char_name_2,
                'Character 3': l_char_name_3,
                'Character 4': l_char_name_4,
                'Character 5': l_char_name_5,
                'ACS': l_acs,
                'K': l_k,
                'D': l_d,
                'A': l_a,
                '+/-': l_p_or_m,
                'KAST': l_kast,
                'ADR': l_adr,
                'HS%': l_hs,
                'FK': l_fk,
                'FD': l_fd,
                "'+/-'": l_p_or_m1
            }

            df = pandas.DataFrame(data_overview_all)
            df.drop_duplicates(inplace=True)

            try:
                os.makedirs(f'valorant/{id_match}/overview/{map_name_table_head}')
            except OSError as e:
                continue

            df.to_excel(rf'valorant/{id_match}/overview/{map_name_table_head}/all.xlsx', index=False)

            l_name.clear()
            l_team.clear()
            l_char_name_1.clear()
            l_char_name_2.clear()
            l_char_name_3.clear()
            l_char_name_4.clear()
            l_char_name_5.clear()
            l_acs.clear()
            l_k.clear()
            l_d.clear()
            l_a.clear()
            l_p_or_m.clear()
            l_kast.clear()
            l_adr.clear()
            l_hs.clear()
            l_fk.clear()
            l_fd.clear()
            l_p_or_m1.clear()

            #  OVERVIEW TABLES -- "ATTACK" CATEGORY
            try:
                tables = valorant_soup.find('table', class_='wf-table-inset mod-overview')
                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                l_name = []
                l_team = []
                l_char_name_1 = []
                l_char_name_2 = []
                l_char_name_3 = []
                l_char_name_4 = []
                l_char_name_5 = []
                l_acs = []
                l_k = []
                l_d = []
                l_a = []
                l_p_or_m = []
                l_kast = []
                l_adr = []
                l_hs = []
                l_fk = []
                l_fd = []
                l_p_or_m1 = []

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        else:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[1]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[1]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[1]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[1]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[1]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[1]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split()[1]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[1]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')

                        try:
                            fk = data[d_num][10].split('\n')[1]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[1]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[1]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[1]
                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        else:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[1]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[1]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[1]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[1]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[1]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[1]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split()[1]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[1]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')

                        try:
                            fk = data[d_num][10].split('\n')[1]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[1]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')

                        try:
                            p_or_m1 = data[d_num][12].split('\n')[1]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                data_overview_all_maps_all = {
                    'Name': l_name,
                    'Team': l_team,
                    'Character 1': l_char_name_1,
                    'Character 2': l_char_name_2,
                    'Character 3': l_char_name_3,
                    'Character 4': l_char_name_4,
                    'Character 5': l_char_name_5,
                    'ACS': l_acs,
                    'K': l_k,
                    'D': l_d,
                    'A': l_a,
                    '+/-': l_p_or_m,
                    'KAST': l_kast,
                    'ADR': l_adr,
                    'HS%': l_hs,
                    'FK': l_fk,
                    'FD': l_fd,
                    "'+//-'": l_p_or_m1
                }

                df = pandas.DataFrame(data_overview_all_maps_all)
                df.drop_duplicates(inplace=True)
                df.to_excel(rf'valorant/{id_match}/overview/{map_name_table_head}/attack.xlsx', index=False)

                l_name.clear()
                l_team.clear()
                l_char_name_1.clear()
                l_char_name_2.clear()
                l_char_name_3.clear()
                l_char_name_4.clear()
                l_char_name_5.clear()
                l_acs.clear()
                l_k.clear()
                l_d.clear()
                l_a.clear()
                l_p_or_m.clear()
                l_kast.clear()
                l_adr.clear()
                l_hs.clear()
                l_fk.clear()
                l_fd.clear()
                l_p_or_m1.clear()
            except:
                continue

            # OVERVIEW TABLES -- "DEFEND" CATEGORY
            try:
                tables = valorant_soup.find('table', class_='wf-table-inset mod-overview')

                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                l_name = []
                l_team = []
                l_char_name_1 = []
                l_char_name_2 = []
                l_char_name_3 = []
                l_char_name_4 = []
                l_char_name_5 = []
                l_acs = []
                l_k = []
                l_d = []
                l_a = []
                l_p_or_m = []
                l_kast = []
                l_adr = []
                l_hs = []
                l_fk = []
                l_fd = []
                l_p_or_m1 = []

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        else:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[2]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[2]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[2]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[2]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[2]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_ - p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[2]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split()[2]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[2]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')

                        try:
                            fk = data[d_num][10].split('\n')[2]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[2]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')
                        try:
                            p_or_m1 = data[d_num][12].split('\n')[2]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                tables = valorant_soup.find_all('table', class_='wf-table-inset mod-overview')[+1]

                data = []
                for content in tables.find_all('tr'):
                    row_data = content.find_all('td')
                    row = [l.text.strip() for l in row_data]
                    data.append(row)

                for d_num in range(1, 6):
                    for table_num in range(3):
                        player_name = data[d_num][0].split('\n')[0].strip()
                        l_name.append(player_name)

                        player_team = data[d_num][0].split('\n')[-1].strip()
                        l_team.append(player_team)

                        char_names = tables.find_all('td', class_='mod-agents')[d_num - 1].find_all('img')
                        char_name = [l['alt'] for l in char_names]

                        if len(char_name) == 1:
                            char_name_1 = char_name[0]
                            char_name_2 = '-'
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 2:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = '-'
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 3:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = '-'
                            char_name_5 = '-'
                        elif len(char_name) == 4:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = '-'
                        else:
                            char_name_1 = char_name[0]
                            char_name_2 = char_name[1]
                            char_name_3 = char_name[2]
                            char_name_4 = char_name[3]
                            char_name_5 = char_name[4]

                        l_char_name_1.append(char_name_1)
                        l_char_name_2.append(char_name_2)
                        l_char_name_3.append(char_name_3)
                        l_char_name_4.append(char_name_4)
                        l_char_name_5.append(char_name_5)

                        try:
                            acs = data[d_num][2].split('\n')[2]
                            l_acs.append(acs)
                        except:
                            l_acs.append('-')

                        try:
                            k = data[d_num][3].split('\n')[2]
                            l_k.append(k)
                        except:
                            l_k.append('-')

                        try:
                            d = data[d_num][4].replace('/', '').strip().split('\n')[2]
                            l_d.append(d)
                        except:
                            l_d.append('-')

                        try:
                            a = data[d_num][5].split('\n')[2]
                            l_a.append(a)
                        except:
                            l_a.append('-')

                        try:
                            p_or_m = data[d_num][6].split('\n')[2]
                            l_p_or_m.append(p_or_m)
                        except:
                            l_ - p_or_m.append('-')

                        try:
                            kast = data[d_num][7].split('\n')[2]
                            l_kast.append(kast)
                        except:
                            l_kast.append('-')

                        try:
                            adr = data[d_num][8].split()[2]
                            l_adr.append(adr)
                        except:
                            l_adr.append('-')

                        try:
                            hs = data[d_num][9].split('\n')[2]
                            l_hs.append(hs)
                        except:
                            l_hs.append('-')

                        try:
                            fk = data[d_num][10].split('\n')[2]
                            l_fk.append(fk)
                        except:
                            l_fk.append('-')

                        try:
                            fd = data[d_num][11].split('\n')[2]
                            l_fd.append(fd)
                        except:
                            l_fd.append('-')
                        try:
                            p_or_m1 = data[d_num][12].split('\n')[2]
                            l_p_or_m1.append(p_or_m1)
                        except:
                            l_p_or_m1.append('-')

                data_overview_all_maps_all = {
                    'Name': l_name,
                    'Team': l_team,
                    'Character 1': l_char_name_1,
                    'Character 2': l_char_name_2,
                    'Character 3': l_char_name_3,
                    'Character 4': l_char_name_4,
                    'Character 5': l_char_name_5,
                    'ACS': l_acs,
                    'K': l_k,
                    'D': l_d,
                    'A': l_a,
                    '+/-': l_p_or_m,
                    'KAST': l_kast,
                    'ADR': l_adr,
                    'HS%': l_hs,
                    'FK': l_fk,
                    'FD': l_fd,
                    "'+//-'": l_p_or_m1
                }

                df = pandas.DataFrame(data_overview_all_maps_all)
                df.drop_duplicates(inplace=True)
                df.to_excel(rf'valorant/{id_match}/overview/{map_name_table_head}/defend.xlsx', index=False)

                l_name.clear()
                l_team.clear()
                l_char_name_1.clear()
                l_char_name_2.clear()
                l_char_name_3.clear()
                l_char_name_4.clear()
                l_char_name_5.clear()
                l_acs.clear()
                l_k.clear()
                l_d.clear()
                l_a.clear()
                l_p_or_m.clear()
                l_kast.clear()
                l_adr.clear()
                l_hs.clear()
                l_fk.clear()
                l_fd.clear()
                l_p_or_m1.clear()
            except:
                continue

            # MAP HEAD TABLES
            try:
                os.makedirs(f'valorant/{id_match}/overview/#map head tables')
            except OSError as e:
                continue

            list_data_mapheadtable_team1 = []
            list_data_mapheadtable_team2 = []

            for map_head_table_num in range(int(first_team_score) + int(second_team_score)):
                soup_map_head_table = valorant_soup.find_all('div', class_='vlr-rounds')[map_head_table_num]
                map_head_table_total_num_of_col = int(
                    soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[-1].find('div',
                                                                                              class_='rnd-num').text.strip())

                try:
                    for map_head_col_num in range(1, map_head_table_total_num_of_col + 4):
                        map_head_table_col = soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[
                            map_head_col_num]
                        if soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[map_head_col_num]['class'] == [
                            'vlr-rounds-row-col', 'mod-spacing']:
                            continue
                        elif \
                        soup_map_head_table.find_all('div', class_='vlr-rounds-row-col')[map_head_col_num].find_all('div')[
                            1]['class'] == ['team']:
                            continue
                        elif map_head_table_col.find('div', class_='rnd-num').find_next_sibling()['class'] == ['rnd-sq']:
                            list_data_mapheadtable_team1.append('-')
                            action_string = \
                            map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find_next_sibling().find(
                                'img')['src']
                            action_name = action_string.split('/')[-1].split('.')[0]
                            if map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find_next_sibling()[
                                'class'][2] == 'mod-ct':
                                list_data_mapheadtable_team2.append(action_name + '[green]')
                            else:
                                list_data_mapheadtable_team2.append(action_name + '[red]')
                        else:
                            action_string = \
                            map_head_table_col.find('div', class_='rnd-num').find_next_sibling().find('img')['src']
                            action_name = action_string.split('/')[-1].split('.')[0]
                            if map_head_table_col.find('div', class_='rnd-num').find_next_sibling()['class'][2] == 'mod-ct':
                                list_data_mapheadtable_team1.append(action_name + '[green]')
                            else:
                                list_data_mapheadtable_team1.append(action_name + '[red]')
                            list_data_mapheadtable_team2.append('-')
                except Exception as e:
                    pass

                try:
                    map_head_tables_dataframe = pandas.DataFrame({
                        f'{first_team_name}': list_data_mapheadtable_team1,
                        f'{second_team_name}': list_data_mapheadtable_team2
                    })
                except:
                    map_head_tables_dataframe = pandas.DataFrame({
                        f'{first_team_name}': list_data_mapheadtable_team1[:len(list_data_mapheadtable_team1) - 1],
                        f'{second_team_name}': list_data_mapheadtable_team2
                    })
                map_head_tables_dataframe.to_excel(
                    f'valorant/{id_match}/overview/#map head tables/{map_name_table_head}.xlsx', index=False)

                list_data_mapheadtable_team1.clear()
                list_data_mapheadtable_team2.clear()

            # ............................................................................PERFORMANCE..................................................................



            # CREATE PERFORMANCE FOLDER
            try:
                os.makedirs(f'valorant/{id_match}/performance')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            valorant_browser.open(link_performance)
            performance_soup = valorant_browser.get_current_page()

            # PERFORMANCE TABLES -- "ALL KILLS" CATEGORY
            list_performance_header = []
            list_performance_index = []

            try:
                performance_allkills_headersoup = \
                performance_soup.find_all('table', class_='wf-table-inset mod-matrix mod-normal')[0]

                performance_headstag = performance_allkills_headersoup.find('tr')
                performance_headings = performance_headstag.find_all('td')
                performance_head = [l.text.strip() for l in performance_headings]

                for performance_heading in performance_head:
                    if len(performance_heading) == 0:
                        continue
                    list_performance_header.append(
                        performance_heading.split('\n')[0].strip() + str([performance_heading.split('\n')[1].strip()]))

                performance_first_row = performance_allkills_headersoup.find_all('tr')[1]
                performance_second_row = performance_allkills_headersoup.find_all('tr')[2]
                performance_third_row = performance_allkills_headersoup.find_all('tr')[3]
                performance_fourth_row = performance_allkills_headersoup.find_all('tr')[4]
                performance_fifth_row = performance_allkills_headersoup.find_all('tr')[5]

                list_performance_index.append(
                    performance_first_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_second_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_third_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_fourth_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
                list_performance_index.append(
                    performance_fifth_row.find_all('td')[0].text.strip().split('\n')[0].strip() + str(
                        [performance_first_row.find_all('td')[0].text.strip().split('\n')[1].strip()]))
            except:
                with open(rf'valorant/{id_match}/match cancelled.txt', 'w') as f:
                    f.write('MATCH CANCELLED!!!')

            list_performance_firstrow = []
            list_performance_secondrow = []
            list_performance_thirdrow = []
            list_performance_fourthrow = []
            list_performance_fifthrow = []
            if performance_soup.find('div', class_='vm-stats-game').find('table'):
                performance_toptable_soup = performance_soup.find('div', class_='vm-stats-game')
                performance_allkills_tablesoup = performance_toptable_soup.find('table',
                                                                                class_='wf-table-inset mod-matrix mod-normal')

                # 1st row
                performance_allkills_first_row = performance_allkills_tablesoup.find_all('tr')[1]
                for firstrownum in performance_allkills_first_row.find_all('td')[1:]:
                    for data in firstrownum:
                        if firstrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                            list_performance_firstrow.append([0, 0, '-'])
                            break
                        if len(data.text.strip()) == 0:
                            continue
                        firstrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                             data.text.strip().split('\n')[2].strip(),
                                             data.text.strip().split('\n')[4].strip()))
                        list_performance_firstrow.append(firstrow)

                # 2nd row
                performance_allkills_second_row = performance_allkills_tablesoup.find_all('tr')[2]
                for secondrownum in performance_allkills_second_row.find_all('td')[1:]:
                    for data in secondrownum:
                        if secondrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                            list_performance_secondrow.append([0, 0, '-'])
                            break
                        if len(data.text.strip()) == 0:
                            continue
                        secondrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                              data.text.strip().split('\n')[2].strip(),
                                              data.text.strip().split('\n')[4].strip()))
                        list_performance_secondrow.append(secondrow)

                # 3rd row
                performance_allkills_third_row = performance_allkills_tablesoup.find_all('tr')[3]
                for thirdrownum in performance_allkills_third_row.find_all('td')[1:]:
                    for data in thirdrownum:
                        if thirdrownum.find_all('div', class_='stats-sq')[0].text == '\n':
                            list_performance_thirdrow.append(['-', '-', '-'])
                            break
                        if thirdrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                            list_performance_thirdrow.append([0, 0, '-'])
                            break
                        if len(data.text.strip()) == 0:
                            continue
                        thirdrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                             data.text.strip().split('\n')[2].strip(),
                                             data.text.strip().split('\n')[4].strip()))
                        list_performance_thirdrow.append(thirdrow)

                # 4th row
                performance_allkills_fourth_row = performance_allkills_tablesoup.find_all('tr')[4]
                for fourthrownum in performance_allkills_fourth_row.find_all('td')[1:]:
                    for data in fourthrownum:
                        if fourthrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                            list_performance_fourthrow.append([0, 0, '-'])
                            break
                        if len(data.text.strip()) == 0:
                            continue
                        fourthrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                              data.text.strip().split('\n')[2].strip(),
                                              data.text.strip().split('\n')[4].strip()))
                        list_performance_fourthrow.append(fourthrow)

                # 5th row
                performance_allkills_fifth_row = performance_allkills_tablesoup.find_all('tr')[5]
                for fifthrownum in performance_allkills_fifth_row.find_all('td')[1:]:

                    for data in fifthrownum:
                        if fifthrownum.find_all('div', class_='stats-sq')[2].text == '\n':
                            list_performance_fifthrow.append([0, 0, '-'])
                            break
                        if len(data.text.strip()) == 0:
                            continue
                        fifthrow = ','.join((data.text.strip().split('\n')[0].strip(),
                                             data.text.strip().split('\n')[2].strip(),
                                             data.text.strip().split('\n')[4].strip()))
                        list_performance_fifthrow.append(fifthrow)

                performance_allkills_toptable_dataframe = pandas.DataFrame((list_performance_firstrow,
                                                                            list_performance_secondrow,
                                                                            list_performance_thirdrow,
                                                                            list_performance_fourthrow,
                                                                            list_performance_fifthrow),
                                                                           index=list_performance_index)

                try:
                    os.makedirs(f'valorant/{id_match}/performance/{map_name_table_head}')
                except OSError as e:
                    continue

                performance_allkills_toptable_dataframe.to_excel(
                    f'valorant/{id_match}/performance/{map_name_table_head}/all kills.xlsx', header=list_performance_header)

                list_performance_firstrow.clear()
                list_performance_secondrow.clear()
                list_performance_thirdrow.clear()
                list_performance_fourthrow.clear()
                list_performance_fifthrow.clear()

            elif performance_soup.find('div', class_='vm-stats-game').find('table') == None:
                try:
                    os.makedirs(f'valorant/{id_match}/performance/{map_name_table_head}')
                except OSError as e:
                    continue

            # PERFORMANCE TABLES -- "FIRST KILLS" CATEGORY
            list_performance_firstkills_firstrow = []
            list_performance_firstkills_secondrow = []
            list_performance_firstkills_thirdrow = []
            list_performance_firstkills_fourthrow = []
            list_performance_firstkills_fifthrow = []

            if performance_soup.find('div', class_='vm-stats-game').find('table'):
                performance_toptable_soup = performance_soup.find('div', class_='vm-stats-game')
                performance_firstkills_tablesoup = performance_toptable_soup.find('table',
                                                                                  class_='wf-table-inset mod-matrix mod-fkfd')
                # 1st row
                performance_firstkills_first_row = performance_firstkills_tablesoup.find_all('tr')[1]
                for n in range(0, 15, 3):
                    if performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                        n].text == '\n':
                        list_performance_firstkills_firstrow.append(['-', '-', '-'])
                    performance_firstkills_tab_firstvalue = \
                        performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                            n].text.strip()
                    performance_firstkills_tab_secondvalue = \
                        performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                            n + 1].text.strip()
                    performance_firstkills_tab_thirdvalue = \
                        performance_firstkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[
                            n + 2].text.strip()

                    list_performance_firstkills_firstrow.append(
                        [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                         performance_firstkills_tab_thirdvalue])

                for nested_list in list_performance_firstkills_firstrow:
                    if nested_list[0] == '':
                        list_performance_firstkills_firstrow.remove(nested_list)

                # 2nd row
                performance_firstkills_second_row = performance_firstkills_tablesoup.find_all('tr')[2]
                for n in range(0, 15, 3):
                    if performance_firstkills_second_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_firstkills_secondrow.append(['-', '-', '-'])
                    performance_firstkills_tab_firstvalue = \
                    performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_firstkills_tab_secondvalue = \
                    performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_firstkills_tab_thirdvalue = \
                    performance_firstkills_second_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_firstkills_secondrow.append(
                        [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                         performance_firstkills_tab_thirdvalue])
                for nested_list in list_performance_firstkills_secondrow:
                    if nested_list[0] == '':
                        list_performance_firstkills_secondrow.remove(nested_list)

                # 3rd row
                performance_firstkills_third_row = performance_firstkills_tablesoup.find_all('tr')[3]
                for n in range(0, 15, 3):
                    if performance_firstkills_third_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_firstkills_thirdrow.append(['-', '-', '-'])
                    performance_firstkills_tab_firstvalue = \
                    performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_firstkills_tab_secondvalue = \
                    performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_firstkills_tab_thirdvalue = \
                    performance_firstkills_third_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_firstkills_thirdrow.append(
                        [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                         performance_firstkills_tab_thirdvalue])

                for nested_list in list_performance_firstkills_thirdrow:
                    if nested_list[0] == '':
                        list_performance_firstkills_thirdrow.remove(nested_list)

                # 4th row
                performance_firstkills_fourth_row = performance_firstkills_tablesoup.find_all('tr')[4]
                for n in range(0, 15, 3):
                    if performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_firstkills_fourthrow.append(['-', '-', '-'])
                    performance_firstkills_tab_firstvalue = \
                    performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_firstkills_tab_secondvalue = \
                    performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_firstkills_tab_thirdvalue = \
                    performance_firstkills_fourth_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_firstkills_fourthrow.append(
                        [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                         performance_firstkills_tab_thirdvalue])

                for nested_list in list_performance_firstkills_fourthrow:
                    if nested_list[0] == '':
                        list_performance_firstkills_fourthrow.remove(nested_list)

                # 5th row
                performance_firstkills_fifth_row = performance_firstkills_tablesoup.find_all('tr')[5]
                for n in range(0, 15, 3):
                    if performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_firstkills_fifthrow.append(['-', '-', '-'])
                    performance_firstkills_tab_firstvalue = \
                    performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_firstkills_tab_secondvalue = \
                    performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_firstkills_tab_thirdvalue = \
                    performance_firstkills_fifth_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_firstkills_fifthrow.append(
                        [performance_firstkills_tab_firstvalue, performance_firstkills_tab_secondvalue,
                         performance_firstkills_tab_thirdvalue])

                for nested_list in list_performance_firstkills_fifthrow:
                    if nested_list[0] == '':
                        list_performance_firstkills_fifthrow.remove(nested_list)

                performance_firstkills_toptable_dataframe = pandas.DataFrame((list_performance_firstkills_firstrow,
                                                                              list_performance_firstkills_secondrow,
                                                                              list_performance_firstkills_thirdrow,
                                                                              list_performance_firstkills_fourthrow,
                                                                              list_performance_firstkills_fifthrow),
                                                                             index=list_performance_index)

                performance_firstkills_toptable_dataframe.to_excel(
                    rf'valorant/{id_match}/performance/{map_name_table_head}/first kills.xlsx',
                    header=list_performance_header)

                list_performance_firstkills_firstrow.clear()
                list_performance_firstkills_secondrow.clear()
                list_performance_firstkills_thirdrow.clear()
                list_performance_firstkills_fourthrow.clear()
                list_performance_firstkills_fifthrow.clear()

            elif performance_soup.find('div', class_='vm-stats-game').find('table') == None:
                continue

            # PERFORMANCE TABLES -- "OP KILLS" CATEGORY
            list_performance_opkills_firstrow = []
            list_performance_opkills_secondrow = []
            list_performance_opkills_thirdrow = []
            list_performance_opkills_fourthrow = []
            list_performance_opkills_fifthrow = []

            if performance_soup.find('div', class_='vm-stats-game').find('table'):
                performance_toptable_soup = performance_soup.find('div', class_='vm-stats-game')
                performance_opkills_tablesoup = performance_toptable_soup.find('table',
                                                                               class_='wf-table-inset mod-matrix mod-op')

                # 1st row
                performance_opkills_first_row = performance_opkills_tablesoup.find_all('tr')[1]
                for n in range(0, 15, 3):
                    if performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_opkills_firstrow.append(['-', '-', '-'])
                    performance_opkills_tab_firstvalue = \
                    performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n].text.strip()
                    performance_opkills_tab_secondvalue = \
                    performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n + 1].text.strip()
                    performance_opkills_tab_thirdvalue = \
                    performance_opkills_tablesoup.find_all('tr')[1].find_all('div', class_='stats-sq')[n + 2].text.strip()

                    list_performance_opkills_firstrow.append(
                        [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                         performance_opkills_tab_thirdvalue])

                for nested_list in list_performance_opkills_firstrow:
                    if nested_list[0] == '':
                        list_performance_opkills_firstrow.remove(nested_list)

                # 2nd row
                performance_opkills_second_row = performance_opkills_tablesoup.find_all('tr')[2]
                for n in range(0, 15, 3):
                    if performance_opkills_second_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_opkills_secondrow.append(['-', '-', '-'])
                    performance_opkills_tab_firstvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_opkills_tab_secondvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_opkills_tab_thirdvalue = performance_opkills_second_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_opkills_secondrow.append(
                        [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                         performance_opkills_tab_thirdvalue])
                for nested_list in list_performance_opkills_secondrow:
                    if nested_list[0] == '':
                        list_performance_opkills_secondrow.remove(nested_list)

                # 3rd row
                performance_opkills_third_row = performance_opkills_tablesoup.find_all('tr')[3]
                for n in range(0, 15, 3):
                    if performance_opkills_third_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_opkills_thirdrow.append(['-', '-', '-'])
                    performance_opkills_tab_firstvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_opkills_tab_secondvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_opkills_tab_thirdvalue = performance_opkills_third_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_opkills_thirdrow.append(
                        [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                         performance_opkills_tab_thirdvalue])

                for nested_list in list_performance_opkills_thirdrow:
                    if nested_list[0] == '':
                        list_performance_opkills_thirdrow.remove(nested_list)

                # 4th row
                performance_opkills_fourth_row = performance_opkills_tablesoup.find_all('tr')[4]
                for n in range(0, 15, 3):
                    if performance_opkills_fourth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_opkills_fourthrow.append(['-', '-', '-'])
                    performance_opkills_tab_firstvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_opkills_tab_secondvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_opkills_tab_thirdvalue = performance_opkills_fourth_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_opkills_fourthrow.append(
                        [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                         performance_opkills_tab_thirdvalue])

                for nested_list in list_performance_opkills_fourthrow:
                    if nested_list[0] == '':
                        list_performance_opkills_fourthrow.remove(nested_list)

                # 5th row
                performance_opkills_fifth_row = performance_opkills_tablesoup.find_all('tr')[5]
                for n in range(0, 15, 3):
                    if performance_opkills_fifth_row.find_all('div', class_='stats-sq')[n].text == '\n':
                        list_performance_opkills_fifthrow.append(['-', '-', '-'])
                    performance_opkills_tab_firstvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                        n].text.strip()
                    performance_opkills_tab_secondvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                        n + 1].text.strip()
                    performance_opkills_tab_thirdvalue = performance_opkills_fifth_row.find_all('div', class_='stats-sq')[
                        n + 2].text.strip()

                    list_performance_opkills_fifthrow.append(
                        [performance_opkills_tab_firstvalue, performance_opkills_tab_secondvalue,
                         performance_opkills_tab_thirdvalue])

                for nested_list in list_performance_opkills_fifthrow:
                    if nested_list[0] == '':
                        list_performance_opkills_fifthrow.remove(nested_list)

                performance_opkills_toptable_dataframe = pandas.DataFrame((list_performance_opkills_firstrow,
                                                                           list_performance_opkills_secondrow,
                                                                           list_performance_opkills_thirdrow,
                                                                           list_performance_opkills_fourthrow,
                                                                           list_performance_opkills_fifthrow),
                                                                          index=list_performance_index)

                performance_opkills_toptable_dataframe.to_excel(
                    rf'valorant/{id_match}/performance/{map_name_table_head}/op kills.xlsx', header=list_performance_header)

                list_performance_opkills_firstrow.clear()
                list_performance_opkills_secondrow.clear()
                list_performance_opkills_thirdrow.clear()
                list_performance_opkills_fourthrow.clear()
                list_performance_opkills_fifthrow.clear()

            elif performance_soup.find('div', class_='vm-stats-game').find('table') == None:
                continue

            # PERFORMANCE -- BOTTOM TABLES
            list_performance_bottomtable_index = []
            list_performance_bottomtable_row_data = []
            list_performance_bottomtable_headers = []

            if performance_soup.find('div', class_='vm-stats-game').find('table', class_='wf-table-inset mod-adv-stats'):
                performance_bottomtablesoup = performance_soup.find('div', class_='vm-stats-game')
                performance_bottomtable_soup = performance_bottomtablesoup.find('table',
                                                                                class_='wf-table-inset mod-adv-stats')

                for header_data in performance_bottomtable_soup.find_all('th'):
                    for data in header_data:
                        heads = data.text
                        list_performance_bottomtable_headers.append(heads)
                list_performance_bottomtable_headers.insert(0, 'character name')

                for num in range(1, 11):
                    performance_bottom_table_row = performance_bottomtable_soup.find_all('tr')[num]
                    performance_bottomtable_char = \
                    performance_bottom_table_row.find_all('td')[1].find('img')['src'].split('/')[-1].split('.')[0]
                    performance_bottomtable_vals = performance_bottom_table_row.find_all('td')[2:]
                    performance_bottomtable_val = [data.text.strip().split('\n')[0].strip() for data in
                                                   performance_bottomtable_vals]
                    performance_bottomtable_val.insert(0, performance_bottomtable_char)

                    performance_bottomtable_player = performance_bottom_table_row.find('td').text.strip().split('\n')[
                                                         0].strip() + str(
                        [performance_bottom_table_row.find('td').text.strip().split('\n')[1].strip()])

                    list_performance_bottomtable_index.append(performance_bottomtable_player)
                    list_performance_bottomtable_row_data.append(performance_bottomtable_val)

                performance_bottomtable_dataframe = pandas.DataFrame((
                    list_performance_bottomtable_row_data[0],
                    list_performance_bottomtable_row_data[1],
                    list_performance_bottomtable_row_data[2],
                    list_performance_bottomtable_row_data[3],
                    list_performance_bottomtable_row_data[4],
                    list_performance_bottomtable_row_data[5],
                    list_performance_bottomtable_row_data[6],
                    list_performance_bottomtable_row_data[7],
                    list_performance_bottomtable_row_data[8],
                    list_performance_bottomtable_row_data[9]), index=list_performance_bottomtable_index)

                performance_bottomtable_dataframe.to_excel(
                    rf'valorant/{id_match}/performance/{map_name_table_head}/#bottom table.xlsx',
                    header=list_performance_bottomtable_headers)

                list_performance_bottomtable_index.clear()
                list_performance_bottomtable_row_data.clear()
                list_performance_bottomtable_headers.clear()
            elif performance_soup.find('div', class_='vm-stats-game').find('table',
                                                                           class_='wf-table-inset mod-adv-stats') == None:
                continue



            # ................................................................................ECONOMY....................................................................



            # CRREATE ECONOMY FOLDER
            try:
                os.makedirs(f'valorant/{id_match}/economy')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            valorant_browser.open(link_economy)
            economy_soup = valorant_browser.get_current_page()

            # ECONOMY -- TOP TABLE
            list_economy_toptable_header = []
            economy_toptable_firstrow_vals_list = []
            economy_toptable_secondrow_vals_list = []
            list_economy_toptable_index = []

            if economy_soup.find('div', class_='vm-stats-game').find('table', class_='wf-table-inset mod-econ'):
                economy_toptablesoup = economy_soup.find('div', class_='vm-stats-game')
                economy_toptable_soup = economy_toptablesoup.find('table', class_='wf-table-inset mod-econ')

                for header_data in economy_toptable_soup.find_all('th'):
                    for data in header_data:
                        economy_heads = data.text.strip()
                        list_economy_toptable_header.append(economy_heads)

                economy_toptable_firstrow = economy_toptable_soup.find_all('tr')[1]

                economy_toptable_firstrow_vals = economy_toptable_firstrow.find_all('div', class_='stats-sq')
                economy_toptable_firstrow_val = [l.text.strip() for l in economy_toptable_firstrow_vals]

                economy_toptable_firstrow_vals_list.append(economy_toptable_firstrow_val[0])
                for val in economy_toptable_firstrow_val[1:]:
                    economy_toptable_firstrow_vals_list.append(val.split('\t')[0] + val.split('\t')[-1])

                economy_toptable_secondrow = economy_toptable_soup.find_all('tr')[2]

                economy_toptable_secondrow_vals = economy_toptable_secondrow.find_all('div', class_='stats-sq')
                economy_toptable_secondrow_val = [l.text.strip() for l in economy_toptable_secondrow_vals]

                economy_toptable_secondrow_vals_list.append(economy_toptable_secondrow_val[0])
                for val in economy_toptable_secondrow_val[1:]:
                    economy_toptable_secondrow_vals_list.append(val.split('\t')[0] + val.split('\t')[-1])

                list_economy_toptable_index.append(first_team_name)
                list_economy_toptable_index.append(second_team_name)

                economy_toptable_dataframe = pandas.DataFrame((
                    economy_toptable_firstrow_vals_list,
                    economy_toptable_secondrow_vals_list), index=list_economy_toptable_index)

                try:
                    os.makedirs(f'valorant/{id_match}/economy/{map_name_table_head}')
                except OSError as e:
                    continue

                economy_toptable_dataframe.to_excel(
                    f'valorant/{id_match}/economy/{map_name_table_head}/#economy top table.xlsx')

                list_economy_toptable_header.clear()
                economy_toptable_firstrow_vals_list.clear()
                economy_toptable_secondrow_vals_list.clear()
                list_economy_toptable_index.clear()
            elif economy_soup.find('div', class_='vm-stats-game').find('table', class_='wf-table-inset mod-econ') == None:
                try:
                    os.makedirs(f'valorant/{id_match}/economy/{map_name_table_head}')
                except OSError as e:
                    continue
            # ECONOMY -- BOTTOM TABLE
            list_economy_bottomtable_both_headers = []
            list_economy_bottomtable_both_data = []
            list_economy_bottomtable_index = []

            list_economy_bottomtable_index.append(first_team_name)
            list_economy_bottomtable_index.append(second_team_name)
            list_economy_bottomtable_index.append(' ')
            try:
                economy_soup.find('div', class_='vm-stats-game').find_all('table', class_='wf-table-inset mod-econ')[1]
                economy_toptablesoup = economy_soup.find('div', class_='vm-stats-game')
                economy_bottomtable_soup = economy_toptablesoup.find_all('table', class_='wf-table-inset mod-econ')[1]

                length_of_table = len(economy_bottomtable_soup.find_all('td'))

                for economy_header_num in range(1, length_of_table):

                    if economy_header_num == 13:
                        continue
                    elif economy_header_num == 26:
                        continue
                    elif economy_header_num == 39:
                        continue

                    for header_num in range(2):
                        economy_bottomtable_header = \
                        economy_bottomtable_soup.find_all('td')[economy_header_num].find_all('div', class_='bank')[
                            header_num].text.strip()
                        list_economy_bottomtable_both_headers.append(economy_bottomtable_header)

                list_economy_bottomtable_top_headers = list_economy_bottomtable_both_headers[::2]
                list_economy_bottomtable_bottom_headers = list_economy_bottomtable_both_headers[1::2]

                for economy_bottomtable_data_num in range(1, length_of_table):

                    if economy_bottomtable_data_num == 13:
                        continue
                    elif economy_bottomtable_data_num == 26:
                        continue
                    elif economy_bottomtable_data_num == 39:
                        continue

                    for data_num in range(2):
                        economy_bottomtable_data = \
                        economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                       class_='rnd-sq')[
                            data_num].text.strip()
                        if 'mod-t' in economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                                     class_='rnd-sq')[
                            data_num]['class']:
                            list_economy_bottomtable_both_data.append(economy_bottomtable_data + '[red]')
                        elif 'mod-ct' in \
                                economy_bottomtable_soup.find_all('td')[economy_bottomtable_data_num].find_all('div',
                                                                                                               class_='rnd-sq')[
                                    data_num]['class']:
                            list_economy_bottomtable_both_data.append(economy_bottomtable_data + '[green]')
                        else:
                            list_economy_bottomtable_both_data.append(economy_bottomtable_data)

                list_economy_bottomtable_top_data = list_economy_bottomtable_both_data[::2]
                list_economy_bottomtable_bottom_data = list_economy_bottomtable_both_data[1::2]

                economy_bottomtable_dataframe = pandas.DataFrame((
                    list_economy_bottomtable_top_data,
                    list_economy_bottomtable_bottom_data,
                    list_economy_bottomtable_bottom_headers), index=list_economy_bottomtable_index)

                economy_bottomtable_dataframe.to_excel(
                    f'valorant/{id_match}/economy/{list_singlename_maps_economy[map_economy_bottom_table_num]}/economy bottom table.xlsx',
                    header=list_economy_bottomtable_top_headers)

                list_economy_bottomtable_both_headers.clear()
                list_economy_bottomtable_both_data.clear()
            except:
                continue
    except:
        with open('match cancelled.txt', 'w') as f:
            f.write('MATCH CANCELLED!!!')
