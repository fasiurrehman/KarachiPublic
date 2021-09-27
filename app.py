import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px
import numpy as np
import textwrap

def customwrap(s,width=40):
    return "<br>".join(textwrap.wrap(s,width=width))


df=pd.read_csv(("Civic.csv"))


cols=df.columns
col1,col2= st.beta_columns([1,1])

title = ["Age","Gender","Income","Area of Residence"]
opts=[]
for val in range(2,6):
    opt = st.sidebar.selectbox(
        title[val-2],
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
            df_col = pd.DataFrame(civic[col]) ; df_col = df_col.assign(var1=df_col[col].str.split(';')).explode('var1'); df_col[col] = df_col['var1']; df_col = df_col.drop('var1',axis=1);

            out = pd.DataFrame.from_dict(Counter(df_col[col].to_list()), orient='index').reset_index();
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
new=pd.read_csv(r"new.csv")


def treeplot(df,width=300, height=400):
    df[df.columns[0]]=df[df.columns[0]].map(customwrap)
    df["Percentage"]=df["count"].round(2)
    df["Answers"]=df[df.columns[0]]
    df.sort_values("Percentage",ascending=False,inplace=True)
    intensity=100
    colors_=[col1]

    intensity=100
    colors_=[]
    for i in range(0,len(df)):
        colors_.append("rgba(22, 86, 93,"+str(round(intensity/100,2))+")")
        intensity=intensity-(intensity*0.10)
    
    vals=df.sort_values("Percentage",ascending=False)["Answers"].to_list()
    res = {}
    res["(?)"]="lightgray"
    for key in vals:
        for value in colors_:
            res[key] = value
            colors_.remove(value)
            break  
        
    if width!=300:
        fig = px.treemap(df,path=[px.Constant("Reponses"),"Answers"], values='count'
                         ,custom_data=[df.columns[1],df.columns[0]],width=width, height=height,
                        color="Answers",color_discrete_map=res
                         )
    else:
        fig = px.treemap(df,path=[px.Constant("Reponses"),"Answers"], values='count'
                            ,custom_data=[df.columns[1],df.columns[0]],color="Answers",color_discrete_map=res)
    
    fig.update_traces( hovertemplate="<br>".join([
         "%{customdata[1]}",
        "Percentage: %{customdata[0]}"
    ]))

    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20))
    
    return fig

