from dash import Dash, dcc, html, Input, Output, callback

import os
import plotly.express as px
import pandas as pd
import plotly.io as pio

#結果は　http://127.0.0.1:8050/　で確認

D        = [30,30,30,30,30,30,30,30,30,30,30,30,30,30];
O        = [2,2,2,2,2,2,2,2,2,2,2,2,3,3];


#アプリケーションの初期化
app = Dash(__name__)

app.layout = html.Div([
    html.H6("ドロップダウンメニューから描画したい図を選んで下さい:"),
    dcc.Dropdown(
        id='plot-dropdown',
        #labelの後は選択肢の名前　valueはそれを選ぶことで返される値
        options=[
            {'label': 'LIRCMOP5_k', 'value': 'LIRCMOP5_k'},
            {'label': 'LIRCMOP5_CA', 'value': 'LIRCMOP5_CA'},
            {'label': 'LIRCMOP6_k', 'value': 'LIRCMOP6_k'},
            {'label': 'LIRCMOP6_CA', 'value': 'LIRCMOP6_CA'},
            {'label': 'LIRCMOP7_k', 'value': 'LIRCMOP7_k'},
            {'label': 'LIRCMOP7_CA', 'value': 'LIRCMOP7_CA'},
            {'label': 'LIRCMOP8_k', 'value': 'LIRCMOP8_k'},
            {'label': 'LIRCMOP8_CA', 'value': 'LIRCMOP8_CA'},
            {'label': 'LIRCMOP9_k', 'value': 'LIRCMOP9_k'},
            {'label': 'LIRCMOP9_CA', 'value': 'LIRCMOP9_CA'},
            {'label': 'LIRCMOP10_k', 'value': 'LIRCMOP10_k'},
            {'label': 'LIRCMOP10_CA', 'value': 'LIRCMOP10_CA'},
            {'label': 'LIRCMOP11_k', 'value': 'LIRCMOP11_k'},
            {'label': 'LIRCMOP11_CA', 'value': 'LIRCMOP11_CA'},
            {'label': 'LIRCMOP12_k', 'value': 'LIRCMOP12_k'},
            {'label': 'LIRCMOP12_CA', 'value': 'LIRCMOP12_CA'},
            {'label': 'LIRCMOP13_k', 'value': 'LIRCMOP13_k'},
            {'label': 'LIRCMOP13_CA', 'value': 'LIRCMOP13_CA'},
            {'label': 'LIRCMOP14_k', 'value': 'LIRCMOP14_k'},
            {'label': 'LIRCMOP14_CA', 'value': 'LIRCMOP14_CA'},
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
        
        for i in range(4):
            tmp = 'x' + str(i+1)
            column.append(tmp)
            cols.append(i)
            
        for i in range(O[int(p_num)-1]):
            tmp = 'f' + str(i+1)
            column.append(tmp)
            cols.append(i+D[int(p_num)-1])
            
        filename = value.split('_')[0]
        dir = 'LIRCMOP_datalist/' + filename
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
            
            fname3 = "EMO_cv_withgrid_" + filename + ".xlsx" 
            data3 = pd.read_excel(fname3,header=None,usecols = cols)
            data3.columns = column
            data3['class'] = "Infeasible"
                 
                 
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
            
            title = "LIRCMOP" + str(p_num) + "_k:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
            
        if cla == 'CA':
            fname2 = "EMO_dominated_CA_" +filename +".xlsx" 
            data2 = pd.read_excel(fname2,header=None,usecols = cols)
            data2.columns=column
            data2['class'] = "Dominated"
            
            fname3 = "EMO_cv_CA_" +filename +".xlsx" 
            data3 = pd.read_excel(fname3,header=None,usecols = cols)
            data3.columns=column
            data3['class'] = "Infeasible"
                
            
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
            
            title = "LIRCMOP" + str(p_num) + "_CA:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
        os.chdir('../')
        os.chdir('../')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
        
#アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)