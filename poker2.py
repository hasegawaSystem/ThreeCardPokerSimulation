import random
import csv

#csvに書き出す関数です。
def csvoutput(x):
    with open('kane4.csv', 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([x])

#カードを生成する関数です。
def cardset():
    
    card = []
    
    #プレイヤー3枚ディーラー3枚の合わせて6枚を生成します。
    while(len(card)<6):
        #カードを生成してカード列に追加します。
        card.append([random.randrange(2,15), random.randrange(1,5)])
        
        twincheck = True
        check = 0
        while(check+1 < len(card)):
            if card[check] == card[-1] and card[check] == card[-1]:
                twincheck = False
                card.pop()
                card.append([random.randrange(3,15), random.randrange(1,4)])
            else:
                check +=1
    
    #プレイヤーとディーラーのカードを大きい順にソートします
    if card[0][0] < card[1][0]:
        card[0], card[1] =  card[1], card[0]
            
    if card[0][0] < card[2][0]:
        card[0], card[2] =  card[2], card[0]
        
    if card[1][0] < card[2][0]:
        card[1], card[2] =  card[2], card[1]
            
    if card[3][0] < card[4][0]:
        card[3], card[4] =  card[4], card[3]
            
    if card[3][0] < card[5][0]:
        card[3], card[5] =  card[5], card[3]
        
    if card[4][0] < card[5][0]:
        card[4], card[5] =  card[5], card[4]
        
    return card[0], card[1], card[2], card[3], card[4], card[5]       

#手配の強さを確定させる関数です。
def pointset():

    p1, p2, p3, d1, d2, d3 = cardset()

    #手配の強さを示す変数です。
    # 5 >= ストレートフラッシュ
    # 4 >= スリーカード
    # 3 >= ストレート
    # 2 >= フラッシュ
    # 1 >= ペア
    # 0 >= ハイカード
    p_card = 0
    d_card = 0
    
    #配列の中を参照するための変数です。
    # n == カードの数字
    # s == カードのスートカテゴリ
    n = 0
    s = 1
    
    #プレイヤー側
    #スリーカード？
    if(p1[n] == p2[n] == p3[n]):
        p_card += 4
    
    #ストレート？
    if(p1[n] == p2[n]+1 == p3[n]+2 or (p1[n]==14 and p2[n]==3 and p3[n]==2)):
        p_card += 3
    
    #フラッシュ？(スリーカードではなく？)
    if((p1[s] == p2[s] == p3[s]) and (p_card != 4)):
        p_card += 2
        
    #ペア？(フラッシュでもスリーカードでもなく？)
    if(p_card != 2 and p_card != 4):
        if(p1[n] == p2[n]):
            p_card += 1
            
        if(p1[n] == p3[n]):
            p_card += 1
            p2, p3 = p3, p2
            
        if(p2[n] == p3[n]):
            p_card += 1
            p1, p3 = p3, p1
            
    #ディーラー側
    #スリーカード？
    if(d1[n] == d2[n] == d3[n]):
        d_card += 4
    
    #ストレート？
    if(d1[n] == d2[n]+1 == d3[n]+2 or (d1[n]==14 and d2[n]==3 and d3[n]==2)):
        d_card += 3
    
    #フラッシュ？(スリーカードではなく？)
    if((d1[s] == d2[s] == d3[s]) and (d_card != 4)):
        d_card += 2
        
    #ペア？(フラッシュでもスリーカードでもなく？)
    if(d_card != 2 and d_card != 4):
        if(d1[n] == d2[n]):
            d_card += 1
            
        if(d1[n] == d3[n]):
            d_card += 1
            d2, d3 = d3, d2
            
        if(d2[n] == d3[n]):
            d_card += 1
            d1, d3 = d3, d1


    #カードの強さを計算します
    p_card += (p1[n]/14 + p2[n]/140 + p3[n]/1400)* 9/10
    d_card += (d1[n]/14 + d2[n]/140 + d3[n]/1400)* 9/10
    
    return p_card, d_card

#Q65戦法でレイズかフォールドかを判断する関数です。returnが0ならフォールド、1ならレイズです。
def Q65(p_card):
    
    #プレイヤーはQ65以下だったら降ります。
    #定数はQ65のときの強さを示す数字
    if(p_card < 0.813):
        return 0
    else:
        return 1
    
#ディーラーはハンドがQ以上じゃなければ降ります。returnが0ならディーラーノットクオリファイ、1ならプレイです。
def delerplay(d_card):
    
    #定数はQ32のときの強さを示す数字
    if(d_card < 0.792):
        return 0
    else:
        return 1

#実際に強さを比較する関数です。returnは(配当金)です。
def battle(p_card, d_card, bet):
    
    #どっちも降りてなかったら勝負させます
    #ディーラーが勝ってたら返却なし
    if(d_card > p_card):
        return 0
    
    #もしあいこでしたらお金を返却します
    elif(d_card == p_card):
        return bet
    
    #プレイヤーが勝ってたら、手に応じて配当金を出します
    else:
        #ストレートフラッシュで勝ってたら配当は5倍です
        if p_card > 5:
            return bet*5
        
        #スリーカードで勝ってたら配当は4倍です。
        if p_card > 4:
            return bet*4
        
        #ハイカード、ペア、ストレート、フラッシュで勝ってたら配当は2倍です。
        else:
            return bet*2

#マーチンゲール法で賭け金を決める関数です。連勝数が0かマイナスの時にbet額を返して、それ以外は0を返します
def martingale(vic, minbet):
    
    if vic<0:
        bet = minbet
        for _ in range(-vic-1):
            bet *= 2
            
        return bet
    
    elif vic==0:
        return minbet
    
    else:
        return 0

#連勝法で賭け金を決める関数です。連勝数が1以上の時にmaxbetを返して、それ以外は0を返します。正直関数化しなくても良かったけど、今後のため
def winstreek(vic, maxbet):
    
    if(vic>=1):
        return maxbet
    
    else:
        return 0

#3連勝する確立が9%であることから、3回まで賭ける連勝法です。
def Threewinstreek(vic, maxbet):
    
    if(vic >=1 and vic < 4):
        return maxbet
    
    else:
        return 0

#勝った時のvicを決める関数です。今まで負けてたら連勝数を1にして、勝ってたら+1にしたものを返します。
def winvic(vic):
    if(vic<1):
        return 1
    
    elif(vic>0):
        return vic+1
    
#負けた時のvicを決める関数です。今まで負けてたら連勝数を-1加算して、勝ってたら-1にしたものを返します。
def losevic(vic):
    if(vic>0):
        return -1
    
    elif(vic<1):
        return vic-1

#実際に実行する関数です。引数は左から初期金、プレイ回数、minbet額、maxbet額です。
def main(importmoney, kazu, minbet, maxbet):
    money = importmoney
    vic = 0
    
    for _ in range(kazu):
        p_card, d_card = pointset()
        
        #マーチンゲール法と連勝法を組み合わせます
        #連勝法：勝ったら次の賭けを最大に。負けたら最小に
        #マーチンゲール法：負けたら次の賭けを倍に
        bet = martingale(vic, minbet) #+ Threewinstreek(vic, maxbet)
        #bet = winstreek(vic, maxbet)
        
        #もしmaxbetを超えてしまうなら、maxbetと同額に調整します
        if bet > maxbet:
            bet = maxbet
        
        #もしminbetを下回ってしまうなら、minbetと同額に調整します
        if bet < minbet:
            bet = minbet
            
        #決めたベット額を所持金から引きます
        money -= bet
        
        #プレイヤーはQ65法で、レイズかフォールドか選択します
        #Q65以下ならフォールド
        if(Q65(p_card)==0): 
            vic = losevic(vic)
            kekka = -1
            
        #Q65以上ならレイズ
        elif(Q65(p_card)==1):
            money -= bet
            bet *= 2
        
        #ディーラーはQ32以下でプレイヤーが勝負に乗ってたらディーラーノットクオリファイです。
        if(delerplay(d_card)==0 and Q65(p_card)==1):
            #配当はアンティベット*2+レイズ額。レイズ分はそのまま返却です。
            
            money += bet/2 * 3
            vic = winvic(vic)
            kekka = 1
        
        #プレイヤーもディーラーも勝負に乗ってたらどちらが強いか比較して、配当金分を加算します。
        if(delerplay(d_card)==1 and Q65(p_card)==1):
            deltamoney = battle(p_card, d_card, bet)
            money += deltamoney
            
            #配当金が0なら負けてたってコト！？
            if(deltamoney == 0):
                vic = losevic(vic)
                kekka = -2
                
            #配当金と合計bet額が同じならあいこってコト！？
            elif(deltamoney == bet):
                vic = 0
                kekka = 0
            
            #それ以外なら勝ちってコト！？    
            else:
                vic = winvic(vic)
                kekka = 2
        
        #所持金と連勝数を表示するだけ       
        #print(int(money), kekka, vic)
        
    #全体での結果を出力します。初期所持金より多かったら1,少なかったら0を出力します
    #if money > importmoney:
        #return 1
    
    #else:
        #return 0
        csvoutput(money)

print("start")
main(100000, 1000, 10, 5000)
    

#ここから本編



#for x in range(5):
    #リセットしてカウントってのを何回やるのか決めます。(何日分？)
    #vic = 0
    #lose = 0
    #for _ in range(1):
        
        #一日に何回プレイする？みたいな認識
        #if(main(100000, 1000, 10, 5000)):vic += 1
        #else:   lose += 1

    #全体を通して勝った回数と負けた回数を表示します。
    #output = vic, lose
    #csvoutput(vic, lose)
    #print("step" + str(x+1))
