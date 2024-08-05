# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 19:34:51 2021
@author: Sathish
"""
import streamlit as st
import numpy as np
import pandas as pd
import warnings
import os
from mplsoccer import PyPizza, add_image, FontManager
from PIL import Image
import matplotlib.pyplot as plt
import snowflake.connector
from soccerplots.radar_chart import Radar
from matplotlib.font_manager import FontProperties


def connect(option1):

    df = pd.read_csv("Fully Cleaned FM Data.csv")

    return df
        
  
def dataprep(option1):
    data=connect(option1)

    
    league = data['Division'].tolist()
    league = np.array(league)
    league = np.unique(league)
    pos =  [
    "Centre Back",
    "Midfielder",
    "Attacking Midfielder",
    "Goalkeeper",
    "Defensive Midfielder",
    "Striker",
    "Fullback","Winger"]
    Club = data['Club'].tolist()
    Club = np.array(Club)
    Club = np.unique(Club)


    Pizzaapp(data,league,pos,Club)

def Pizzaapp(data,league,pos,Club):
    st.title("Pizza plots")
    st.markdown("Choose appropriate filters from the menu bar on your left hand side. Click **'Generate pizza plot'** to generate plots.")
            
    
    
    singlepizza(data,league,pos,Club)
        
    if st.sidebar.button('Sign out'):
        st.session_state['PageFour'] = False
        st.session_state['valid_user'] = False
        st.experimental_rerun()


def mental(data,col1,label,value):
    label1 = label
    attacking = value
    slice_colors =  [st.session_state['h1']] * 5+ [st.session_state['h2']] * 5 + [st.session_state['h3']] * 5
    text_colors = ["#000000"] * 15

    min_range = [0] * 15
    max_range = [20] * 15

# instantiate PyPizza class
    baker = PyPizza(
        params=label1,
        min_range = min_range,
        max_range=max_range,
        background_color=st.session_state['bg'],     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=1,               # linewidth of last circle
        other_circle_lw=1,              # linewidth for other circles
        inner_circle_size=18,             # linewidth for other circles
        other_circle_ls="-."            # linestyle for other circles
          # size of inner circle
        )
# plot pizza
    fig, ax = baker.make_pizza(
        attacking,                          # list of values
        figsize=(8, 8.5),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
        edgecolor="#000000", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11,
            fontproperties=st.session_state['font_normal1'], va="center"
    ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
        color="#F2F2F2", fontsize=11,
        fontproperties=st.session_state['font_normal1'], zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values labels
)
    #data.reset_index(inplace = True)
    #titlename = data['Player'][0]
    #teamname = data['Team'][0]
    titlename = data['Name'][0]
    teamname = data['Club'][0]
    #position = data['Categorical position'][0]
    #mp = data['Minutes played'][0]
    age = data['Age'][0]
    age = int(float(age))
    league = data['Division'][0]




    title = titlename + " | " + str(age) + "-years-old"
    subtitle = 'Player Key Attributes'
    subtitle2 = titlename + " plays for " + teamname + " in " + league


    fig.text(
    0.515, 0.005, subtitle2, size=10,
    fontproperties=st.session_state['font_normal1'], color="#F2F2F2",
    ha="center"
)



# add title
    fig.text(
        0.515, 0.975, title, size=19,
        ha="center", fontproperties=st.session_state['font_normal2'], color="#F2F2F2"
        )
    fig.text(
    0.515, 0.938,
    subtitle,
    size=16,
    ha="center", fontproperties=st.session_state['font_normal2'], color="#F2F2F2"
)





    if st.session_state['template'] == 'TFA':
        fdj_cropped = Image.open('Logo.png')
        ax_image = add_image(
        fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127)
    elif st.session_state['template'] == 'SS':
        fdj_cropped = Image.open('smartscout.png')
        ax_image = add_image(
        fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127)
    elif st.session_state['template'] == 'Minnesota':
        fdj_cropped = Image.open('logo3.png')
        ax_image = add_image(fdj_cropped, fig, left=0.4598, bottom=0.4450, width=0.10, height=0.095)
    elif st.session_state['template'] == 'Avid':
        fdj_cropped = Image.open('avid.png')
        ax_image = add_image(fdj_cropped, fig, left=0.4598, bottom=0.4450, width=0.10, height=0.095)
    elif st.session_state['template'] == 'Game Changer FA':
        fdj_cropped = Image.open('gcfc.png')
        ax_image = add_image(fdj_cropped, fig, left=0.4598, bottom=0.4450, width=0.10, height=0.095)
    elif st.session_state['template'] == 'Virtual Scout':
        fdj_cropped = Image.open('Virtual-Scout-White.png')
        ax_image = add_image(
        fdj_cropped, fig, left=0.4578, bottom=0.4315, width=0.11, height=0.127)

    #ax_image = add_image(
    #fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127)
    # add text
    fig.text(
    0.34, 0.0285, "Technical        Mental        Physical", size=14,
    fontproperties=st.session_state['font_normal1'], color="#FFFFFF"
)
# add rectangles
    fig.patches.extend([
    plt.Rectangle(
        (0.31, 0.0285), 0.025, 0.021, fill=True, color=st.session_state['h1'],
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.462, 0.0285), 0.025, 0.021, fill=True, color=st.session_state['h2'],
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.582, 0.0285), 0.025, 0.021, fill=True, color=st.session_state['h3'],
        transform=fig.transFigure, figure=fig
    ),
])

    st.pyplot(fig)


#generate_radar(final_df,2,st.session_state['bg'],st.session_state['bg2'],"#FFFFFF","#FFFFFF",st.session_state['R1'],st.session_state['R2'])
def genradar(data,col1,label,value1,value2):
    radar = Radar(background_color=st.session_state['bg'], patch_color=st.session_state['bg2'], label_color="#FFFFFF",range_color="#FFFFFF")
    label = label
    value1 = value1
    pos = data['Position'][0]
    value2 =  value2


    attacking = [value1,value2]


    titlename = data['Name'][0]
    teamname = data['Club'][0]
    titlename2 = pos + ' Average'
    teamname2 = data['Division'][0]

    title = dict(
                title_name=titlename,
                title_color=st.session_state['R1'],
                subtitle_name=teamname,
                subtitle_color='#FFFFFF',
                title_name_2=titlename2,
                title_color_2=st.session_state['R2'],
                subtitle_name_2=teamname2,
                subtitle_color_2='#FFFFFF',
                title_fontsize=18,
                subtitle_fontsize=15,
                )

    ranges1 = [(0, 20)]*15
    attacking, ax = radar.plot_radar(ranges=ranges1,params=label,values=attacking,radar_color=[st.session_state['R1'], st.session_state['R2']],title=title,
                          end_color=st.session_state['bg'],dpi=600,compare=True)

    if st.session_state['template'] == 'TFA':
                    fdj_cropped = Image.open('Logo.png')
                    ax_image = add_image(
                    fdj_cropped, attacking, left=0.5958, bottom=0.0795, width=0.13, height=0.127)
    elif st.session_state['template'] == 'SS':
                    fdj_cropped = Image.open('smartscout.png')
                    ax_image = add_image(
                    fdj_cropped, attacking, left=0.5958, bottom=0.0795, width=0.13, height=0.127)
    elif st.session_state['template'] == 'Minnesota':
                    fdj_cropped = Image.open('logo3.png')
                    ax_image = add_image(fdj_cropped, attacking, left=0.6358, bottom=0.0795, width=0.06, height=0.06)
    elif st.session_state['template'] == 'SISU':
                    fdj_cropped = Image.open('sisu.webp')
                    ax_image = add_image(fdj_cropped, attacking, left=0.6358, bottom=0.0795, width=0.06, height=0.06)
    elif st.session_state['template']=='Avid':
                    fdj_cropped = Image.open('avid.png')
                    ax_image = add_image(fdj_cropped, attacking, left=0.6354, bottom=0.0795, width=0.06, height=0.06)
    elif st.session_state['template'] == 'Game Changer FA':
                    fdj_cropped = Image.open('gcfc.png')
                    ax_image = add_image(fdj_cropped, attacking, left=0.6358, bottom=0.0795, width=0.06, height=0.06)
    elif st.session_state['template'] == 'Virtual Scout':
        fdj_cropped = Image.open('Virtual-Scout-White.png')
        ax_image = add_image(fdj_cropped, attacking, left=0.6258, bottom=0.0795,width=0.06, height=0.06)




                #passing, ax1 = radar.plot_radar(ranges=ranges2,params=label2,values=passing,radar_color=[player1, player2],title=title,
                  #         end_color=bg,dpi=600,compare=True)

                #defending, ax2 = radar.plot_radar(ranges=ranges3,params=label3,values=defending,radar_color=[player1, player2],title=title
                 #          ,end_color=bg,dpi=600,compare=True)

                #st.markdown("<h3 style='text-align: center; color: white;'>Attacking & Shooting</h3>", unsafe_allow_html=True)
    st.pyplot(attacking)

def generatepizza(data,pos,col1,col2,col3,entire_data):
    data.reset_index(inplace=True)
    if pos=='Centre Back':
        label = ['Acceleration','Agility','Balance','Pace','Strength','Aggression','Anticipation','Bravery','Positioning','Determination','Marking','Passing','Tackling','Heading','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Aggression'].values[0], 2), round(data['Anticipation'].values[0], 2),
                             round(data['Bravery'].values[0], 2), round(data['Positioning'].values[0], 2),
                             round(data['Determination'].values[0], 2), round(data['Marking'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Tackling'].values[0], 2),
                              round(data['Heading'].values[0], 2),round(data['Technique'].values[0], 2)]
    elif pos=='Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Decision\nMaking','Vision','Work Rate','Composure','First\nTouch','Passing','Technique','Dribbling','Long Shots']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Decisions'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['Work Rate'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['First Touch'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Technique'].values[0], 2),
                              round(data['Dribbling'].values[0], 2),round(data['Long Shots'].values[0], 2)]
    elif pos=='Attacking Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Anticipation','Flair','Decision\nMaking','Determination','Vision','First\nTouch','Passing','Technique','Dribbling','Finishing']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Flair'].values[0], 2),
                             round(data['Decisions'].values[0], 2), round(data['Determination'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['First Touch'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Technique'].values[0], 2),
                              round(data['Dribbling'].values[0], 2),round(data['Finishing'].values[0], 2)]
    elif pos=='Goalkeeper':
        label = ['Jumping Reach','Agility','Balance','Stamina','Strength','Anticipation','Composure','Concentration','Leadership','Team Work','Aerial\nReach','Communication','Handling','Passing','Reflexes']
        value =  attacking = [round(data['Jumping Reach'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Stamina'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Composure'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Leadership'].values[0], 2),
                             round(data['Team Work'].values[0], 2), round(data['Aerial Ability'].values[0], 2)
                            ,round(data['Communication'].values[0], 2),round(data['Handling'].values[0], 2),
                              round(data['Passing'].values[0], 2),round(data['Reflexes'].values[0], 2)]
    elif pos=='Defensive Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Strength','Composure','Concentration','Determination','Work Rate','Positioning','Marking','Passing','Tackling','Heading','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['Concentration'].values[0], 2),
                             round(data['Determination'].values[0], 2), round(data['Work Rate'].values[0], 2),
                             round(data['Positioning'].values[0], 2), round(data['Marking'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Tackling'].values[0], 2),
                              round(data['Heading'].values[0], 2),round(data['Technique'].values[0], 2)]
    elif pos=='Striker':
        label = ['Acceleration','Agility','Pace','Stamina','Strength','Anticipation','Bravery','Positioning','Decision\nMaking','Flair','Finishing','First\nTouch','Heading','Technique','Penalty\nTaking']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Pace'].values[0], 2),
                             round(data['Stamina'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Bravery'].values[0], 2),
                             round(data['Positioning'].values[0], 2), round(data['Decisions'].values[0], 2),
                             round(data['Flair'].values[0], 2), round(data['Finishing'].values[0], 2)
                            ,round(data['First Touch'].values[0], 2),round(data['Heading'].values[0], 2),
                              round(data['Technique'].values[0], 2),round(data['Penalty Taking'].values[0], 2)]
    elif pos=='Fullback':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Determination','Work Rate','Anticipation','Composure','Crossing','Marking','Passing','Tackling','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Determination'].values[0], 2),
                             round(data['Work Rate'].values[0], 2), round(data['Anticipation'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['Crossing'].values[0], 2)
                            ,round(data['Marking'].values[0], 2),round(data['Passing'].values[0], 2),
                              round(data['Tackling'].values[0], 2),round(data['Technique'].values[0], 2)]
    elif pos=='Winger':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Vision','Off The\nBall','Work Rate','Flair','Bravery','Crossing','Dribbling','Passing','First\nTouch','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['Off The Ball'].values[0], 2),
                             round(data['Work Rate'].values[0], 2), round(data['Flair'].values[0], 2),
                             round(data['Bravery'].values[0], 2), round(data['Crossing'].values[0], 2)
                            ,round(data['Dribbling'].values[0], 2),round(data['Passing'].values[0], 2),
                              round(data['First Touch'].values[0], 2),round(data['Technique'].values[0], 2)]

    mental(data,col1,label[::-1],value[::-1])
    #genradar(data,col1,label[::-1],value[::-1],entire_data)


def generateradar(data,pos,col1,col2,col3,entire_data):
    data.reset_index(inplace=True)
    filter_pos = data['Position'][0]
    entire_data = entire_data[entire_data['Position']==filter_pos]


    if pos=='Centre Back':
        label = ['Acceleration','Agility','Balance','Pace','Strength','Aggression','Anticipation','Bravery','Positioning','Determination','Marking','Passing','Tackling','Heading','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Aggression'].values[0], 2), round(data['Anticipation'].values[0], 2),
                             round(data['Bravery'].values[0], 2), round(data['Positioning'].values[0], 2),
                             round(data['Determination'].values[0], 2), round(data['Marking'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Tackling'].values[0], 2),
                              round(data['Heading'].values[0], 2),round(data['Technique'].values[0], 2)]
        entire_data = entire_data[label]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                              round(average_row['Balance'].values[0], 2),
                             round(average_row['Pace'].values[0], 2), round(average_row['Strength'].values[0], 2),
                             round(average_row['Aggression'].values[0], 2), round(average_row['Anticipation'].values[0], 2),
                             round(average_row['Bravery'].values[0], 2), round(average_row['Positioning'].values[0], 2),
                             round(average_row['Determination'].values[0], 2), round(average_row['Marking'].values[0], 2)
                            ,round(average_row['Passing'].values[0], 2),round(average_row['Tackling'].values[0], 2),
                              round(average_row['Heading'].values[0], 2),round(average_row['Technique'].values[0], 2)]


    elif pos=='Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Decision\nMaking','Vision','Work Rate','Composure','First\nTouch','Passing','Technique','Dribbling','Long Shots']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Decisions'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['Work Rate'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['First Touch'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Technique'].values[0], 2),
                              round(data['Dribbling'].values[0], 2),round(data['Long Shots'].values[0], 2)]

        label2 = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Decisions','Vision','Work Rate','Composure','First Touch','Passing','Technique','Dribbling','Long Shots']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                              round(average_row['Balance'].values[0], 2),
                             round(average_row['Pace'].values[0], 2), round(average_row['Stamina'].values[0], 2),
                             round(average_row['Concentration'].values[0], 2), round(average_row['Decisions'].values[0], 2),
                             round(average_row['Vision'].values[0], 2), round(average_row['Work Rate'].values[0], 2),
                             round(average_row['Composure'].values[0], 2), round(average_row['First Touch'].values[0], 2)
                            ,round(average_row['Passing'].values[0], 2),round(average_row['Technique'].values[0], 2),
                              round(average_row['Dribbling'].values[0], 2),round(average_row['Long Shots'].values[0], 2)]


    elif pos=='Attacking Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Anticipation','Flair','Decision\nMaking','Determination','Vision','First\nTouch','Passing','Technique','Dribbling','Finishing']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Flair'].values[0], 2),
                             round(data['Decisions'].values[0], 2), round(data['Determination'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['First Touch'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Technique'].values[0], 2),
                              round(data['Dribbling'].values[0], 2),round(data['Finishing'].values[0], 2)]

        label2 = ['Acceleration','Agility','Balance','Pace','Stamina','Anticipation','Flair','Decisions','Determination','Vision','First Touch','Passing','Technique','Dribbling','Finishing']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Balance'].values[0], 2),
                     round(average_row['Pace'].values[0], 2), round(average_row['Stamina'].values[0], 2),
                     round(average_row['Anticipation'].values[0], 2), round(average_row['Flair'].values[0], 2),
                     round(average_row['Decisions'].values[0], 2), round(average_row['Determination'].values[0], 2),
                     round(average_row['Vision'].values[0], 2), round(average_row['First Touch'].values[0], 2)
                    ,round(average_row['Passing'].values[0], 2),round(average_row['Technique'].values[0], 2),
                      round(average_row['Dribbling'].values[0], 2),round(average_row['Finishing'].values[0], 2)]


    elif pos=='Goalkeeper':
        label = ['Jumping Reach','Agility','Balance','Stamina','Strength','Anticipation','Composure','Concentration','Leadership','Team Work','Aerial\nReach','Communication','Handling','Passing','Reflexes']
        value =  attacking = [round(data['Jumping Reach'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Stamina'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Composure'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Leadership'].values[0], 2),
                             round(data['Team Work'].values[0], 2), round(data['Aerial Ability'].values[0], 2)
                            ,round(data['Communication'].values[0], 2),round(data['Handling'].values[0], 2),
                              round(data['Passing'].values[0], 2),round(data['Reflexes'].values[0], 2)]
        label2 = ['Jumping Reach','Agility','Balance','Stamina','Strength','Anticipation','Composure','Concentration','Leadership','Team Work','Aerial Ability','Communication','Handling','Passing','Reflexes']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Jumping Reach'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Balance'].values[0], 2),
                     round(average_row['Stamina'].values[0], 2), round(average_row['Strength'].values[0], 2),
                     round(average_row['Anticipation'].values[0], 2), round(average_row['Composure'].values[0], 2),
                     round(average_row['Concentration'].values[0], 2), round(average_row['Leadership'].values[0], 2),
                     round(average_row['Team Work'].values[0], 2), round(average_row['Aerial Ability'].values[0], 2)
                    ,round(average_row['Communication'].values[0], 2),round(average_row['Handling'].values[0], 2),
                      round(average_row['Passing'].values[0], 2),round(average_row['Reflexes'].values[0], 2)]


    elif pos=='Defensive Midfielder':
        label = ['Acceleration','Agility','Balance','Pace','Strength','Composure','Concentration','Determination','Work Rate','Positioning','Marking','Passing','Tackling','Heading','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['Concentration'].values[0], 2),
                             round(data['Determination'].values[0], 2), round(data['Work Rate'].values[0], 2),
                             round(data['Positioning'].values[0], 2), round(data['Marking'].values[0], 2)
                            ,round(data['Passing'].values[0], 2),round(data['Tackling'].values[0], 2),
                              round(data['Heading'].values[0], 2),round(data['Technique'].values[0], 2)]

        label2 = ['Acceleration','Agility','Balance','Pace','Strength','Composure','Concentration','Determination','Work Rate','Positioning','Marking','Passing','Tackling','Heading','Technique']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Balance'].values[0], 2),
                     round(average_row['Pace'].values[0], 2), round(average_row['Strength'].values[0], 2),
                     round(average_row['Composure'].values[0], 2), round(average_row['Concentration'].values[0], 2),
                     round(average_row['Determination'].values[0], 2), round(average_row['Work Rate'].values[0], 2),
                     round(average_row['Positioning'].values[0], 2), round(average_row['Marking'].values[0], 2)
                    ,round(average_row['Passing'].values[0], 2),round(average_row['Tackling'].values[0], 2),
                      round(average_row['Heading'].values[0], 2),round(average_row['Technique'].values[0], 2)]


    elif pos=='Striker':
        label = ['Acceleration','Agility','Pace','Stamina','Strength','Anticipation','Bravery','Positioning','Decision\nMaking','Flair','Finishing','First\nTouch','Heading','Technique','Penalty\nTaking']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Pace'].values[0], 2),
                             round(data['Stamina'].values[0], 2), round(data['Strength'].values[0], 2),
                             round(data['Anticipation'].values[0], 2), round(data['Bravery'].values[0], 2),
                             round(data['Positioning'].values[0], 2), round(data['Decisions'].values[0], 2),
                             round(data['Flair'].values[0], 2), round(data['Finishing'].values[0], 2)
                            ,round(data['First Touch'].values[0], 2),round(data['Heading'].values[0], 2),
                              round(data['Technique'].values[0], 2),round(data['Penalty Taking'].values[0], 2)]

        label2 = ['Acceleration','Agility','Pace','Stamina','Strength','Anticipation','Bravery','Positioning','Decisions','Flair','Finishing','First Touch','Heading','Technique','Penalty Taking']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Pace'].values[0], 2),
                     round(average_row['Stamina'].values[0], 2), round(average_row['Strength'].values[0], 2),
                     round(average_row['Anticipation'].values[0], 2), round(average_row['Bravery'].values[0], 2),
                     round(average_row['Positioning'].values[0], 2), round(average_row['Decisions'].values[0], 2),
                     round(average_row['Flair'].values[0], 2), round(average_row['Finishing'].values[0], 2)
                    ,round(average_row['First Touch'].values[0], 2),round(average_row['Heading'].values[0], 2),
                      round(average_row['Technique'].values[0], 2),round(average_row['Penalty Taking'].values[0], 2)]


    elif pos=='Fullback':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Determination','Work Rate','Anticipation','Composure','Crossing','Marking','Passing','Tackling','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Concentration'].values[0], 2), round(data['Determination'].values[0], 2),
                             round(data['Work Rate'].values[0], 2), round(data['Anticipation'].values[0], 2),
                             round(data['Composure'].values[0], 2), round(data['Crossing'].values[0], 2)
                            ,round(data['Marking'].values[0], 2),round(data['Passing'].values[0], 2),
                              round(data['Tackling'].values[0], 2),round(data['Technique'].values[0], 2)]

        label2 = ['Acceleration','Agility','Balance','Pace','Stamina','Concentration','Determination','Work Rate','Anticipation','Composure','Crossing','Marking','Passing','Tackling','Technique']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Balance'].values[0], 2),
                     round(average_row['Pace'].values[0], 2), round(average_row['Stamina'].values[0], 2),
                     round(average_row['Concentration'].values[0], 2), round(average_row['Determination'].values[0], 2),
                     round(average_row['Work Rate'].values[0], 2), round(average_row['Anticipation'].values[0], 2),
                     round(average_row['Composure'].values[0], 2), round(average_row['Crossing'].values[0], 2)
                    ,round(average_row['Marking'].values[0], 2),round(average_row['Passing'].values[0], 2),
                      round(average_row['Tackling'].values[0], 2),round(average_row['Technique'].values[0], 2)]

    elif pos=='Winger':
        label = ['Acceleration','Agility','Balance','Pace','Stamina','Vision','Off The\nBall','Work Rate','Flair','Bravery','Crossing','Dribbling','Passing','First\nTouch','Technique']
        value =  attacking = [round(data['Acceleration'].values[0], 2), round(data['Agility'].values[0], 2),
                              round(data['Balance'].values[0], 2),
                             round(data['Pace'].values[0], 2), round(data['Stamina'].values[0], 2),
                             round(data['Vision'].values[0], 2), round(data['Off The Ball'].values[0], 2),
                             round(data['Work Rate'].values[0], 2), round(data['Flair'].values[0], 2),
                             round(data['Bravery'].values[0], 2), round(data['Crossing'].values[0], 2)
                            ,round(data['Dribbling'].values[0], 2),round(data['Passing'].values[0], 2),
                              round(data['First Touch'].values[0], 2),round(data['Technique'].values[0], 2)]

        label2 = ['Acceleration','Agility','Balance','Pace','Stamina','Vision','Off The Ball','Work Rate','Flair','Bravery','Crossing','Dribbling','Passing','First Touch','Technique']

        entire_data = entire_data[label2]
        average_row = entire_data.mean()
        average_row = pd.DataFrame([average_row])

        value2 =  attacking = [round(average_row['Acceleration'].values[0], 2), round(average_row['Agility'].values[0], 2),
                      round(average_row['Balance'].values[0], 2),
                     round(average_row['Pace'].values[0], 2), round(average_row['Stamina'].values[0], 2),
                     round(average_row['Vision'].values[0], 2), round(average_row['Off The Ball'].values[0], 2),
                     round(average_row['Work Rate'].values[0], 2), round(average_row['Flair'].values[0], 2),
                     round(average_row['Bravery'].values[0], 2), round(average_row['Crossing'].values[0], 2)
                    ,round(average_row['Dribbling'].values[0], 2),round(average_row['Passing'].values[0], 2),
                      round(average_row['First Touch'].values[0], 2),round(average_row['Technique'].values[0], 2)]


    #mental(data,col1,label[::-1],value[::-1])
    genradar(data,col1,label[::-1],value[::-1],value2[::-1])
def singlepizza(data,league,pos,Club):

    Player1_League = st.sidebar.selectbox('Choose League of Player',league)
    data = data[data['Division']==Player1_League]

    df = data

    team = data['Club'].unique().tolist()

    Player1_Club = st.sidebar.selectbox('Choose Club of Player',team)
    data = data[data['Club']==Player1_Club]

        
    name1 = data['Name'].unique().tolist()
    Player_Name1 = st.sidebar.selectbox('Choose player',name1)
    data = data[data['Name']==Player_Name1]

    position = st.sidebar.selectbox('Choose template',pos)

    option = st.sidebar.selectbox("Choose Type",['Individual','Compare to League avg'])

    submit = st.sidebar.button("Generate pizza plot")
    
    col1, col2,col3= st.columns(3)
    if submit:
        if option=='Individual':
            generatepizza(data,position,col1,col2,col3,df)
        else:
            generateradar(data,position,col1,col2,col3,df)



def goto():
    option1 = 'Men'
    cols = ['TFA','Virtual Scout','SS','BFM','Minnesota','Avid','Game Changer FA','IMAD']
    template = st.sidebar.selectbox("Select colour template",cols)
    if template == 'TFA':
        st.session_state['template'] = 'TFA'
        st.session_state['bg'] = '#16003B'
        st.session_state['bg2'] = '#11002e'
        st.session_state['text'] = '#FFFFFF'
        st.session_state['h1'] = '#f2e806'
        st.session_state['h2'] = '#f73c93'
        st.session_state['h3'] = '#FFFFFF'
        st.session_state['R1'] = st.session_state['h2']
        st.session_state['R2'] = st.session_state['h1']
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    if template == 'SS':
        st.session_state['template'] = 'SS'
        st.session_state['bg'] = '#1C4F61'
        st.session_state['text'] = '#FFFFFF'
        st.session_state['h1'] = '#26F594'
        st.session_state['h2'] = '#FFFFFF'
        st.session_state['h3'] =  '#F6F558'
        st.session_state['bg2'] = '#0E2730'
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = st.session_state['h3']
        path = "Quicksand-Bold.ttf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "Quicksand-SemiBold.ttf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    if template == 'BFM':
        st.session_state['template'] = 'BFM'
        st.session_state['bg'] = '#118B4A'
        st.session_state['text'] = 'black'
        st.session_state['h1'] = '#0074B3'
        st.session_state['h2'] = '#F5A623'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = st.session_state['h3']
        st.session_state['bg2'] = '#14703f'
    if template == 'Minnesota':
        st.session_state['template'] = 'Minnesota'
        st.session_state['bg'] = '#231F20'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#8CD2F4'
        st.session_state['h2'] = '#6E6EFF'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = st.session_state['h3']
        st.session_state['bg2'] = '#292325'
    elif template == 'Avid':
        st.session_state['template'] = 'Avid'
        st.session_state['bg'] = '#1b2530'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#b4945b'
        st.session_state['h2'] = '#b45b5d'
        st.session_state['h3'] = '#5ba8b4'
        st.session_state['c'] = st.session_state['h1']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = st.session_state['h3']
        st.session_state['bg2'] = '#101c29'
    elif template == 'Game Changer FA':
        st.session_state['template'] = 'Game Changer FA'
        st.session_state['bg'] = '#0c0c0c'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#2c248c'
        st.session_state['h2'] = '#db40e3'
        st.session_state['h3'] = '#dbe340'
        st.session_state['c'] = st.session_state['h1']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = '#cccccc'
        st.session_state['bg2'] = '#171414'
    elif template == 'IMAD':
        st.session_state['template'] = 'IMAD'
        st.session_state['bg'] = '#14243b'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#f4d450'
        st.session_state['h2'] = '#ff5e57'
        st.session_state['h3'] = '#f73c93'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'Virtual Scout':
        st.session_state['template'] = 'Virtual Scout'
        st.session_state['bg'] = '#171516'
        st.session_state['bg2'] = '#140f0f'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#f2e806'
        st.session_state['h2'] = '#f73c93'
        st.session_state['h3'] = '#FFFFFF'
        st.session_state['c'] = '#171616'
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)


    
    dataprep(option1)
    
    
    

