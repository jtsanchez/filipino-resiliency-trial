import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
#add in libraries
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

sns.set()


def load_data():
    # Load the data
    data = pd.read_csv(
        "micro_world.csv",
        encoding='ISO-8859-1'
    )
    return data


def introduction():
    # Write the title and the subheader
    st.title("Financial Resiliency: Assessing Filipino’s preparedness"
    )
    st.subheader(
        """
        Rex | Gian | Pau 
        mentor: Tim
        """
    )
    st.subheader(
        """
        In today's uncertain and unpredictable world, it is more important than ever to assess our financial resiliency and preparedness in the face of emergencies.
        In this study, we aim to:
        1. Look at the financial preparedness of Filipinos.
        2. Explore Filipino's current state of readiness to handle unexpected financial emergencies.
        3. Explore the current state of readiness of Filipinos for their future.
        """
    )

    # Load photo
    st.image("streamlit-photo-1.jpeg")

    # Load data
    data = load_data()

    philippine_data = data[
        data['regionwb'] == 'East Asia & Pacific (excluding high income)'
        ]

    # Display data
    st.markdown("**The Data**")
    st.dataframe(philippine_data)
    st.markdown("Source: Global Findex 2021 from World Bank.")

def general():
    # Write the title and the subheader
    st.title("The Philippines has high % population with savings compared to neighboring countries.")

    #Insert graph on TOP EA&P countries in terms of %savings 
    data = load_data()
    dataeap = data[
        data['regionwb'] == 'East Asia & Pacific (excluding high income)'
        ]
    dataeap['has_saved'] = dataeap['saved'].apply(
    lambda x: 1 if x == 1 else 0)
    
    st.markdown(
        "In this case, savings generally means that respondents have saved or set aside money in the past year, whether using an account at a financial institution, mobile money account, savings club or for any reason. "
    )
    # Partition the page into 2
    col1, col2 = st.columns(2)


    # Display metric in column 1
    col1.metric(
        label='Filipinos with savings',
        value=str('64.50%')
    )

    # Display metric in column 1
    col2.metric(
        value=str('Rank 1'), label='versus neighboring countries in the Low Middle income group of East Asia & Pacific Region'
        )


    # Group the data and apply aggregations
    grouped_data = dataeap.groupby(['economy', 'economycode', 'regionwb']).agg(total_saved=('saved', 'sum'),total_population=('wpid_random', 'count')).reset_index()
    # Compute debit card ownership in %
    grouped_data['% of population saved'] = grouped_data['total_saved']*100.0/grouped_data['total_population']
    #Top EA&P countries in terms of % people with savings
    top_10 = grouped_data.sort_values('% of population saved', ascending=False).head(10).reset_index(drop=True)
    sns.set(font_scale=2)
    fig, ax = plt.subplots(figsize=(10, 6))
    cols = ['#036791' if (y == 'Philippines') else '#adbdc4' for y in top_10.economy]
    sns.barplot(x="% of population saved", y="economy", data=top_10, palette=cols, ax=ax, orient='h').set(title='Top EA&P countries in terms of % people with savings')
    st.pyplot(fig)
   
    st.subheader(
        """.....but are we really doing great?"""
        )

    st.markdown(
        "Below is the graph that shows the disparity among the income classes."
    )

    #create function
    def income_group(row):
        if row['inc_q']==1:
            return 'Poorest'
        elif row['inc_q']==2:
            return 'Poor'
        elif row['inc_q']==3:
            return 'Middle Class'
        elif row['inc_q']==4:
            return 'Rich' #borrow from bank/employer/lender
        elif row['inc_q']==5:
            return 'Richest'
        else:
            return 'unknown/no answer'

    data['Income Group'] = data.apply(income_group, axis=1)
    # Fetch Philippine data
    philippine_data = data[
        data['economy'] == 'Philippines'
        ]
    # Group the data and apply aggregations
    grouped_dataph = philippine_data.groupby('Income Group').count()['wpid_random'].to_frame()
    grouped_dataph = philippine_data.groupby(['economy', 'Income Group']).agg(
    total_saved=('saved', 'sum'),
    total_population=('wpid_random', 'count')
    ).reset_index()


    # Compute debit card ownership in %
    grouped_dataph['% of population saved'] = grouped_dataph['total_saved']*100.0/grouped_dataph['total_population']
    grouped_dataph['% of population with no savings'] = 100 - grouped_dataph['% of population saved']
    top_10ph = grouped_dataph.sort_values('% of population with no savings', ascending=False).head(10).reset_index(drop=True)
    sns.set(font_scale=2)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Income Group", y="% of population with no savings", data=top_10ph, ax=ax, orient='v', color='#036791').set(title='Percentage of Filipinos with savings versus without savings')
    st.pyplot(fig)
    
    st.subheader("""Are savings only for the rich?""")

    st.markdown(
        """More than half of low-income Filipinos and almost half of the middle class have no savings. 
    """
    )
    st.markdown(
        """Let us look at another dimension of financial well-being that is the anxiety or worry that people feel about their financial lives. 
    """
    )
    st.title("Filipinos are financially insecure.")

    # INSERT GRAPH 
    


    # Partition the page into 2
    col1, col2 = st.columns(2)
    # Display metric in column 1
    col1.metric(
        label='', value=str('28.50%')
    )
    col1.markdown("""**of Filipinos are very worried about all four financial issues.**""")

    # Display metric in column 1
    col2.metric(
        value=str('Medical Expenses'), label=''
        )
    col2.markdown("**Biggest financial worry of Filipinos**")

    philippine_data = data[
        data['economy'] == 'Philippines'
        ]
    # Group the data and apply aggregations

    def fin_worry(row):
        if row['fin45']==1:
            return 'Old Age'
        elif row['fin45']==2:
            return 'Medical Cost'
        elif row['fin45']==3:
            return 'Monthly Expense or Bills'
        elif row['fin45']==4:
            return 'School or Education Fees'
        else:
            return 'unknown/no answer'

    data['FinancialWorry'] = data.apply(fin_worry, axis=1)
    # Fetch Philippine data
    philippine_data = data[
        data['economy'] == 'Philippines'
        ]
    # Group the data and apply aggregations

    grouped_dataph = philippine_data.groupby(['economy', 'FinancialWorry']).agg(
    total_population=('wpid_random', 'count')
    ).reset_index()
    grouped_dataph['% most worried'] = grouped_dataph['total_population'] / 1000 *100
    grouped_dataph=grouped_dataph.sort_values('% most worried',ascending=False)
    # Compute debit card ownership in %
    sns.set(font_scale=2)
    fig, ax = plt.subplots(figsize=(10, 6))
    cols = ['#036791' if (y == 'Medical Cost') else '#adbdc4' for y in grouped_dataph.FinancialWorry]
    sns.barplot(x="% most worried", y="FinancialWorry", data=grouped_dataph, ax=ax, orient='h', palette=cols)
    st.pyplot(fig)

