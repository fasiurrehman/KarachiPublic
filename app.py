import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px
import numpy as np
import textwrap

def customwrap(s,width=40):
    return "<br>".join(textwrap.wrap(s,width=width))

st.title('Civic')
df=pd.read_csv(r"civic.csv")


cols=df.columns

opts=[]
for val in range(2,6):
    opt = st.sidebar.selectbox(
        cols[val],
        ["All"]+list(df[cols[val]].unique()))
    
    opts.append(opt)

def count(civic):
    for val in range(2,6):
        if opts[val-2]!="All":
            print(opts[val-2],civic.columns[val])
            civic=civic[civic[civic.columns[val]]==opts[val-2]]
    outs=[]
    maps=[]
    abc=[]
    ops=[]
    for col in civic.columns[6:]:
        if ":" not in col:
            out = pd.DataFrame.from_dict(Counter(civic[col].to_list()), orient='index').reset_index()
            out.rename({"index":col,0:"count"},axis=1,inplace=True)
            out=out[~out[col].isnull()]
            out["count"]=((out["count"]/out["count"].sum())*100).round(2)
            outs.append(out)
        elif "map:" in col:
            maps.append(civic[col])
        elif "op:" in col:
            ops.append(civic[col])
    return [outs,maps,ops]

exp=pd.read_csv(r"Experience.csv")
civic=pd.read_csv(r"Civic.csv")
desires=pd.read_csv(r"Desires.csv")
acess=pd.read_csv(r"acess.csv")


def treeplot(df,width=300, height=400):
    df[df.columns[0]]=df[df.columns[0]].map(customwrap)
    if width!=300:
        fig = px.treemap(df,path=[df.columns[0]], values='count'
                         ,custom_data=[df.columns[1],df.columns[0]],width=width, height=height)
    else:
        fig = px.treemap(df,path=[df.columns[0]], values='count'
                            ,custom_data=[df.columns[1],df.columns[0]])
    fig.update_traces( hovertemplate="<br>".join([
         "%{customdata[1]}",
        "Percentage: %{customdata[0]}"
    ]))
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20))   
    return fig

def countplot(data,width=300, height=400):
    data[data.columns[0]]=data[data.columns[0]].map(customwrap)
    fig = px.scatter(data, x=np.zeros(len(data)), y=data.columns[0],size=data.columns[1],size_max=40
                        ,width=300, height=400,text=data.columns[0],
                    labels={
                        data.columns[0]: ""
                    },custom_data=[data.columns[1],data.columns[0]])
                        
    fig.update_xaxes(visible=False, showticklabels=False,showgrid = False)
    fig.update_yaxes(visible=False, showticklabels=False,showgrid = False)
    fig.update_traces(textposition='bottom center')
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
)   
    fig.update_traces(
    hovertemplate="<br>".join([
         "%{customdata[1]}",
        "Percentage: %{customdata[0]}"
    ])
)
    return fig


civic=count(civic)
exp=count(exp)
desires=count(desires)
acess=count(acess)


col1,col2= st.beta_columns([1,1])
col3= st.beta_columns([1])[0]
with col1:
    col1.markdown(civic[0][0].columns[0])
    col1.plotly_chart(countplot(civic[0][0]))

with col2:
    col2.markdown(civic[0][1].columns[0])
    col2.plotly_chart(countplot(civic[0][1]))

col3.markdown(civic[0][2].columns[0])
col3.plotly_chart(treeplot(civic[0][2]))



st.title('Experience')

col4,col5= st.beta_columns([1,1])
col6= st.beta_columns([1])[0]
with col4:
    col4.markdown(exp[0][1].columns[0])
    col4.plotly_chart(countplot(exp[0][1]))

with col5:
    col5.markdown(exp[0][0].columns[0])
    col5.plotly_chart(countplot(exp[0][0]))

with col6:
    col6.markdown(exp[0][1].columns[0])
    col6.plotly_chart(treeplot(exp[0][1]))

st.title('Desires')

# desires
col7,col8= st.beta_columns([1,1])
with col7:
    col7.markdown(desires[0][1].columns[0])
    col7.plotly_chart(treeplot(desires[0][1],width=370,height=450))

with col8:
    col8.markdown(desires[0][0].columns[0])
    col8.plotly_chart(countplot(desires[0][0]))

pd.set_option("display.max_colwidth", -1)

st.markdown("What are your recommendations?")
selected = st.text_input("Search for keywords")
df=pd.DataFrame()
df["responses"]=desires[2][0].to_list()
df=df[~df["responses"].isnull()]
# st.text(df)
st.text(df[df[df.columns[0]].str.contains(selected)]["responses"].reset_index().drop("index",axis=1))
# col9.markdown(desires[0][2].columns[0])
# col9.plotly_chart(treeplot(desires[0][2]))

st.title("Access")
col9,col10= st.beta_columns([1,1])
with col9:
    col9.markdown(acess[0][0].columns[0])
    col9.plotly_chart(countplot(acess[0][0]))

with col10:
    col10.markdown(acess[0][1].columns[0])
    col10.plotly_chart(countplot(acess[0][1]))


acess2=pd.read_csv(r"acess.csv")
cols=[]
for i in acess2.columns:
    if "map:" in i:
        cols.append(i)

df=pd.DataFrame()
df[cols[0]]=acess[1][0].to_list()

df=pd.DataFrame.from_dict(Counter(df[cols[0]].to_list()), orient='index').reset_index()
df.rename({"index":cols[0],0:"count"},axis=1,inplace=True)
df=df[~df[cols[0]].isnull()]
df=df.merge(acess2[cols],how="left",on=cols[0])
df=df[~df.duplicated()]


df=df.rename({"map:x":"lat","map:y":"lon"},axis=1)
df["lon"]=df["lon"].astype("float")
df["lat"]=df["lat"].astype("float")
df["size"]=df["count"]

st.markdown(cols[0].split(":")[1])
api_token = "pk.eyJ1IjoiZmFzaWttYW41IiwiYSI6ImNrcTd5aDFtbDBhdW8yb3Fra3ZiMWJrN2YifQ.DnXjEIrwb34tjJLriZFukw"
fig=px.scatter_mapbox(df,zoom=10,opacity=.90, lon = df['lon'],lat = df['lat'],size="size")
fig.update_layout(font_size=16,  title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,}, 
        title_font_size = 24, mapbox_accesstoken=api_token, mapbox_style = "mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")
st.plotly_chart(fig)
# acess[1][1].to_list()
# acess[1][2].to_list()


# acess