def countplot(data,width=300, height=400):
    data.sort_values(data.columns[1],ascending=True,inplace=True)

    data[data.columns[0]]=data[data.columns[0]].map(customwrap)
    fig = px.scatter(data, x=np.zeros(len(data)), y=data.columns[0],size=data.columns[1],size_max=40
                        ,width=300, height=400,text=data.columns[0],
                    labels={
                        data.columns[0]: ""
                    },custom_data=[data.columns[1],data.columns[0]])
                        
    fig.update_xaxes(visible=False, showticklabels=False,showgrid = False , showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(visible=True, showticklabels=False,showgrid = False,showline=True, linewidth=1, linecolor='black', mirror=True)
    # fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    # fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_traces(textposition='bottom center')
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
)   
    fig.update_traces(
    hovertemplate="<br>".join([
         "%{customdata[1]}",
        "%{customdata[0]}%"
    ])
    
)   
    fig.update_layout({
'plot_bgcolor': 'rgb(163, 211,221)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
    fig.update_traces(marker=dict(color = 'rgba(66,126,152,1)'))
    return fig


civic=count(civic)
exp=count(exp)
desires=count(desires)
acess=count(acess)
new=count(new)

# new.to_csv("out.csv")

st.title('On Experience at Clifton Beach')

col4a= st.beta_columns([1])[0]
with col4a:
    col4a.markdown(exp[0][1].columns[0])
    col4a.plotly_chart(treeplot(exp[0][1]))


col6,col7= st.beta_columns([1,1])
with col6:
    col6.markdown(exp[0][2].columns[0])
    col6.plotly_chart(countplot(exp[0][2]))

with col7:
    col7.markdown(exp[0][3].columns[0])
    col7.plotly_chart(countplot(exp[0][3]))

col5a= st.beta_columns([1])[0]
with col5a:
    col5a.markdown(exp[0][0].columns[0])
    col5a.plotly_chart(treeplot(exp[0][0]))

st.title("On Accessing Clifton Beach")
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

df["Percentage"] = df["size"]/(df["size"].sum())
df["Percentage"] = df["Percentage"].round(2)
df["Location"]=df["map: Where do you access the beach from most of the time?"]

fig=px.scatter_mapbox(df,zoom=10,opacity=.90, lon = df['lon'],lat = df['lat'],size="Percentage",
                    text ="Location")

fig.update_layout(font_size=1,  title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,}, 
        title_font_size = 16, mapbox_accesstoken=api_token, 
        mapbox_style = "mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")

st.plotly_chart(fig)

st.title('On Desires for Clifton Beach and the Coast')

# desires
col7,col8= st.beta_columns([1,1])
with col7:
    col7.markdown(desires[0][1].columns[0])
    col7.plotly_chart(countplot(desires[0][1],width=370,height=450))

with col8:
    col8.markdown(desires[0][0].columns[0])
    col8.plotly_chart(treeplot(desires[0][0]))

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

st.title('On Civic Well-Being')
col1,col2= st.beta_columns([1,1])
col3= st.beta_columns([1])[0]

with col1:
    col1.markdown(civic[0][2].columns[0])
    col1.plotly_chart(countplot(civic[0][2]))

with col2:
    col2.markdown(civic[0][1].columns[0])
    col2.plotly_chart(countplot(civic[0][1]))

col3.markdown(civic[0][0].columns[0])
col3.plotly_chart(treeplot(civic[0][0]))


st.title('New Questions')



col1i,col2i,col4i= st.beta_columns([1,1,1])

with col1i:
    col1i.markdown(new[0][3].columns[0])
    col1i.plotly_chart(countplot(new[0][3] , width=200, height=400))

# col1i,col2i= st.beta_columns([1,1])
with col2i:
    col2i.markdown(new[0][4].columns[0])
    col2i.plotly_chart(countplot(new[0][4]))


with col4i:
    col4i.markdown(new[0][6].columns[0])
    col4i.plotly_chart(countplot(new[0][6]))

col3i= st.beta_columns([1])[0]

with col3i:
    col3i.markdown(new[0][5].columns[0])
    col3i.plotly_chart(treeplot(new[0][5]))


col5i,col6i= st.beta_columns([1,1])
with col5i:
    col5i.markdown(new[0][7].columns[0])
    col5i.plotly_chart(countplot(new[0][7]))

with col6i:
    col6i.markdown(new[0][8].columns[0])
    col6i.plotly_chart(countplot(new[0][8]))

#
col7i,col8i= st.beta_columns([1,1])

with col7i:
    col7i.markdown(new[0][9].columns[0])
    col7i.plotly_chart(countplot(new[0][9]))

with col8i:
    col8i.markdown(new[0][10].columns[0])
    col8i.plotly_chart(countplot(new[0][10]))

col9i,col10i= st.beta_columns([1,1])

with col9i:
    col9i.markdown(new[0][11].columns[0])
    col9i.plotly_chart(countplot(new[0][11]))

with col10i:
    col10i.markdown(new[0][12].columns[0])
    col10i.plotly_chart(countplot(new[0][12]))

# col11,col12= st.beta_columns([1,1])

# with col11:
#     col11.markdown(new[0][11].columns[0])
#     col11.plotly_chart(countplot(new[0][11]))

# with col12:
#     col12.markdown(new[0][12].columns[0])
#     col12.plotly_chart(countplot(new[0][12]))


col11,col12= st.beta_columns([1,1])

with col11:
    col11.markdown(new[0][13].columns[0])
    col11.plotly_chart(countplot(new[0][13]))

with col12:
    col12.markdown(new[0][14].columns[0])
    col12.plotly_chart(countplot(new[0][14]))

col13,col14= st.beta_columns([1,1])

with col13:
    col13.markdown(new[0][15].columns[0])
    col13.plotly_chart(countplot(new[0][15]))

with col14:
    col14.markdown(new[0][16].columns[0])
    col14.plotly_chart(countplot(new[0][16]))

col15,col16= st.beta_columns([1,1])

with col15:
    col15.markdown(new[0][17].columns[0])
    col15.plotly_chart(countplot(new[0][17]))

with col16:
    col16.markdown(new[0][18].columns[0])
    col16.plotly_chart(countplot(new[0][18]))