def emergencies():
    # Write the title
    st.title(
        "Are Filipinos ready with Emergencies?"
    )
    st.subheader(
        """
        **NO**
        The data shows that Filipinos are not financially prepared for emergencies.
        """
    )
    st.markdown(
        "The respondents were asked what their source of funds will be in the event of an emergency. It was found that more Filipinos are **financially dependent on their friends and family** during emergencies, than their own emergency savings."
    )
        
      
    # Load data
    data = load_data()

    #add col for revised emergency funds source

    #create function
    def emergency_n(row):
        if row['fin24']==1:
            return 'savings'
        elif row['fin24']==2:
            return 'friends/family'
        elif row['fin24']==3:
            return 'work'
        elif row['fin24']==4:
            return 'loan' #borrow from bank/employer/lender
        elif row['fin24']==5:
            return 'sale of assets'
        elif row['fin24']==6:
            return 'other'
        elif row['fin24']==7:
            return 'no money'
        else:
            return 'unknown/no answer'

    data['emergency_funds_source'] = data.apply(emergency_n, axis=1)
    
    # Fetch Philippine data
    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    # Apply .groupby in data for emergency funds source
    emergency_df=philippine_data.groupby('emergency_funds_source').count()['wpid_random'].to_frame()
    emergency_df['%']=(emergency_df['wpid_random']*100/1000).round(2)
    emergency_df=emergency_df.sort_values('%',ascending=False)
    emergency_df=emergency_df.reset_index()
    emergency_df=emergency_df.rename(columns = {'emergency_funds_source':'Emergency Funds Source','wpid_random':'count'})

    # Plot the data

    #revised to seaborn so removed matplotlib
    #fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    #ax.barh(
    #    emergency_df.index,
    #    emergency_df["%"],
    #    color='tab:orange'
    #)
    #ax.set_xlabel("Emergency Funds Source")
    #ax.set_ylabel("% Population")

    # Show the data
    #st.pyplot(fig)

    #seaborn version

    #st.write(emergency_df)

    #set figsize
    fig, ax = plt.subplots(figsize=(10, 6))

    #create barplot
    sns.set(font_scale=2)
    sns.barplot(x="count", y="Emergency Funds Source", data=emergency_df,
                color="tab:orange", ax=ax, orient='h')       

    #3. personalize axis  
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.set_xlabel("count", fontsize=20)
    ax.set_ylabel("Emergency Funds Source", fontsize=20)
 
    

    # Show the figure
    st.pyplot(fig)



    st.markdown(
        "Furthermore, a **large majority** of Filipinos find it difficult to come up with emergency funds"
    )



    # Partition the page into 2
    col1, col2 = st.columns(2)


    # Display metric in column 1
    col1.metric(
        label='% with difficulty in getting emergency funds within 30 days',
        value=str('79.6%')
    )

    # Display metric in column 1
    col2.metric(
        label='% with difficulty in getting emergency funds within 7 days',
        value=str('84.9%')
    )

    
  
    # Difficulty in coming up with emergency funds within 30 days = fin24a

    difficulty_30 = philippine_data.groupby(['fin24a'],dropna = False).agg(count = ('wpid_random','count'))

    difficulty_30['percentage'] = difficulty_30/1000 
    #difficulty_30_indices = ['Very Difficult', 'Somewhat Difficult', 'No Dificulty', 'Missing Data']
    difficulty_30_indices = ['Very Difficult', 'Difficult', 'Not Difficult', 'Missing Data']

    difficulty_30.index = difficulty_30_indices
    difficulty_30.append(difficulty_30.sum().rename('Total')).style.format({'percentage': '{:.2%}'})

    #st.write(difficulty_30)

    #30 days pie chart- comment since will use donut

    #fig2 = px.pie(difficulty_30, values='count', names=difficulty_30.index, title='Difficulty in coming up with emergency funds within 30 days',
    #            color_discrete_sequence=[
    #                px.colors.qualitative.Prism[7],px.colors.qualitative.Prism[6], px.colors.qualitative.Prism[3], px.colors.qualitative.Prism[10]])
    #fig2.update_layout(width=600, height=300, margin=dict(l=200, r=200, t=50, b=50), showlegend=False)
    #fig2.update_traces(textinfo='percent+label')

    #st.plotly_chart(fig2)

 

    # Difficulty in coming up with emergency funds within 7 days = fin24b
    difficulty_7 = philippine_data.groupby(['fin24b'],dropna = False).agg(count = ('wpid_random','count'))
    difficulty_7['percentage'] = difficulty_7/1000
    #difficulty_7_indices = ['Very Difficult', 'Somewhat Difficult', 'No Dificulty', 'Missing Data']
    difficulty_7_indices = ['Very Difficult', 'Difficult', 'Not Difficult', 'Missing Data']
    difficulty_7.index = difficulty_7_indices
    difficulty_7.append(difficulty_7.sum().rename('Total')).style.format({'percentage': '{:.2%}'})

    #7 days pie chart- comment since will use donut

    #fig3 = px.pie(difficulty_7, values='count', names=difficulty_7.index, title='Difficulty in coming up with emergency funds within 7 days',
    #        
    #        color_discrete_sequence=[
    #             px.colors.qualitative.Prism[7],px.colors.qualitative.Prism[6], px.colors.qualitative.Prism[3], px.colors.qualitative.Prism[10]])
    #fig3.update_layout(width=600, height=300, margin=dict(l=200, r=200, t=50, b=50), showlegend=False)
    #fig3.update_traces(textinfo='percent+label')

    #st.plotly_chart(fig3)



    ###try to improve- plotly coz no seaborn for pie chart

    labels = difficulty_30.index
    #map colors
    #label_color = {'Very Difficult':'red', 'Somewhat Difficult':'orange', 'No Difficulty':'green','Missing Data':'grey'}
    label_color = {'Very Difficult':'red', 'Difficult':'orange', 'Not Difficult':'green','Missing Data':'grey'}

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=(difficulty_30['percentage']*100).round(2), name="DIFFICULTY", marker_colors=difficulty_30.index.map(label_color)),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=(difficulty_7['percentage']*100).round(2), name="DIFFICULTY", marker_colors=difficulty_7.index.map(label_color)),
                1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.5, hoverinfo="label+percent+name", textinfo='percent+label')

    fig.update_layout(
        title_text="Difficulty in Preparing Emergency Funds within Given Period",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='within 30 days', x=0.14, y=0.5, font_size=20, showarrow=False),
                    dict(text='within 7 days', x=.85, y=0.5, font_size=20, showarrow=False)],
        width=900, height=500, showlegend=False)
    #fig.show()

    st.markdown(
        "Filipinos that find it **very difficult** to get emergency funds increases by 13.7% as the timeline is shorten from 30 to 7 days"
       
    )

    st.plotly_chart(fig)

    ###end trial


    

    





