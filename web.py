from flask import Flask, render_template, redirect, request, jsonify
import requests, json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def get_first(players):
    first = {
        "VOTE_CN": 0,
    }
    result_i = 0
    for i, player in enumerate(players):
        if int(str(player['VOTE_CN']).replace(",", "")) > int(str(first['VOTE_CN']).replace(",", "")):
            first = player
            result_i = i
    return first, result_i

def team_to_color(team):
    team_colors = {
        "두산": "#1A1748",   # 네이비
        "롯데": "#041E42",   # 다크 블루
        "LG": "#C30452",     # 레드
        "키움": "#570514",   # 딥 와인
        "KIA": "#EA0029",    # 레드
        "삼성": "#074CA1",   # 블루
        "한화": "#FC4E00",   # 오렌지
        "SSG": "#CE0E2D",    # 레드
        "NC": "#315288",     # 마린 블루
        "KT": "#000000",     # 블랙
    }
    return team_colors.get(team, "#FFFFFF")  # 기본값: 흰색

def vote_to_int(vote):
    return int(str(vote).replace(",", ""))

def pic_to_url(pic):
    return f"https:{pic}"

def code_to_pos(code):
    pos_dict = {
        "C": "포수",
        "1B": "1루수",
        "2B": "2루수",
        "3B": "3루수",
        "SS": "유격수",
        "OF": "외야수",
        "DH": "지명타자",
        "SP": "선발투수",
        "MP": "구원투수",
        "CP": "마무리투수",
    }
    return pos_dict.get(code, code)  # 기본값: 코드 그대로 반환

@app.route('/')
def home():
    try:
        pos = request.args.get('pos')
        dr_nm = request.args.get('dr_nm')
        if not pos:
            return redirect('/?pos=C&dr_nm=dr')
        if not dr_nm:
            return redirect('/?pos=C&dr_nm=dr')
        url = "https://allstar.koreabaseball.com/ws/Allstar.asmx/GetKboAll"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "pos": pos
        }
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        # ✅ 유니코드 이스케이프 없이 바로 JSON 파싱
        json_data = response.json()
        
        # 예시: 총 득표수 계산
        all_EA = sum(int(E['VOTE_CN'].replace(',', '')) for E in json_data['arrEA'])
        all_WE = sum(int(W['VOTE_CN'].replace(',', '')) for W in json_data['arrWE'])
        
        EA_players = json_data['arrEA']
        WE_players = json_data['arrWE']
        
        return_EA = []
        return_WE = []
        
        for i in range(2):
            EA_ = get_first(EA_players)
            del EA_players[EA_[1]]
            WE_ = get_first(WE_players)
            del WE_players[WE_[1]]
            return_EA.append(EA_[0])
            return_WE.append(WE_[0])
        
        print(f"드림팀 올스타: {return_EA[0]['P_NM']} ({return_EA[0]['VOTE_CN']}) / {return_EA[1]['P_NM']} ({return_EA[1]['VOTE_CN']})")
        print(f"나눔팀 올스타: {return_WE[0]['P_NM']} ({return_WE[0]['VOTE_CN']}) / {return_WE[1]['P_NM']} ({return_WE[1]['VOTE_CN']})")
        
        print(f"총 득표수 (드림팀): {all_EA}, 총 득표수 (나눔팀): {all_WE}")
        
        if dr_nm == "dr":
            team = [return_EA[0]['T_NM'], return_EA[1]['T_NM']]
            player = [return_EA[0]['P_NM'], return_EA[1]['P_NM']]
            vote = [vote_to_int(return_EA[0]['VOTE_CN']), vote_to_int(return_EA[1]['VOTE_CN'])]
            total = all_EA
            percent = [round(vote_to_int(return_EA[0]['VOTE_CN']) / all_EA * 100, 2), round(vote_to_int(return_EA[1]['VOTE_CN']) / all_EA * 100, 2)]
            color = [team_to_color(return_EA[0]['T_NM']), team_to_color(return_EA[1]['T_NM'])]
            picture = [pic_to_url(return_EA[0]['P_IMG_LK']), pic_to_url(return_EA[1]['P_IMG_LK'])]
        else:
            team = [return_WE[0]['T_NM'], return_WE[1]['T_NM']]
            player = [return_WE[0]['P_NM'], return_WE[1]['P_NM']]
            vote = [vote_to_int(return_WE[0]['VOTE_CN']), vote_to_int(return_WE[1]['VOTE_CN'])]
            total = all_WE
            percent = [round(vote_to_int(return_WE[0]['VOTE_CN']) / all_WE * 100, 2), round(vote_to_int(return_WE[1]['VOTE_CN']) / all_WE * 100, 2)]
            color = [team_to_color(return_WE[0]['T_NM']), team_to_color(return_WE[1]['T_NM'])]
            picture = [pic_to_url(return_WE[0]['P_IMG_LK']), pic_to_url(return_WE[1]['P_IMG_LK'])]
            
        pos_dict = {
            "C": "포수",
            "1B": "1루수",
            "2B": "2루수",
            "3B": "3루수",
            "SS": "유격수",
            "OF": "외야수",
            "DH": "지명타자",
            "SP": "선발투수",
            "MP": "구원투수",
            "CP": "마무리투수",
        }
        
        pos_text = code_to_pos(pos)
        team_text = "드림팀" if dr_nm == "dr" else "나눔팀"
        return render_template('index.html', pos=pos, dr_nm=dr_nm, 
                            team=team, player=player, vote=vote, 
                            total_vote=total, percent=percent, 
                            color=color, picture=picture, pos_text=pos_text, 
                            team_text=team_text, pos_dict=pos_dict)
    except Exception as e:
        print(f"Error: {e}")
        return render_template("err.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)