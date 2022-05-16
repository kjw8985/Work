import shutil
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import requests 
import os
import xml.etree.ElementTree as ET 
from bs4 import BeautifulSoup
import PublicDataReader as pdr
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow import keras
import math
import folium
from pandas import DataFrame
from folium.plugins import MarkerCluster


def foliumMap(month, size):
    print('주택 거래 내역 가져오는 중')
    test = pd.read_csv('media/csv_file/as_{}.csv'.format(month), encoding='CP949',skiprows=15)
    tst=test.loc[:,['시군구', '전용면적(㎡)', '단지명','거래금액(만원)','계약년월']].replace(',','',regex=True).astype({'거래금액(만원)':float})
    tst['평수'] = tst['전용면적(㎡)']/3.3
    tst['평단가'] = tst['거래금액(만원)']/tst['평수']
    tstt = tst.loc[:,['시군구','평수','단지명','평단가','계약년월']]
    #print(tstt)
    df = DataFrame()

    sigungu_arr = tstt.loc[:,'시군구'].unique() 
    df['시군구'] = sigungu_arr
    
    pyeng = size+'평대' ### input값

    pyengsu = {'10평대':'평수 >= 10 and 평수 < 15', '15평대':'평수 >= 15 and 평수 < 20','20평대':'평수 >= 20 and 평수 < 25',
            '25평대':'평수 >= 25 and 평수 < 30','30평대':'평수 >= 30 and 평수 < 35','35평대':'평수 >= 35 and 평수 < 40','40평대':'평수 >= 40 and 평수 < 45'}

    
    
    price_lst = []
    for i in range(len(sigungu_arr)):
        price_lst.append(tstt.query('시군구 == "{}"'.format(df.loc[i,'시군구'])).query(pyengsu[pyeng]).loc[:,'평단가'].mean())
        
    price_arr = np.array(price_lst)
    df['평단가'] = price_arr
    
    print('법정동 정보 가져오는 중')
    #position = pd.read_excel('D:/kerina/git_final_pro/final_project/media/csv_file/pos.xlsx')
    #position.to_csv('D:/kerina/git_final_pro/final_project/media/csv_file/position.csv')
    pos = pd.read_csv('media/csv_file/position.csv', encoding='utf-8')
    poss = pos.loc[:,['시도','시군구','읍면동','하위','위도','경도']]
    poss = poss.fillna('')
    #else:
    poss['시군구'] = poss['시도']+ ' '+poss['시군구'] +' '+poss['읍면동']+ ' '+poss['하위']

    poss['평단가'] = np.nan
    poss = poss.loc[:, ['시군구', '위도','경도','평단가']]
    
    #print(poss)
    print('지도와 평단가를 매칭하는 중')
    position = []
    for i in range(df.count()[0]):
        position.append(poss.loc[poss['시군구'].str.contains(df.loc[i,'시군구'], case=False, na=False)].loc[:,['위도','경도']][-1:].values)
    
    print('비어있는 위치정보 삭제')
    df['위도','경도'] = position
    index_num = []
    for i in range(df.count()[0]):
        index_ = poss.loc[poss['시군구'].str.contains(df.loc[i,'시군구'][:-1], case=False, na=False)].index
        index_num.append(index_)
    
    naindex= []
    for i in range(df.count()[0]):
        if len(index_num[i][:]) ==0:
            print(i)
            naindex.append(i)
    df = df.drop(naindex, axis = 0)
    df_real = df.dropna()
    

    print('지도를 작성하는 중')
    print(df_real.count()[0])
    #print(df_real['위도','경도'][1170:1180])
    
    m = folium.Map(location = [37.500335, 127.037596],zoom_start=14,width='100%',height='100%')
    marker_cluster = MarkerCluster().add_to(m)   
    for i in range(df_real.count()[0]-1):
        try:
            folium.Marker(df_real['위도','경도'][i:i+1].tolist()[0].tolist()[0],
                        tooltip = '<pre>{}<br>평당가 : {}만원</pre>'.format(df_real['시군구'][i:i+1].tolist()[0] , round(df_real['평단가'][i:i+1].tolist()[0]))).add_to(marker_cluster)    
        except:
            print(i)   
    return m



