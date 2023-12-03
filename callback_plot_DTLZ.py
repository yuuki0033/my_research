from dash import Dash, dcc, html, Input, Output, callback

import os
import plotly.express as px
import pandas as pd
import plotly.io as pio

#結果は　http://127.0.0.1:8050/　で確認

D = [7,12,12,12,12,12];
O = [3,3,3,3,3,3];

#アプリケーションの初期化
app = Dash(__name__)

app.layout = html.Div([
    html.H6("ドロップダウンメニューから描画したい図を選んで下さい:"),
    dcc.Dropdown(
        id='plot-dropdown',
        #labelの後は選択肢の名前　valueはそれを選ぶことで返される値
        options=[
            {'label': 'DTLZ1_k', 'value': 'DTLZ1_k'},
            {'label': 'DTLZ1_CA', 'value': 'DTLZ1_CA'},
            {'label': 'DTLZ2_k', 'value': 'DTLZ2_k'},
            {'label': 'DTLZ2_CA', 'value': 'DTLZ2_CA'},
            {'label': 'DTLZ3_k', 'value': 'DTLZ3_k'},
            {'label': 'DTLZ3_CA', 'value': 'DTLZ3_CA'},
            {'label': 'DTLZ4_k', 'value': 'DTLZ4_k'},
            {'label': 'DTLZ4_CA', 'value': 'DTLZ4_CA'},
            {'label': 'DTLZ5_k', 'value': 'DTLZ5_k'},
            {'label': 'DTLZ5_CA', 'value': 'DTLZ5_CA'},
            {'label': 'DTLZ6_k', 'value': 'DTLZ6_k'},
            {'label': 'DTLZ6_CA', 'value': 'DTLZ6_CA'},
            
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
        tmp = value.split('Z')[1]
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
        dir = 'DTLZ_datalist/' + filename
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
            
            data = pd.concat([data2,data1])
            fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua', 'red'])   
            l1 = len(data1)
            l2 = len(data2)
            total = len(data)
            rate_p = '{:.1%}'.format(l1/total)
            rate_d = '{:.1%}'.format(l2/total)
            title2 = " Pareto " + rate_p + ", Dominated " + rate_d
                                        
                
            title = "DTLZ" + str(p_num) + "_k:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
        
        if cla == 'CA':
            fname2 = "EMO_dominated_CA_" +filename +".xlsx" 
            data2 = pd.read_excel(fname2,header=None)
            data2.columns=column
            data2['class'] = "Dominated"
            
                
            data = pd.concat([data2,data1])
            fig = px.scatter_matrix(data,dimensions=column,color = "class",color_discrete_sequence = ['aqua', 'red'])  
            l1 = len(data1)
            l2 = len(data2)
            total = len(data)
            rate_p = '{:.1%}'.format(l1/total)
            rate_d = '{:.1%}'.format(l2/total)
            title2 = " Pareto " + rate_p + ", Dominated " + rate_d
                
            title = "DTLZ" + str(p_num) + "_CA:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
            
        os.chdir('../')
        os.chdir('../')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
        
        
     
#アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)
            