import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import cufflinks as cf
cf.go_offline()

#loading Dataset 
df = pd.read_csv('E:\ML Datasets\Global Terrorism\globalt.csv', encoding = 'cp1252')

df.head()
df.isnull().any()
#size of the dataset 
df.shape
msno.matrix(df)

df.isnull().sum()
#Replacing encoded unknown values with NaN and visualising that
df = df.replace({
"property":-9, "INT_LOG":-9, "INT_MISC":-9, "INT_IDEO":-9, "INT_NE":-9,
"attacktype1":9, "targtype1":20,"weaptype1":13,
"crit1":0,"crit2":0,"crit3":0,
"doubtterr":1,"ishostkid":-9,
"attacktype1_txt" : 'Unknown',
"targsubtype1_txt" : 'Unknown',
"weaptype1_txt": 'Unknown',
"imonth": 0,
"iday": 0,

},np.NaN)
df.shape
df.isna().sum()
df.shape
#Removing columns > 15% missing values and visualising it
missing_percentages = df.isna().sum().sort_values(ascending = False)/len(df)
missing_percentages
list_empty_columns = list(missing_percentages[missing_percentages > 0.15].index.values)
df.drop(list_empty_columns,inplace=True,axis=1)
df.shape
##dropping columns
df.drop(['eventid','imonth','iday','extended',"provstate","latitude","longitude","specificity",'targsubtype1','targsubtype1_txt','guncertain1','weapsubtype1',
'weapsubtype1_txt','dbsource'], axis = 1,inplace=True)
group=df[['gname','nkill','nwound']].value_counts()
#===================================================================================     
##Function that removes above 5% null values
def divide_dataframe5per(a,b):
    temp_df = df.iloc[a:b]
    for i in range(a,b):
        print("Nan in row ", i , " : " , df.iloc[i].isnull().sum()/len(df.columns)) 
        if (df.iloc[i].isnull().sum()/len(df.columns) > 0.05):
             temp_df.drop([i],axis=0,inplace=True)  
             
        else:
             pass
   
    temp_df01 = temp_df.copy()
    return temp_df01   
##Removing data above 5%
temp_df21=divide_dataframe5per(0,25000)
temp_df22=divide_dataframe5per(25000,50000)
temp_df23=divide_dataframe5per(50000, 75000)
temp_df24=divide_dataframe5per(75000,100000)
temp_df25=divide_dataframe5per(100000,125000)
temp_df26=divide_dataframe5per(125000,150000)
temp_df27=divide_dataframe5per(150000,175000)
temp_df28=divide_dataframe5per(175000,181696)


#=====================================================================================

modified_df2 = pd.concat([temp_df21,temp_df22,temp_df23,temp_df24,temp_df25,temp_df26,temp_df27,temp_df28], axis=0)
modified_df2=modified_df2.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
modified_df2.drop('index',axis = 1,inplace= True)

## Imputing the values 
modified_df2['nkill'].fillna(modified_df2['nkill'].std(axis = 0, skipna = True), inplace=True)
modified_df2['nwound'].fillna(modified_df2['nwound'].std(axis = 0, skipna = True), inplace=True)
##modified_df2.to_csv('E:\ML Datasets\Global Terrorism\GTD_modified_rowsremoved2.csv', sep='\t')

with pd.ExcelWriter('E:\ML Datasets\Global Terrorism\GTD_modified_rowsremoved2.xlsx') as writer:
    modified_df2.to_excel(writer)
    
## Frequency of attacks
plt.figure(figsize=(30,30))
sns.countplot(x='iyear',data=modified_df2)
plt.title('Frequency of attacks')

##groupname with most number of kills and wounded
gangs = modified_df2[modified_df2['gname'] != 'Unknown']
l = gangs.groupby('gname').agg({'nkill':'sum','nwound':'sum'}).sort_values(by=['nkill'],ascending=True)
lkill_wound=l[(l['nkill']>=4500)]
lkill_wound.plot.barh(stacked=True)
plt.title('Gang responsible for most number of kils and wounds')
# =============================================================================
# Looking at the plot these are the most active gangs responsible for most number of kills
# The Islamic State of Iraq and The Levant is the gang with most number of kills ISIL, has also allied 
# with the terrorist group Al-Qaeda , In May 2015 in the Iraq attacks 450 people were killed by ISIL
# 
# Next is Taliban that emerged during the Afghan Civil War which consisted of students 

# Boko Haram is a terrorist organization based in Nigeria 
# =============================================================================

#Visualising weapons with respect to attack types
attacktype_weapontype_table = pd.crosstab(index=modified_df2["attacktype1_txt"], columns=modified_df2["weaptype1_txt"])
attacktype_weapontype_table.plot(kind="bar",figsize=(10,10),stacked=True)

##Visualising weapons with respect to target type
targettype_weapontype_table = pd.crosstab(index=modified_df2["targtype1_txt"], columns=modified_df2["weaptype1_txt"])
targettype_weapontype_table.plot(kind="bar",figsize=(10,10),stacked=True)
plt.xlabel("Target Type")
plt.ylabel("Weapon Type")


##The most active gang in kills and wounds from 1970 to 2009
gangs_b_2000 = gangs[gangs['iyear']<= 2009]
kw_past = gangs_b_2000.groupby('gname').agg({'nkill':'sum','nwound':'sum'}).sort_values(by=['nkill'],ascending=True)
kwp_kill_wound=kw_past[(kw_past['nkill']>=1800)]
kwp_kill_wound.plot.barh(stacked=True)
plt.title('Most active gangs from 1970 to 2009')


