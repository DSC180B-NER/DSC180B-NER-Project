#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[15]:


import re
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import hist

def split_into_sentences(text):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])" 
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "i.e." in text: text = text.replace("i.e.","i<prd>e<prd>")
    if "e.g." in text:text = text.replace("e.g.","e<prd>g<prd>")
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


# In[ ]:





# In[ ]:





# In[ ]:





# In[16]:


def draw_hist(outdir,pd_series,name,bins_type):
    Q1=pd_series.quantile(.25)
    Q3=pd_series.quantile(.75)
    IQR=1.5*(Q3-Q1)
    ax = plt.gca()
    hist(pd_series[pd_series.between(Q1-IQR, Q3+IQR)],bins=bins_type,ax=ax, density=True)
    ax.grid(color='grey', alpha=0.5, linestyle='solid')
    plt.savefig(os.path.join(outdir, name))


# In[17]:


def word_cloud(outdir,df):
    sw = stopwords.words("english")
    sw.extend(['said','mr','u','would','could'])
    for i in range(5):
        text =df.summary.iloc[i]
        wordcloud  = WordCloud(width = 400, height = 400, 
                        background_color ='white', 
                        stopwords = sw,
                        collocations = False,

                        min_font_size = 10).generate(text.lower()) 
        plt.figure(figsize = (4,4), facecolor = None) 
        plt.title(df_by_type.index[i])

        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        plt.savefig(os.path.join(outdir, df_by_type.index[i]+'.png'))

        plt.show() 


# In[18]:


def generate_stats(outdir,**kwargs):
    os.makedirs(outdir, exist_ok=True)
    parent_dir=os.getcwd()
    df=pd.read_csv('all_data.csv')
    hist_1=parent_dir+kwargs['barh_doc']
    df.type_code.value_counts().plot.barh()
    plt.savefig(os.path.join(hist_1, 'barh_doc'))
    summary_series=df.summary.apply(lambda x:len(x.split()))
    hist_2=parent_dir+kwargs['hist_doc_words']
    draw_hist(hist_2,summary_series,'hist_doc_words','freedman')
    df=df.rename(columns={'Unnamed: 0': 'doc'})
    df['summary_sentences']=df.summary.apply(lambda x:split_into_sentences(x))
    df_summary_sentences=df.summary_sentences.explode().reset_index().rename(columns={'index': 'doc'})
    df_summary_sentences=df_summary_sentences.merge(df[['doc','type_code']], on="doc", how = 'left')
    hist_3=parent_dir+kwargs['hist_sentence_doc']
    draw_hist(hist_2,df.summary_sentences.explode().apply(lambda x: len(x)),'hist_sentence_doc','freedman')
    df_by_type=df[['summary','type']].groupby('type').agg({'summary': ' '.join})
    wc=parent_dir+kwargs['wc']

    word_cloud(wc,df_by_type)


# In[ ]:





# In[ ]:




