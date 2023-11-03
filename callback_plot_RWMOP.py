from dash import Dash, dcc, html, Input, Output, callback

import os
import plotly.express as px
import pandas as pd
import plotly.io as pio

#結果は　http://127.0.0.1:8050/　で確認

D = [4,5,3,4,4,7,4,7,4,2,3,4,7,5,3,2,6,3,10,4,6,9,6,9,2,3,3,8,7,25,25,25,30,30,30,28,28,28,28,34,34,34,34,34,34,34,18,18,18,6];
O = [2,2,2,2,2,2,2,3,2,2,5,2,3,2,2,2,3,2,3,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,3,2,2,3,3,4,2,2,3,2];

#アプリケーションの初期化
app = Dash(__name__)

app.layout = html.Div([
    html.H6("ドロップダウンメニューから描画したい図を選んで下さい:"),
    dcc.Dropdown(
        id='plot-dropdown',
        #labelの後は選択肢の名前　valueはそれを選ぶことで返される値
        options=[
            {'label': 'RWMOP1_k', 'value': 'RWMOP1_k'},
            {'label': 'RWMOP1_CA', 'value': 'RWMOP1_CA'},
            {'label': 'RWMOP2_k', 'value': 'RWMOP2_k'},
            {'label': 'RWMOP2_CA', 'value': 'RWMOP2_CA'},
            {'label': 'RWMOP4_k', 'value': 'RWMOP4_k'},
            {'label': 'RWMOP4_CA', 'value': 'RWMOP4_CA'},
            {'label': 'RWMOP5_k', 'value': 'RWMOP5_k'},
            {'label': 'RWMOP5_CA', 'value': 'RWMOP5_CA'},
            {'label': 'RWMOP6_k', 'value': 'RWMOP6_k'},
            {'label': 'RWMOP6_CA', 'value': 'RWMOP6_CA'},
            {'label': 'RWMOP7_k', 'value': 'RWMOP7_k'},
            {'label': 'RWMOP7_CA', 'value': 'RWMOP7_CA'},
            {'label': 'RWMOP8_k', 'value': 'RWMOP8_k'},
            {'label': 'RWMOP8_CA', 'value': 'RWMOP8_CA'},
            {'label': 'RWMOP9_k', 'value': 'RWMOP9_k'},
            {'label': 'RWMOP9_CA', 'value': 'RWMOP9_CA'},
            {'label': 'RWMOP10_k', 'value': 'RWMOP10_k'},
            {'label': 'RWMOP10_CA', 'value': 'RWMOP10_CA'},
            {'label': 'RWMOP11_k', 'value': 'RWMOP11_k'},
            {'label': 'RWMOP11_CA', 'value': 'RWMOP11_CA'},
            {'label': 'RWMOP12_k', 'value': 'RWMOP12_k'},
            {'label': 'RWMOP12_CA', 'value': 'RWMOP12_CA'},
            {'label': 'RWMOP13_k', 'value': 'RWMOP13_k'},
            {'label': 'RWMOP13_CA', 'value': 'RWMOP13_CA'},
            {'label': 'RWMOP14_k', 'value': 'RWMOP14_k'},
            {'label': 'RWMOP14_CA', 'value': 'RWMOP14_CA'},
            {'label': 'RWMOP16_k', 'value': 'RWMOP16_k'},
            {'label': 'RWMOP16_CA', 'value': 'RWMOP16_CA'},
            {'label': 'RWMOP17_k', 'value': 'RWMOP17_k'},
            {'label': 'RWMOP17_CA', 'value': 'RWMOP17_CA'},
            {'label': 'RWMOP18_k', 'value': 'RWMOP18_k'},
            {'label': 'RWMOP18_CA', 'value': 'RWMOP18_CA'},
            {'label': 'RWMOP19_k', 'value': 'RWMOP19_k'},
            {'label': 'RWMOP19_CA', 'value': 'RWMOP19_CA'},
            {'label': 'RWMOP20_k', 'value': 'RWMOP20_k'},
            {'label': 'RWMOP20_CA', 'value': 'RWMOP20_CA'},
            {'label': 'RWMOP21_k', 'value': 'RWMOP21_k'},
            {'label': 'RWMOP21_CA', 'value': 'RWMOP21_CA'},
            {'label': 'RWMOP25_k', 'value': 'RWMOP25_k'},
            {'label': 'RWMOP25_CA', 'value': 'RWMOP25_CA'},
            {'label': 'RWMOP26_k', 'value': 'RWMOP26_k'},
            {'label': 'RWMOP26_CA', 'value': 'RWMOP26_CA'},
            {'label': 'RWMOP27_k', 'value': 'RWMOP27_k'},
            {'label': 'RWMOP27_CA', 'value': 'RWMOP27_CA'},
        ],
    ),
    #html.Br()はHTMLの改行要素を表す
    html.Br(),
    html.Div(id='output-message')
])

@app.callback(
    Output('output-message', 'children'),
    Input('plot-dropdown', 'value')
)
def update_message(value):
    
    #if文は選択されていない場合のエラー回避のため
    if value:
        tmp = value.split('P')[1]
        p_num = tmp.split('_')[0]
        cla = tmp.split('_')[1]
        column = []
        cols = []
        
        for i in range(D[int(p_num)-1]):
            tmp = 'x' + str(i+1)
            column.append(tmp)
            cols.append(i)
            
        for i in range(O[int(p_num)-1]):
            tmp = 'f' + str(i+1)
            column.append(tmp)
            cols.append(i+D[int(p_num)-1])
            
        filename = value.split('_')[0]
        #dir = 'RWMOP_data/' + filename
        dir = 'RWMOP_datalist/' + filename
        os.chdir(dir)
        
        #データ読み込み開始
        fname1 = "EMO_pareto_" + filename + ".xlsx" 
        data1 = pd.read_excel(fname1,header=None,usecols = cols)
        data1.columns=column
        data1['class'] = "Pareto"
        
        #クラスタリング手法によって読み込むファイルを変更
        if cla == 'k':
            fname2 = "EMO_dominated_withgrid_" + filename + ".xlsx" 
            data2 = pd.read_excel(fname2,header=None,usecols = cols)
            data2.columns = column
            data2['class'] = "Dominated"
            
            if  int(p_num) != 9 and int(p_num) != 10 and int(p_num) != 21:
                 fname3 = "EMO_cv_withgrid_" + filename + ".xlsx" 
                 data3 = pd.read_excel(fname3,header=None,usecols = cols)
                 data3.columns = column
                 data3['class'] = "Infeasible"
                 
                 
            if  int(p_num) == 9 or int(p_num) == 10 or int(p_num) == 21:
                data = pd.concat([data2,data1])
                fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua', 'red'])   
                l1 = len(data1)
                l2 = len(data2)
                total = len(data)
                rate_p = '{:.1%}'.format(l1/total)
                rate_d = '{:.1%}'.format(l2/total)
                title2 = " Pareto " + rate_p + ", Dominated " + rate_d
                
            else:
                data = pd.concat([data2,data3,data1])
                fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua','gray','red'])
                l1 = len(data1)
                l2 = len(data2)
                l3 = len(data3)
                total = len(data)
                rate_p = '{:.1%}'.format(l1/total)
                rate_d = '{:.1%}'.format(l2/total)
                rate_i = '{:.1%}'.format(l3/total)
                title2 = " Pareto " + rate_p + ", Dominated " + rate_d + ", Infeasible " + rate_i
                
            title = "RWMOP" + str(p_num) + "_k:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
        
        if cla == 'CA':
            fname2 = "EMO_dominated_CA_" +filename +".xlsx" 
            data2 = pd.read_excel(fname2,header=None)
            data2.columns=column
            data2['class'] = "Dominated"
            
            if  int(p_num) != 9 and int(p_num) != 10 and int(p_num) != 21:
                fname3 = "EMO_cv_CA_" +filename +".xlsx" 
                data3 = pd.read_excel(fname3,header=None)
                data3.columns=column
                data3['class'] = "Infeasible"
                
            if  int(p_num) == 9 or int(p_num) == 10 or int(p_num) == 21:
                data = pd.concat([data2,data1])
                fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua', 'red'])  
                l1 = len(data1)
                l2 = len(data2)
                total = len(data)
                rate_p = '{:.1%}'.format(l1/total)
                rate_d = '{:.1%}'.format(l2/total)
                title2 = " Pareto " + rate_p + ", Dominated " + rate_d
                
            else:
                data = pd.concat([data2,data3,data1])
                fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua','gray','red'])
                l1 = len(data1)
                l2 = len(data2)
                l3 = len(data3)
                total = len(data)
                rate_p = '{:.1%}'.format(l1/total)
                rate_d = '{:.1%}'.format(l2/total)
                rate_i = '{:.1%}'.format(l3/total)
                title2 = " Pareto " + rate_p + ", Dominated " + rate_d + ", Infeasible " + rate_i
                
            title = "RWMOP" + str(p_num) + "_CA:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
            
        os.chdir('../')
        os.chdir('../')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
        
        
     
#アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)