# =============================================================================
# During the period 1970 - 2000 we could see the most active group is the Shining Path which a communist guerilla group in PEru
# 
# Secong most active is the LTTE (Liberation Tigers Of Tamil Eelam) responsible for the assasination of Rajiv Gandhi the prime minister of India during that period 
# =============================================================================
##region and attack type
att = pd.crosstab(modified_df2['region_txt'], modified_df2['attacktype1_txt'], rownames=['region_txt'], colnames=['attacktype1_txt'])
att.plot.barh(stacked=True,figsize=(10,10))
plt.title('Attacked regions with attack type')

  
# =============================================================================
# Looking at the plot we could infer that Middle East and North Africa is most effected region with bombing and explosions the most frequent attack type 
# Followed by South Asia with bombing and explosion as the most used attack type  
# Australia is the least effected when compared to all the regions   
# =============================================================================

##10 Most attacked cities with more no of kills and group that attacked in india
df_india=modified_df2[modified_df2['country_txt']=='India']
df_india = df_india[df_india['city'] !='Unknown']

ind_gp = df_india.groupby(['city','gname']).agg({'nkill':'sum'}).sort_values(by=['nkill'],ascending=True)
ind_gp1=ind_gp[ind_gp['nkill']>100]
ind_gp1.plot.pie(y='nkill',autopct="%.2f",figsize=(5,5),legend=False);
plt.title('Cities with most number of kills in India and the groups responsible')

# =============================================================================
# Most number of kills were seen in Srinagar but the gang names are unknown 
# it is followed by Amritsar by Sikh Extremists 
# Third most attacked city is Mumbai the group responsible is Lashkar-e-Taiba
# 
# =============================================================================
 

## gangs most used weapons and targets

name_targ_weap = modified_df2[modified_df2['gname']!='Unknown'].groupby(['gname','targtype1_txt','weaptype1_txt']).agg({'nkill':'sum'}).sort_values(by=['nkill'],ascending=True)
name_targ_weap1 = name_targ_weap[name_targ_weap['nkill']>2000]
name_targ_weap1.plot.pie(y='nkill',autopct="%.2f",figsize=(10,15),legend=False);
plt.title('Gangs and their most prefered target and weapons')


name_targ_weap1.plot.barh(stacked=True)

att_t = pd.crosstab(modified_df2['gname'],modified_df2['targtype1_txt'], rownames=['gname'], colnames=['targtype1_txt'])
att_t.plot.barh(stacked=True)
##Gangs Active After 2010
gangs_p_2010 = gangs[gangs['iyear']> 2010]
kw_past2010 = gangs_p_2010.groupby('gname').agg({'nkill':'sum','nwound':'sum'}).sort_values(by=['nkill'],ascending=True)
kwp_kill_wound2010=kw_past2010[(kw_past2010['nkill']>=1800)]
kwp_kill_wound2010.plot.barh(stacked=True,figsize=(5,5))
plt.title('Gangs most active after 2010')


# =============================================================================
# As seen in the the number of attacks plot there was a sharp increase in attacks after 2010 
# so after 2010 ISIL is the most active terrorist group followed by Taliban and Boko Haram
# =============================================================================

##cities ranked based on kills and the most active groups after 2010
df_india=modified_df2[modified_df2['country_txt']=='India']
df_india = df_india[df_india['city'] !='Unknown']
df_india2=df_india[df_india['iyear']>=2010]
ind_gp2 = df_india2.groupby(['city','gname']).agg({'nkill':'sum'}).sort_values(by=['nkill'],ascending=True)
ind_gp3=ind_gp2[ind_gp['nkill']>100]
ind_gp3.plot.pie(y='nkill',autopct="%.2f",figsize=(5,5),legend=False);
plt.title('Cities with most number of kills in India and the groups responsible after 2010')

# Count of different types of attack types that occurred in all the regions beyon 2010
yr = df[df['iyear'] >= 2010]
reg_atype = pd.crosstab(yr.region_txt, yr.attacktype1_txt)
reg_atype.head()

pl = reg_atype.plot(kind="line", stacked=False, rot=0)

plt.xticks(rotation=60)
fig=plt.gcf()
fig.set_size_inches(12,5)

pl.legend(title='Attack types', bbox_to_anchor=(1, 1.02), loc='upper left')


# Was there any property damage due to different attack types?
pdmg = pd.crosstab( yr.iyear,yr.region_txt)
# pdmg.head()
pl = pdmg.plot(kind="line", stacked=False, rot=0)

plt.xticks(rotation=60)

fig=plt.gcf()
fig.set_size_inches(18,6)
plt.show()
pl.legend(title='Property Damage', bbox_to_anchor=(1, 1.02), loc='upper left')


ind = modified_df2[modified_df2['country_txt'] == 'India']
ind2 = ind[(ind['iyear'] >= 2010)]
top = pd.DataFrame(ind2['gname'].value_counts().head(20).index.tolist())

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
from PIL import Image

text = " ".join(value for value in top[0].values.astype(str))
print ("There are {} words in the combination of all cells in column imonth.".format(len(text)))

stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400).generate(text)

plt.axis("off")
fig=plt.gcf()
fig.set_size_inches(15,8)

plt.tight_layout(pad=0)
plt.imshow(wordcloud, interpolation='bilinear')
plt.show()