def model(locate, size):
    print('데이터 모음 가져오는 중')
    df = DataFrame()
    df = pd.read_csv('media/csv_file/as_2203.csv',encoding='CP949',skiprows=15)
    df = pd.concat((df,pd.read_csv('media/csv_file/as_2202.csv', encoding='CP949',skiprows=15)))
    df = pd.concat((df,pd.read_csv('media/csv_file/as_2201.csv', encoding='CP949',skiprows=15)))
    df = pd.concat((df,pd.read_csv('media/csv_file/as_2204.csv', encoding='CP949',skiprows=15)))

    for i in range(6,22):
        for j in range(1,13):
            i_z = str(i).zfill(2)
            j_z = str(j).zfill(2)
            df = pd.concat((df,pd.read_csv('media/csv_file/as_{0}{1}.csv'.format(i_z,j_z),encoding='CP949',skiprows=15, low_memory=False)))
        print('20{}'.format(str(i).zfill(2)))
        
    print('데이터 프레임 생성 중')
    tst=df.loc[:,['시군구', '전용면적(㎡)', '단지명','거래금액(만원)','계약년월','건축년도']].replace(',','',regex=True).astype({'거래금액(만원)':float})
    tst['평수'] = tst['전용면적(㎡)']/3.3
    tst['평단가'] = tst['거래금액(만원)']/tst['평수']
    tst['준공기간'] = (tst['계약년월']/100) - tst['건축년도']
    final_tst = tst.loc[:,['시군구','평수','단지명','평단가','계약년월','준공기간']]


    print('평당가 생성 중')
    price = []
    
    juso = locate
    pyeng = size+'평대' ### input값

    pyengsu = {'10평대':'평수 >= 10 and 평수 < 15', '15평대':'평수 >= 15 and 평수 < 20','20평대':'평수 >= 20 and 평수 < 25',
            '25평대':'평수 >= 25 and 평수 < 30','30평대':'평수 >= 30 and 평수 < 35','35평대':'평수 >= 35 and 평수 < 40','40평대':'평수 >= 40 and 평수 < 45'}

    for i in range(6,22):
        for j in range(1,13):
            i_z = str(i).zfill(2)
            j_z = str(j).zfill(2)
            date = '20{0}{1}'.format(i_z,j_z)
            price_mean = final_tst.query('시군구 == "{}"'.format(juso)).query('계약년월=='+date).query(pyengsu[pyeng]).loc[:,'평단가'].mean()
            price_round = round(price_mean,1)
            price.append([int(date), float(price_round)])
        print('20{}'.format(str(i).zfill(2)))

    for i in range(22,23):
        for j in range(1,5):
            i_z = str(i).zfill(2)
            j_z = str(j).zfill(2)
            date = '20{0}{1}'.format(i_z,j_z)
            price_mean = final_tst.query('시군구 == "{}"'.format(juso)).query('계약년월=='+date).query(pyengsu[pyeng]).loc[:,'평단가'].mean()
            price_round = round(price_mean,1)
            price.append([int(date), float(price_round)])



    price_arr = np.array(price)
    avarage = []

    # nan은 좌우의 값을 참고해서 평균값을 내기
    for i in range(len(price)): # 전체 price 요소 훑기
        if(np.isnan(price_arr[i][1])): # nan일때
            print('nan searched',i)
            if (i==0): # 첫번째 요소라면 뒤의 2개값을 찾아서 평균내기
                print('first positioned nan')
                for j in range(1,len(price)):
                    if (np.isnan(price_arr[j][1])):
                        pass
                    else : 
                        avarage.append(price_arr[j][1])
                    if (len(avarage)==2):
                        price_arr[i][1] = sum(avarage)/len(avarage)
                        avarage=[]
                        break
            
            elif (i == len(price)-1):
                for j in range(len(price)-2,-1,-1):
                    print(j)
                    if (np.isnan(price_arr[j][1])):
                        pass
                    else :
                        avarage.append(price_arr[j][1])
                    if (len(avarage)==2):
                        price_arr[i][1] = sum(avarage)/len(avarage)
                        avarage=[]
                        break
            else:
                for j in range(i+1,len(price)): # 뒤에 nan아닌 값
                    if (np.isnan(price_arr[j][1])):
                        pass
                    else : 
                        avarage.append(price_arr[j][1])
                        avarage.append(price_arr[i-1][1])
                        price_arr[i][1] = sum(avarage)/len(avarage)
                        avarage=[]
                        break


    print('주택담보대출 금리 가져오는 중')
    path = 'media/csv_file/asdf.txt'
    interest = []

    with open(path,encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    for row in soup.findAll('row'):
        print('년월 :',row.time.text, '  주택담보대출금리 :',row.data_value.text)
        interest.append(float(row.data_value.text))


                        
    print('전처리 중')
    interest_one = []
    for i in range(len(interest)-1):
        if interest[i] < interest[i+1]:
            interest_one.append(1)
        elif interest[i] > interest[i+1]:
            interest_one.append(0)
        elif interest[i] == interest[i+1]:
            interest_one.append(interest_one[-1])
        
            
    ######################################################################################################################### 
    print('10% 증감 예측 모델 생성 중')
    # 비율을 빼볼까

    # 가격만 list만들기
    price_lst = []
    for tmp in price_arr:
        price_lst.append(round(tmp[1],1))
    print(price_lst)

    nocount=0
    #scaler = MinMaxScaler()
    #scaler.fit(price_lst)
    #price_lst = scaler.trainsform(price_lst)
    vsum = 0
    mean = sum(price_lst)/len(price_lst)

    for i in price_lst:
        vsum += (i-mean)**2
    variance = vsum/ len(price_lst)
    std = math.sqrt(variance)

    price_lst = (price_lst-mean)/std 

    price_lst = (price_lst-min(price_lst))/max(price_lst - min(price_lst))

    #s_max = max(price_lst)
    #price_lst = price_lst/s_max
    # 6달 모아서 이번달 예측 과거데이터 6개, 미래데이터 1개

    price_queter = []
    #for i in range(1, int(len(price_lst)/2)-1):
    #    price_queter.append(round((price_lst[0+2*i]*(1-interest[-1+2*i]/12)+price_lst[1+2*i]*(1-interest[0+2*i]/12))/2,2))
    #print('2달 데이터 : ',price_queter)
    #print(len(price_queter), len(price_lst))

    for i in range(1,len(price_lst)):
        price_queter.append(round(price_lst[i]*(1-interest[i-1]*0.01),1))

    pair_accuracy = []
    pair_loss = []
    pair_predict = []

    for i in range(3,11):
        learn_num = i
        leanring_data = []
        result_data = []
        price_one = [0]
        

        for i in range(len(price_queter)-1):
            if price_queter[i]< price_queter[i+1]:
                price_one.append(1)
            elif price_queter[i]> price_queter[i+1]:
                price_one.append(0)
            else :#price_lst[i]==price_lst[i+1]:
                #price_one.append(0.5)
                price_one.append(price_one[-1])
                nocount += 1

    #    print("조사에서 제외한 달 수 : " ,nocount)
    #    print("price_lst : " ,price_lst)
    #    print("price_one : " ,price_one)

        for i in range(len(price_one)-learn_num-1):
            leanring_data.append(price_one[i:i+learn_num])
            result_data.append(price_one[i+learn_num])
            train_data = np.array(leanring_data)
            target_data = np.array(result_data)

        #train_input, test_input, train_target, test_target = train_test_split(train_data, target_data, test_size=0.1)
        train_input, val_input, train_target, val_target = train_test_split(train_data, target_data, test_size=0.2)


        model = keras.Sequential()
        model.add(keras.layers.LSTM(5, input_shape = (learn_num,1), dropout=0.3))#, return_sequences=True))
        #model.add(keras.layers.LSTM(15, dropout=0.3))
        model.add(keras.layers.Dense(1, activation='relu'))
        model.compile(optimizer = 'adam', loss='mse', metrics = 'accuracy')
        print(learn_num, '번째 모델')
        checkpoint_cb = keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only= True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience =2, restore_best_weights = True)
        history = model.fit(train_input, train_target, epochs=100,validation_data = (val_input, val_target), callbacks=[checkpoint_cb, early_stopping_cb])

        if (history.history['loss'][-3:-2][0]<1):
            pair_accuracy.append(['@@\n',learn_num, history.history['accuracy'][-3:-2][0], history.history['val_accuracy'][-3:-2][0]])
            pair_loss.append(['@@\n',learn_num, history.history['loss'][-3:-2][0], history.history['val_loss'][-3:-2][0]])
            pair_predict.append([learn_num, model.predict(train_data[-1:]), train_data[-1:]])# 4개면 과거 4개를 넣어서 확인

        print(train_input[-1])
        print(train_input[:])
        print(model.predict(val_input[-1:]))
        print(model.predict(train_input[:]))

    betl = max(pair_accuracy[0][2], pair_accuracy[0][3])
    bet_accuracyl = min(pair_accuracy[0][2], pair_accuracy[0][3])
    bet_lossl = max(pair_loss[0][2], pair_loss[0][3])
    bet_numl=pair_accuracy[0][1]
    bet_predictl = pair_predict[0][1][0][0]

    if len(pair_accuracy) >2:
        for i in range(1, len(pair_accuracy)):
            if ((pair_accuracy[i][2] > (betl+bet_accuracyl)/2 or pair_accuracy[i][3] > (betl+bet_accuracyl)/2) and (abs(pair_accuracy[i][2]-pair_accuracy[i][3]))<abs(betl-bet_accuracyl)):
                betl = max(pair_accuracy[i][2], pair_accuracy[i][3])
                bet_accuracyl = min(pair_accuracy[i][2], pair_accuracy[i][3])
                bet_lossl = max(pair_loss[i][2], pair_loss[i][3])
                bet_numl = pair_accuracy[i][1]
                bet_predictl = pair_predict[i][1][0][0]

    if bet_predictl >1:
        bet_predictl =1
    print(pair_accuracy)
    print(pair_loss)
    print(bet_numl, bet_accuracyl, bet_lossl, bet_predictl)
    print("장기적 관점 : 정확도 = " ,round(bet_accuracyl*100,2),'%',' 오차 = ',round(bet_lossl*100,2),'%')


    ################################################ 1174
    print('1% 증감 예측 모델 생성 중')
    

    # 단기적 관점점으로 볼때, 향후 예측치를 보여준다. 얼마정도가 될 것인지
    #  두개를 동시에 보여주고 싶다면? 단기적 합치기, 마지막 나온 결과에서의 그래프를 보여주자

    # 비율을 빼볼까

    # 가격만 list만들기
    price_lst = []
    for tmp in price_arr:
        price_lst.append(round(tmp[1],1))
    
    price_lst2 = price_lst
    price_lst_max = max(price_lst)
    nocount=0
    #scaler = MinMaxScaler()
    #scaler.fit(price_lst)
    #price_lst = scaler.trainsform(price_lst)
    vsum = 0
    mean = sum(price_lst)/len(price_lst)

    for i in price_lst:
        vsum += (i-mean)**2
    variance = vsum/ len(price_lst)
    std = math.sqrt(variance)

    price_lst = (price_lst-mean)/std 

    price_lst = (price_lst-min(price_lst))/max(price_lst - min(price_lst))

    #s_max = max(price_lst)
    #price_lst = price_lst/s_max
    # 6달 모아서 이번달 예측 과거데이터 6개, 미래데이터 1개

    price_queter = []
    price_queter2= []
    #for i in range( int(len(price_lst)/3)-1):
    #    price_queter.append(round((price_lst[0+2*i]+price_lst[1+2*i]+price_lst[2+2*i]/3),2))
    #print('2달 데이터 : ',price_queter)
    #print(len(price_queter), len(price_lst))


    #for i in range(1,len(price_lst)):
    #    price_queter.append(round(price_lst[i]*(1-interest[i-1]*0.01)/12,2))
    #print('price_queter : ', price_queter)
    for i in range(1,len(price_lst)):
        price_queter.append(round(price_lst[i]*(1-interest[i-1]*0.01),2))
    #print('price_queter : ', price_queter)

    
    for i in range(1,len(price_lst)):
        price_queter2.append(price_lst[i]*(1-interest[i-1]*0.01))

    pair_accuracy = []
    pair_loss = []
    pair_predict = []

    for i in range(3,11):
        learn_num = i
        leanring_data = []
        result_data = []
        price_one = [0]
        

        for i in range(len(price_queter)-1):
            if price_queter[i]< price_queter[i+1]:
                price_one.append(1)
            elif price_queter[i]> price_queter[i+1]:
                price_one.append(0)
            else :#price_lst[i]==price_lst[i+1]:
                #price_one.append(0.5)
                price_one.append(price_one[-1])
                nocount += 1

    #    print("조사에서 제외한 달 수 : " ,nocount)
    #    print("price_lst : " ,price_lst)
    #    print("price_one : " ,price_one)

        for i in range(len(price_one)-learn_num-1):
            leanring_data.append(price_one[i:i+learn_num])
            result_data.append(price_one[i+learn_num])
            train_data = np.array(leanring_data)
            target_data = np.array(result_data)

        #train_input, test_input, train_target, test_target = train_test_split(train_data, target_data, test_size=0.1)
        train_input, val_input, train_target, val_target = train_test_split(train_data, target_data, test_size=0.2)


        model = keras.Sequential()
        model.add(keras.layers.LSTM(5, input_shape = (learn_num,1), dropout=0.1))#, return_sequences=True))
        #model.add(keras.layers.LSTM(15, dropout=0.3))
        model.add(keras.layers.Dense(1, activation='relu'))
        model.compile(optimizer = 'adam', loss='mse', metrics = 'accuracy')
        print(learn_num, '번째 모델')

        checkpoint_cb = keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only= True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience =2, restore_best_weights = True)
        history = model.fit(train_input, train_target, epochs=100,validation_data = (val_input, val_target), callbacks=[checkpoint_cb, early_stopping_cb])

        
        if (history.history['loss'][-3:-2][0]<1):
            pair_accuracy.append(['@@\n',learn_num, history.history['accuracy'][-3:-2][0], history.history['val_accuracy'][-3:-2][0]])
            pair_loss.append(['@@\n',learn_num, history.history['loss'][-3:-2][0], history.history['val_loss'][-3:-2][0]])
            pair_predict.append([learn_num, model.predict(train_data[-1:]), train_data[-1:]])# 4개면 과거 4개를 넣어서 확인

        print(train_input[-1])
        print(train_input[:])
        print(model.predict(val_input[-1:]))
        print(model.predict(train_input[:]))

        
    bet = max(pair_accuracy[0][2], pair_accuracy[0][3])
    bet_accuracy = min(pair_accuracy[0][2], pair_accuracy[0][3])
    bet_loss = max(pair_loss[0][2], pair_loss[0][3])
    bet_num=pair_accuracy[0][1]
    bet_predict = pair_predict[0][1][0][0]


    best = []
    if len(pair_accuracy) >2:
        for i in range(1, len(pair_accuracy)):
            if ((pair_accuracy[i][2] > (bet+bet_accuracy)/2 or pair_accuracy[i][3] > (bet+bet_accuracy)/2) and (abs(pair_accuracy[i][2]-pair_accuracy[i][3]))<abs(bet-bet_accuracy)):
                bet = max(pair_accuracy[i][2], pair_accuracy[i][3])
                bet_accuracy = min(pair_accuracy[i][2], pair_accuracy[i][3])
                bet_loss = max(pair_loss[i][2], pair_loss[i][3])
                bet_num = pair_accuracy[i][1]
                bet_predict = pair_predict[i][1][0][0]
            
            

    if bet_predict >1:
        bet_predict =1


