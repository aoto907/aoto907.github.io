import random
import itertools
import numpy as np

class Person:
       
    def __init__(self, status = "Negative", color = "b"):  # 状態、Negative：非感染者、Positive：感染者
        self.status = status  # Negative, Positive, Death, Recover
        self.color = color    # Blue(b), red(r), black(k), green(g)
        self.T_recover = 0  # 感染から回復までの時間
        self.serious_illnes = 0     # 重症率：年齢が高いほ度に死亡率が他変わる割合
        self.infection_rate = 0     # 感染率：「濃厚接触者であるほどに感染率が上昇する」かつ「若年層であるほど上昇する」
        self.death_rate = 0         # 死亡率：年齢と潜伏期間と共に高くなる
        self.x = random.randint(0, n-1)  # x座標
        self.y = random.randint(0, n-1)  # y座標
        self.old = np.random.choice(["Young", "Middle", "Old"], p=[0.35, 0.35, 0.3])  # 感染年齢：「高齢者」「中年者」「若年者」
        
    def update_xy(self):  # 次のステップの
        Speed_person = random.randint(1, 3)
        self.x += random.randint(-Speed_person, Speed_person)
        self.y += random.randint(-Speed_person, Speed_person)
    
    def stop_xy(self):  # statusが、「Death」または「Positive」の場合
        self.x += 0
        self.y += 0
        
    def check_infection(self, Posi_or_Nega):  # 感染確認、周囲の情報を確認し自己の状態を変化
        i = self.x
        j = self.y
        R_infection = random.randint(1, 3)
        
        # ムーア近傍 : 感染者を中心とした周りのデータ
        moor = [[[suki(k, n), suki(l, n)] 
                 for k in range(i - R_infection, i + R_infection + 1)] for l in range(j - R_infection, j + R_infection+1)]
            
        moor = list(itertools.chain.from_iterable(moor))  # ３次元リストを２次元リストに変換する
            
        # 感染者のリスト：感染者・非感染者分からないものの位置
        Posi_or_Nega_list = [suki(Posi_or_Nega.x, n), suki(Posi_or_Nega.y, n)]
        
        # 非感染者は感染する
        if Posi_or_Nega_list in moor:
            distance = int(max(abs(i-Posi_or_Nega.x), abs(j-Posi_or_Nega.y))) % 3
            inf_rate = [1.0, 2.0, 2.5]
            if Posi_or_Nega.old == "Young":                
                Posi_or_Nega.serious_illnes = 0.001                 # 重症率：0.0
                Posi_or_Nega.infection_rate = inf_rate[distance] * 0.38     # 感染率：
                Posi_or_Nega.death_rate     = 0.005                  # 死亡率：0.05
            elif Posi_or_Nega.old == "Middle":
                Posi_or_Nega.serious_illnes = 0.03                  # 重症率：0.2
                Posi_or_Nega.infection_rate = inf_rate[distance] * 0.29      # 感染率：
                Posi_or_Nega.death_rate     = 0.048                  # 死亡率：
            else: # Posi_or_Nega.old == "Old":
                Posi_or_Nega.serious_illnes = 0.08                  # 重症率：0.8
                Posi_or_Nega.infection_rate = inf_rate[distance] * 0.18     # 感染率：
                Posi_or_Nega.death_rate     = 0.843                  # 死亡率：
            status = np.random.choice(["Positive", "Negative"], p=[Posi_or_Nega.infection_rate, (1-Posi_or_Nega.infection_rate)])
            if status == "Positive":
                Posi_or_Nega.status = "Positive"
                Posi_or_Nega.color  = "r"
            else:
                Posi_or_Nega.status = "Negative"
                Posi_or_Nega.color  = "b"
            
    def check_recover(self, recover): 
        life_or_death = np.random.choice([0, 1, 2], p=[1-(recover.death_rate+recover.serious_illnes), recover.death_rate, recover.serious_illnes])  # 回復率
        if life_or_death == 0:
            recover.status = "Recover"  # 生き返り
            recover.color = "g"
            recover.T_recover = 0
        elif life_or_death == 1:
            recover.status = "Death"  # 死亡
            recover.color = "k"  
            recover.T_recover = 0
        else:
            recover.status = "Positive"  # 継続感染
            recover.color = "r"
            recover.T_recover = random.randint(1, 10)
                         
def suki(k, n):  # 周期境界の関数
    if k < 0:
        return n + k
    elif k == 0:
        return 0
    elif k > n:
        return k - n
    else:
        return k