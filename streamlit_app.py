
"""
Created on Thu Oct 26 23:25:15 2023

@author: idosh
"""
import functions as f
import streamlit as st
import graphs as g

if "center" not in st.session_state:
    layout = "wide"
else:
    layout = "centered" if st.session_state.center else "wide"

st.set_page_config(page_title="שמות בישראל",page_icon="random",layout=layout,initial_sidebar_state="auto")

st.checkbox(
    "האם צופים במובייל?", key="center", value=st.session_state.get("center", False)
)



#set page layout-# Set the text direction right side page
st.markdown(f"""<style>body {{  direction: rtl;}}</style>""", unsafe_allow_html=True)
#remove the hemburger mark
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#get the data as st.chach
data=f.get_data("Names File.xlsx")
sector,names,years=f.data_identifiers(data)

st.header("שמות בישראל מ 1948 עד 2021")
title='''
מה השם הנפוץ בישראל?  
   מתי נולדו הכי הרבה ילדים עם השם שלי?  
המידע נלקח מהאתר של הלשכה המרכזית לסטטיסטקה- שרושמת כמה תינוקות נולדו בכל שם כל שנה (חוץ משמות עם פחות מ 5 לידות בשנה)


'''
st.markdown(title)

st.divider()



if "center" not in st.session_state:
    # decleration of the slidbar
    with st.sidebar:   
        st.header("מה השם?")
        st.markdown('''
                    יש לבחור שם להשוואה.  השם יעודכן בגרף משמאל ויציג כמה ילדים נולדו בשם כל שנה  
                    כמו כן אם יש לנו פירוש שם השם- תוכלו למצוא אותו למטה:tulip:
                    ''')
        selected_name=st.selectbox("יש לבחור שם",names,index=290)
        max_born, max_born_year=f.max_born_at_year(selected_name, data)
        # Display formatted text
        st.metric(f"השנה בה נולדו הכי הרבה {selected_name}", max_born_year)
        st.metric("מספר התינוקות שנולדו בשנה זו בשם זה",max_born)
        with st.expander(f"פירוש השם {selected_name}:"):
            st.markdown(f.name_description(selected_name))

    col1 ,col2=st.columns(2,gap="medium")
    with col1:
        name_list = st.multiselect('בחר שמות להשוואה על ציר הזמן',names,selected_name)
        st.subheader(f"כמות התינוקות שנולדו לאורך השנים")
        st.plotly_chart(g.name_by_year(data, name_list),use_container_width=True)
                

        
    with col2:
        col11,col22,col33=st.columns(3)
        year=col11.selectbox("בחר שנה",years,index=years.index(max_born_year))
        N_names=col22.number_input(label="כמה שמות להראות?",min_value=0,max_value=60,value=10)
        col33.markdown("#")
        show_sector=col33.checkbox('להראות חלוקה לפי מגזר?')
        st.subheader(f"השמות הכי נפוצים לשנת {year}")
        st.plotly_chart(g.treemap_names(data=data,year= year,N_names= N_names,sector=show_sector),use_container_width=True)
     

    #st.plotly_chart(g.pichart_name_by_sector(data=data,name=selected_name),use_container_width=True)
else:


    st.header("מה השם?")
    st.markdown('''
                    יש לבחור שם להשוואה.  השם יעודכן בגרף משמאל ויציג כמה ילדים נולדו בשם כל שנ                    כמו כן אם יש לנו פירוש שם השם- תוכלו למצוא אותו למטה:tulip:
                ''')
    selected_name=st.selectbox("יש לבחור שם",names,index=290)
    max_born, max_born_year=f.max_born_at_year(selected_name, data)
    # Display formatted text
    st.metric(f"השנה בה נולדו הכי הרבה {selected_name}", max_born_year)
    st.metric("מספר התינוקות שנולדו בשנה זו בשם זה",max_born)
    with st.expander(f"פירוש השם {selected_name}:"):
        st.markdown(f.name_description(selected_name))

    col1 ,col2=st.columns(2,gap="medium")
    with col1:
        name_list = st.multiselect('בחר שמות להשוואה על ציר הזמן',names,selected_name)
        st.subheader(f"כמות התינוקות שנולדו לאורך השנים")
        st.plotly_chart(g.name_by_year(data, name_list),use_container_width=True)
                

        
    with col2:
        col11,col22,col33=st.columns(3)
        year=col11.selectbox("בחר שנה",years,index=years.index(max_born_year))
        N_names=col22.number_input(label="כמה שמות להראות?",min_value=0,max_value=60,value=10)
        col33.markdown("#")
        show_sector=col33.checkbox('להראות חלוקה לפי מגזר?')
        st.subheader(f"השמות הכי נפוצים לשנת {year}")
        st.plotly_chart(g.treemap_names(data=data,year= year,N_names= N_names,sector=show_sector),use_container_width=True)
     