def future():
    
    # Write the title
    st.title(
        "Are Filipinos ready for their Future?"
    )
    st.subheader(
        """
        **NO**
        According to recent survey data, the **majority of Filipinos (58.4%) were not able to save for old age** in the 12 months prior to the survey.
        """
    )       
      
    # Load data
    data = load_data()

    # extract Philippine data
    philippine_data = data[
        data['economy'] == 'Philippines'
        ]

    # Saved for old age = fin16
    # Yes, means saved in the past year(past 12 months, according to the survey questinnaire, not previous year)

    # groupy by those who saved vs those who didn't
    saved_for_old_age = philippine_data.groupby(['fin16']).agg(count = ('wpid_random','count'))

    # add percentage column
    saved_for_old_age['percentage'] = saved_for_old_age/len(philippine_data)

    # Change indices to be more meaning full
    saved_for_old_age_indices = ['Yes', 'No']
    saved_for_old_age.index = saved_for_old_age_indices

    labels = saved_for_old_age.index

    #tab20c = plt.get_cmap('tab20c')
    tab10_colors = sns.color_palette('tab10', 8).as_hex()
    tab_orange = tab10_colors[1]
    tab_gray = tab10_colors[7]

    label_color = {'Yes': tab_orange,'No': tab_gray}
    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=1,specs=[[{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=(saved_for_old_age['percentage']*100).round(2), name="SAVED?", marker_colors=labels.map(label_color)))

    fig.update_traces(title='Saved or set aside any money for old age in the past year',
                      hoverinfo="label+percent+name", textinfo='percent+label'
    )
    

    fig.update_layout(height=300, showlegend=False, font=dict(size=18), margin=dict(l=20, r=20, t=20, b=20))

    st.plotly_chart(fig)
    ##################################################

    st.markdown(
        """
        While this figure may seem discouraging, it is worth noting that a significant portion of the population was able to save for old age, especially when compared to several other countries in the East Asia & Pacific (excluding high income) region, such as Cambodia (8.8%), Mongolia (16.8%), Lao PDR (25.7%), Indonesia (27.7%), and Myanmar (32.7%), where less than a third of the population saved for old age, the percentage of savers in the Philippines (41.6%) is relatively high. In terms of those who saved in the past year, **the Philippines still ranked third in the region**, behind Malaysia (54.8%) and Thailand (55.6%), which had higher percentages.
        """
    )

    fin16 = data.query('regionwb == \'East Asia & Pacific (excluding high income)\'').groupby(['economy', 'fin16']).size().unstack(fill_value=0)
    fin16['yes_percentage'] = fin16[1]/(fin16[1]+fin16[2])*100
    fin16.sort_values('yes_percentage', ascending = False, inplace=True)

    #set figsize
    #create barplot

    fig2, ax =  plt.subplots(figsize=(10,6))
  
    # Run bar plot
    sns.barplot(x='yes_percentage',y = fin16.index, data=fin16,
                color='tab:orange', ax=ax, orient='h')       
    # Set title
    #ax.set_title('Top EA&P Countries who saved or set aside money for old age in the past year')

      #3. personalize axis  
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xlabel("% Population", fontsize=17)
    ax.set_ylabel("Countries", fontsize=17)
    ax.set_xlim(0, 60)
    # Show the data
    st.pyplot(fig2)

    #########################
    st.markdown(
        """
        Less than 30% of low-income Filipinos have saved for Old Age in the past year. Even among the rich, less than half of them saved. **Only the richest group had a majority of individuals who saved in the past year.**
        """
    )

    income_mapping = {1: 'poorest', 2: 'poor', 3:'middle class', 4: 'rich', 5: 'richest'}
    philippine_data['income'] = philippine_data[['inc_q']].replace({'inc_q':income_mapping})
    fin16_ph_income = philippine_data.groupby(['income', 'fin16']).size().unstack(fill_value=0)
    fin16_ph_income['yes_percentage'] = fin16_ph_income[1]/(fin16_ph_income[1]+fin16_ph_income[2])*100
    fin16_ph_income.sort_values('yes_percentage', ascending = True, inplace=True)

    # Set figure size
    fig3, ax2 = plt.subplots(figsize=(10,6))
    #cm = plt.get_cmap('tab20c')

    # Run bar plot
    sns.barplot(x=fin16_ph_income.index, y = 'yes_percentage', data=fin16_ph_income,
                color='tab:orange', ax=ax2)    
    # Set labels
    ax2.tick_params(axis='x', labelsize=15)
    ax2.tick_params(axis='y', labelsize=15)
    ax2.set_xlabel('Quintile',fontsize=17)
    ax2.set_ylabel('% who saved in past year',fontsize=17)
    ax2.set_ylim(0, 100)

    # Show figure
    st.pyplot(fig3) 

def why_no_savings():
    st.title("What Hinders Us From Saving?")

    st.subheader(
        """
        The top reason for absence of savings is **lack of money**, Followed by **expensive fees** of maintaining a savings account.
        """
    )
    st.markdown(
        "Although there are other reasons such as difficulty in location and documentation, the evident financial reasons are the main hindrance of Filipinos in saving money."
    )

     # Load data
    data = load_data()

    #add column for why no savings

    #1. too far
    too_far = (data['fin11a']==1) | (data['fin13_1a']==1) | (data['fin10_1a']==1)
    
    data['too far'] = np.where(too_far, 1 ,0)

    #2. no need / no need for financial services
    no_need = (data['fin11h'] == 1) | (data['fin10_1b'] == 1)

    data['no need'] = np.where(no_need, 1, 0)

    #3. lack money
    lack_money=(data['fin11f']==1) | (data['fin10_1c']==1) | (data['fin13_1d']==1)

    data['lack money'] = np.where(lack_money, 1, 0)
        
    #4.not comfortable
    not_comfy=(data['fin10_1d']==1)

    data['not comfortable'] = np.where(not_comfy, 1, 0)
        
    #5. lack trust
    lack_trust = (data['fin11d']==1) |(data['fin10_1e']==1)
    data['lack trust'] = np.where(lack_trust, 1, 0)

    #6. too expensive
    too_expensive = (data['fin11b']==1) |(data['fin13_1b']==1)
    data['too expensive'] = np.where(too_expensive, 1, 0)

    #7. lack documentation
    lack_docu = (data['fin11c']==1) |(data['fin13_1c']==1)
    data['lack documentation'] = np.where(lack_docu, 1, 0)

    #8. religious reasons
    religion = (data['fin11e']==1) |(data['fin13_1c']==1)
    data['religious reasons'] = np.where(religion, 1, 0)

    #9. family member already has one
    fam=(data['fin11g']==1) |(data['fin13_1c']==1)
    data['family already has'] = np.where(fam, 1, 0)

    #10. use agent
    use_agent=(data['fin13_1e']==1)
    data['use agent'] = np.where(use_agent, 1, 0)

    #11. no phone
    no_phone=(data['fin13_1f']==1)
    data['no mobile phone'] = np.where(no_phone, 1, 0)
 

    #df for PH data
    philippine_data=data[data['economy']=='Philippines']

    #df for PH without savings
    PH_nosavings=philippine_data[philippine_data['saved']==0]

    #make df of reasons for no savings
    reasons=PH_nosavings[['too far','no need','lack money','not comfortable','lack trust','too expensive','lack documentation','religious reasons','family already has','use agent','no mobile phone']].sum()
    reasons=reasons.to_frame().reset_index()
    reasons=reasons.rename(columns = {'index':'reasons for no savings',0:'count'})
    
    #add % column
    reasons['%']=(reasons['count']*100/reasons['count'].sum()).round(2)
    reasons.sort_values(by="%", inplace=True, ascending=False)
    reasons=reasons[reasons['count']!=0] #remove no data to clean
    #st.write(reasons)

    #1. make a graph slate set figsize
    fig, ax = plt.subplots(figsize=(10, 6)) #fig used to call "picture", ax to modify properties

    #2. create barplot
    sns.barplot(x="count", y="reasons for no savings", data=reasons,
                color="tab:orange", ax=ax, orient='h')

    #3. personalize axis  
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xlabel("count", fontsize=17)
    ax.set_ylabel("reasons for no savings", fontsize=17)

    # Show the figure
    st.pyplot(fig)




def summary():
    # Write the title
    st.title(
        "SUMMARY"
    )
    st.subheader(
        """
        **GENERAL CONCLUSION:** Filipinos are ready with short term savings but not for emergencies and old age.
        """
    )
    #st.markdown(
    #    """
    #    :flag-ph: Majority of Filipinos (64.5%) have savings; Ranks 4th in East Asia & Pacific region and 1st for lower middle income group in EA&P.
    #
    #    :moneybag: Majority of Filipinos with savings come from high-income households. More than half of low-income Filipinos and almost half of the middle class have no savings
    #
    #    :female-doctor: Medical expenses cause the biggest financial worry among Filipinos

    #    :family: More Filipinos will go to their families and friends than their own savings when there’s an emergency

    #    :older_man: Less than half (41.6%) of Filipinos have set aside money for long-term/Old Age since the past year 

    #    :money_with_wings: Lack of money and expensive bank fees are the top reasons that hinder Filipinos from saving.

        
    #    """
    #)


    # Partition the page into 2
    col1, col2 = st.columns(2)


    # Display text in column 1
    col1.markdown("""
    :flag-ph: \n 
    Majority of Filipinos (64.5%) have savings; Ranks 4th in East Asia & Pacific region and 1st for lower middle income group in EA&P. \n\n
    :female-doctor: \n
    Medical expenses cause the biggest financial worry among Filipinos \n
    :older_man: \n
    Less than half (41.6%) of Filipinos have set aside money for long-term/old Age since the past year """)

 

    # Display text in column 2
    col2.markdown("""
    :moneybag: \n
    Most Filipinos with savings come from high-income households. Majority of low-income Filipinos and almost half of the middle class have no savings \n
    :family: \n
    More Filipinos will go to their families and friends than their own savings when there’s an emergency \n
    :money_with_wings: \n
    Lack of money and expensive bank fees are the top reasons that hinder Filipinos from saving.
    
    """)




    st.subheader(
        """
        **RECOMMENDATION:** Implement rules and regulations that promote and support financial preparedness among Filipinos
        """
    )
    st.markdown(
        """
        :heavy_check_mark: Government support on emergency funds for Filipinos

        :heavy_check_mark: Improve government support on medical expenses

        :heavy_check_mark: Regulations to lessen/remove bank fees for people incapable of maintaining the default amount
        
    
        **Recommendations on further analysis:** 
        :bar_chart:  Survey improvements- data with equal distribution per income quintile for more representative findings
        """ 
    )


    


list_of_pages = [
    "Financial Resiliency: Assessing Filipino’s preparedness",
    "General",
    "Are Filipinos ready with Emergencies?",
    "Are Filipinos ready for their Future?",
    "What hinders us from saving?",
    "SUMMARY"
]

st.sidebar.title(':scroll: Main Pages')
selection = st.sidebar.radio("Go to: ", list_of_pages)

if selection == "Financial Resiliency: Assessing Filipino’s preparedness":
    introduction()

elif selection == "General":
    general()

elif selection == "Are Filipinos ready with Emergencies?":
    emergencies()

elif selection == "Are Filipinos ready for their Future?":
    future()

elif selection == "What hinders us from saving?":
    why_no_savings()

elif selection == "SUMMARY":
    summary()