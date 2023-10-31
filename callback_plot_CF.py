from dash import Dash, dcc, html, Input, Output, callback

import os
import plotly.express as px
import pandas as pd
import plotly.io as pio

#結果は　http://127.0.0.1:8050/　で確認

D  = [5,5,5,5,5,5,5,5,5,5];
O  = [2,2,2,2,2,2,2,3,3,3];

#アプリケーションの初期化
app = Dash(__name__)

app.layout = html.Div([
    html.H6("ドロップダウンメニューから描画したい図を選んで下さい:"),
    dcc.Dropdown(
        id='plot-dropdown',
        #labelの後は選択肢の名前　valueはそれを選ぶことで返される値
        options=[
            {'label': 'CF1_k', 'value': 'CF1_k'},
            {'label': 'CF1_CA', 'value': 'CF1_CA'},
            {'label': 'CF2_k', 'value': 'CF2_k'},
            {'label': 'CF2_CA', 'value': 'CF2_CA'},
            {'label': 'CF3_k', 'value': 'CF3_k'},
            {'label': 'CF3_CA', 'value': 'CF3_CA'},
            {'label': 'CF4_k', 'value': 'CF4_k'},
            {'label': 'CF4_CA', 'value': 'CF4_CA'},
            {'label': 'CF5_k', 'value': 'CF5_k'},
            {'label': 'CF5_CA', 'value': 'CF5_CA'},
            {'label': 'CF6_k', 'value': 'CF6_k'},
            {'label': 'CF6_CA', 'value': 'CF6_CA'},
            {'label': 'CF7_k', 'value': 'CF7_k'},
            {'label': 'CF7_CA', 'value': 'CF7_CA'},
            {'label': 'CF8_k', 'value': 'CF8_k'},
            {'label': 'CF8_CA', 'value': 'CF8_CA'},
            {'label': 'CF9_k', 'value': 'CF9_k'},
            {'label': 'CF9_CA', 'value': 'CF9_CA'},
            {'label': 'CF10_k', 'value': 'CF10_k'},
            {'label': 'CF10_CA', 'value': 'CF10_CA'},
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
        tmp = value.split('F')[1]
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
        dir = 'CF_datalist/' + filename
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
            
            title = "CF" + str(p_num) + "_k:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
        if cla == 'CA':
            fname2 = "EMO_dominated_CA_" +filename +".xlsx" 
            data2 = pd.read_excel(fname2,header=None)
            data2.columns=column
            data2['class'] = "Dominated"
            
            fname3 = "EMO_cv_CA_" +filename +".xlsx" 
            data3 = pd.read_excel(fname3,header=None)
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
            
            title = "CF" + str(p_num) + "_CA:" + title2
            fig.update_layout(title=title,height=800, width=800)
            
            
            
        os.chdir('../')
        os.chdir('../')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
        
#アプリケーションの実行
if __name__ == '__main__':
    app.run(debug=True)