############################################################################################################### 가격 예측모델
    # bet_num을 활용하기 그때에 맞는 model값을 만들자. 모델은 한번만 쓰고 버리면 된다. 쌓아두지 말기
    learn_num = bet_num
    leanring_data = []
    result_data = []
    price_one = []

    for i in range(len(price_queter2)-learn_num-1):
        leanring_data.append(price_queter2[i:i+learn_num])
        result_data.append(price_queter2[i+learn_num])
    train_data = np.array(leanring_data)
    target_data = np.array(result_data)

    #train_input, test_input, train_target, test_target = train_test_split(train_data, target_data, test_size=0.1)
    train_input, val_input, train_target, val_target = train_test_split(train_data, target_data, test_size=0.2)


    model = keras.Sequential()
    model.add(keras.layers.LSTM(5, input_shape = (learn_num,1), dropout=0.1))#, return_sequences=True))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer = 'adam', loss='mse', metrics = 'accuracy')

    checkpoint_cb = keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only= True)
    early_stopping_cb = keras.callbacks.EarlyStopping(patience =2, restore_best_weights = True)
    history = model.fit(train_input, train_target, epochs=100,validation_data = (val_input, val_target), callbacks=[checkpoint_cb, early_stopping_cb])
    
    #pval = model.predict(train_data) *(max(price_lst-min(price_lst) ) + min(price_lst))*std + mean
    #target_data = target_data *(max(price_lst-min(price_lst) ) + min(price_lst))*std + mean
    #pval = (model.predict(train_data) *max(price_lst-min(price_lst) ) + min(price_lst))*std + mean
    #target_data = (target_data *max(price_lst-min(price_lst) ) + min(price_lst))*std + mean
    #target_data = target_data/max(target_data) * price_lst_max
    #pval = pval/max(target_data) * price_lst_max
    #pval = model.predict(train_data) * price_lst_max
    #target_data = target_data * price_lst_max
    
    #pval = model.predict(train_data) * price_lst_max
    #pval = (pval *max(pval-min(pval) ) + min(pval))*std
    #print('target_data : ',target_data)
    #target_data = (target_data *max(target_data-min(target_data) ) + min(target_data))*std
    #target_data = target_data/max(target_data) * price_lst_max
    #pval = pval * price_lst_max
    #target_data = target_data * price_lst_max
    #pval = model.predict(train_data) * max(target_data)
    pval = model.predict(train_data) / max(target_data) * price_lst_max 
    target_data[:] = target_data[:] / max(target_data) * price_lst_max 
    plt.plot(pval[:], 'r', label='predict')
    plt.plot(target_data[:], 'b', label='actual')
    plt.legend()
    plt.savefig('media/img/predict.png')
    plt.clf()
    


    print(pair_accuracy)
    print(pair_loss)
    print(bet_num, bet_accuracy, bet_loss)
    print('지난 {}개월의 데이터를 기반으로 한 예측입니다.'.format(bet_num))
    print("단기적 관점 : 증감의 정확도 = " ,round(bet_accuracy*100,2),'%',' 오차 = ',round(bet_loss*100,2),'%')
    print('단기적 관점 : 가격예측 오차 = ',round(max(history.history['loss'][-3:-2][0],history.history['val_loss'][-3:-2][0])*100,2),'%')
    print('단기적 관점 : 예측가 = ', pval[-1:])#*(max(price_lst-min(price_lst) ) + min(price_lst))*std + mean )

    count = []
    date_lst=[]

    for i in range(18,22):
        for j in range(1,13):
            i_z = str(i).zfill(2)
            j_z = str(j).zfill(2)
            date = '20{0}{1}'.format(i_z,j_z)
            cnt = final_tst.query('시군구 == "{}"'.format(juso)).query('계약년월=='+date).query(pyengsu[pyeng]).loc[:,'평단가'].count()
            count.append([j_z, int(cnt)])
        print(date)

    for i in range(22,23):
        for j in range(1,4):
            i_z = str(i).zfill(2)
            j_z = str(j).zfill(2)
            date = '20{0}{1}'.format(i_z,j_z)
            cnt = final_tst.query('시군구 == "{}"'.format(juso)).query('계약년월=='+date).query(pyengsu[pyeng]).loc[:,'평단가'].count()
            count.append([j_z, int(cnt)])
    count_arr = np.array(count)


    print(count)
    print(count_arr)

    #plt.plot(count[:,0],count[:,1])
    #plt.show()
    plt.plot( count_arr[:,1].astype(np.int))
    plt.xticks(np.arange(0,60,6))
    plt.savefig('media/img/amount.png')
    plt.clf()
    return bet_num, round(bet_accuracy*100,2), round(bet_loss*100,2), round(bet_predict*100,2), round(max(history.history['loss'][-3:-2][0],history.history['val_loss'][-3:-2][0])*100,2), int(pval[-1:][0][0]),bet_numl,round(bet_accuracyl*100,2),round(bet_lossl*100,2), round(bet_predictl*100,2)
        # 단기 개월, 단기 정확도, 단기 오차, 단기 오차, 단기 예측값, 장기 개월수, 장기 정확도, 장기 오차 ( 8개 )



def reset_dir():
    dir_path1 = "media/img"

    if os.path.exists(dir_path1):
        shutil.rmtree(dir_path1)
        os.mkdir(dir_path1)
    else :
        os.mkdir(dir_path1)
