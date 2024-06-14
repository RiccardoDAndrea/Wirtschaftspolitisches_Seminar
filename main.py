import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, GRU
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import SimpleRNN, Dropout, Input
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
########################################################################################
#############  L O T T I E _ F I L E S #################################################
########################################################################################
def load_lottieurl(url:str): 
    """ 
    A funcztion to load lottie files from a url

    Input:
    - A URL of the lottie animation
    Output:
    - A lottie animation
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

no_X_variable_lottie = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_ydo1amjm.json')
wrong_data_type_ML = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_2frpohrv.json')
no_data_lottie = load_lottieurl('https://lottie.host/08c7a53a-a678-4758-9246-7300ca6c3c3f/sLoAgnhaN1.json')
value_is_zero_in_train_size = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_usmfx6bp.json')

########################################################################################
#############  L O T T I E _ F I L E S #################################################
########################################################################################





# Title of the main page
st.set_page_config(page_title='Recurrent Neural Network', page_icon=':robot:', layout='wide')
st.title('Recurrent Neural Network')


st.sidebar.title('Recurrent Neural Network')
file_uploader = st.sidebar.file_uploader('Upload your dataset', type=['csv'])
    
# Check if the file has been uploaded
if file_uploader is None:           # If no file is uploaded
    st.sidebar.info('Please upload your dataset')
    st.markdown("""
        Welcome to the Recurrent Neural Network
        This is a simple example of how to create 
        a Recurrent Neural Network using TensorFlow 
        and Keras.
        Please upload your dataset to get started
        """)
    
    st_lottie(no_data_lottie)
    st.stop()       # Stop the script so that we dont get an error

else:
    # Expander for upload settings.
    with st.sidebar.expander('Upload settings'):
        separator, thousands = st.columns(2)
        with separator:
            selected_separator = st.selectbox('value separator:', (",", ";", ".", ":"))
        with thousands:
            selected_thousands = st.selectbox('thousands separator:', (".", ","), key='thousands')
        
        decimal, unicode = st.columns(2)
        with decimal:
            selected_decimal = st.selectbox('decimal separator:', (".", ","), key='decimal')
        with unicode:
            selected_unicode = st.selectbox('file encoding:', ('utf-8', 'utf-16', 'utf-32', 'iso-8859-1', 'cp1252'))

   

        # Read the uploaded file into a DataFrame with the selected separators
df = pd.read_csv(file_uploader, sep=selected_separator, 
                thousands=selected_thousands, decimal=selected_decimal)

# Spalte 'Date' in datetime-Objekte konvertieren
df['Date'] = pd.to_datetime(df['Date'])




    

### General Information about the data
# Display the DataFrame
st.subheader("Your DataFrame: ")
st.dataframe(df, use_container_width=True)
st.divider()

##########################################################################################
#############  D a t a _ d e s c r i b e #################################################
##########################################################################################

with st.expander('Data Description'):
    st.subheader("Data Description: ")  
    st.dataframe(df.describe())
    st.divider()

##########################################################################################
#############  D a t a _ d e s c r i b e #################################################
##########################################################################################



##################################################################################################
#############  D a t a _ C l e a n i n g _ e n d #################################################
##################################################################################################

with st.expander('Data Cleaning'):
    st.subheader('How to proceed with NaN values')
    st.dataframe(df.isna().sum(), use_container_width=True) # get the sum of NaN values in the DataFrame
    checkbox_nan_values = st.checkbox("Do you want to replace the NaN values to proceed?", key="disabled")

    if checkbox_nan_values:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        missing_values = st.selectbox(
            "How do you want to replace the NaN values in the numeric columns?",
            key="visibility",
            options=["None",
                    "with Median", 
                    "with Mean", 
                    "with Minimum value", 
                    "with Maximum value", 
                    "with Zero"])

        if 'with Median' in missing_values:
            uploaded_file_median = df[numeric_columns].median()
            df[numeric_columns] = df[numeric_columns].fillna(uploaded_file_median)
            st.write('##### You have succesfully change the NaN values :blue[with the Median]')
            st.dataframe(df.isna().sum(), use_container_width=True)
            st.divider()
            
        elif 'with Mean' in missing_values:
            uploaded_file_mean = df[numeric_columns].mean()
            df[numeric_columns] = df[numeric_columns].fillna(uploaded_file_mean)
            st.markdown(' ##### You have succesfully change the NaN values :blue[ with the Mean]')
            st.dataframe(df.isna().sum(), use_container_width=True)
            st.divider()

        elif 'with Minimum value' in missing_values:
            uploaded_file_min = df[numeric_columns].min()
            df[numeric_columns] = df[numeric_columns].fillna(uploaded_file_min)
            st.write('##### You have succesfully change the NaN values :blue[with the minimum values]')
            st.dataframe(df.isna().sum(), use_container_width=True)
            st.divider()
            
        elif 'with Maximum value' in missing_values:
            uploaded_file_max = df[numeric_columns].max()
            df[numeric_columns] = df[numeric_columns].fillna(uploaded_file_max)
            st.write('##### You have succesfully change the NaN values :blue[with the maximums values]')
            st.dataframe(df.isna().sum(), use_container_width=True)
            st.divider()
            
        elif 'with Zero' in missing_values:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            df[numeric_columns] = df[numeric_columns].fillna(0)
            st.write('##### You have successfully changed :blue[the NaN values to 0.]')
            st.dataframe(df.isna().sum(), use_container_width=True)
            st.divider()

    st.divider()
    st.subheader("Remove Columns:")
    selected_columns = st.multiselect("Choose your columns", df.columns)
    df = df.drop(selected_columns, axis=1)
    st.dataframe(df)
    st.divider()


    st.subheader('Your DataFrame data types: ')
    st.dataframe(df.dtypes, use_container_width=True)
    st.write('Change your DataFrame data types')

    st.subheader("Change your Data Types:")
    selected_columns = st.multiselect("Choose your columns", df.columns, key='change_data_type')
    selected_dtype = st.selectbox("Choose a data type", ["int64", "float64", "string", "datetime64[ns]"])
    st.divider()

##################################################################################################
#############  D a t a _ C l e a n i n g #################################################
##################################################################################################



####################################################################################################
#############  D a t a _ V i s u a l i z a t i o n #################################################
####################################################################################################


with st.expander('Data Visualization'):

    options_of_charts = st.multiselect('What Graphs do you want?', ('Linechart', 
                                                                    'Scatterchart',
                                                                    'Correlation Matrix'))
    for chart_type in options_of_charts:

        if chart_type == 'Scatterchart':
            st.write('You can freely choose your :blue[Scatter plot]')
            x_axis_val_col_, y_axis_val_col_ = st.columns(2)
            with x_axis_val_col_:
                x_axis_val = st.selectbox('Select X-Axis Value', options=df.columns, key='x_axis_selectbox')
            with y_axis_val_col_:
                y_axis_val = st.selectbox('Select Y-Axis Value', options=df.columns, key='y_axis_selectbox')
            scatter_plot_1 = px.scatter(df, x=x_axis_val,y=y_axis_val)

            st.plotly_chart(scatter_plot_1,use_container_width=True)
            # Erstellen des Histogramms mit Plotly
            plt.tight_layout()
            st.divider()
        
        elif chart_type == 'Linechart':
            st.markdown('You can freely choose your :blue[Linechart] :chart_with_upwards_trend:')

            col3,col4 = st.columns(2)
            
            with col3:
                x_axis_val_line = st.selectbox('Select X-Axis Value', options=df.columns,
                                            key='x_axis_line_multiselect')
            with col4:
                y_axis_vals_line = st.multiselect('Select :blue[Y-Axis Values]', options=df.columns,
                                                key='y_axis_line_multiselect')

            line_plot_1 = px.line(df, x=x_axis_val_line, y=y_axis_vals_line)
            st.plotly_chart(line_plot_1)
        
        elif chart_type == 'Correlation Matrix':
            corr_matrix = df.select_dtypes(include=['float64', 
                                                    'int64']).corr()


            # Erstellung der Heatmap mit Plotly
            fig_correlation = px.imshow(corr_matrix.values, 
                                        color_continuous_scale = 'purples', 
                                        zmin = -1, 
                                        zmax = 1,
                                        x = corr_matrix.columns, 
                                        y = corr_matrix.index,
                                        labels = dict( x = "Columns", 
                                                    y = "Columns", 
                                                    color = "Correlation"))

            # Anpassung der Plot-Parameter
            fig_correlation.update_layout(
                                        title='Correlation Matrix',
                                        font=dict(
                                        color='grey'
                )
            )

            fig_correlation.update_traces(  showscale = False, 
                                            colorbar_thickness = 25)

            # Hinzufügen der numerischen Werte als Text
            annotations = []
            for i, row in enumerate(corr_matrix.values):
                for j, val in enumerate(row):
                    annotations.append(dict(x=j, y=i, text=str(round(val, 2)), showarrow=False, font=dict(size=16)))
            fig_correlation.update_layout(annotations=annotations)

            # Anzeigen der Plot
            st.plotly_chart(fig_correlation, use_container_width= True)
            fig_correlationplot = go.Figure(data=fig_correlation)

####################################################################################################
#############  D a t a _ V i s u a l i z a t i o n #################################################
####################################################################################################





####################################################################################################
############# R e c c u r e n t _ N e u r a l _ N e t w o r k ######################################
####################################################################################################




st.subheader("Create your own Reccurent Neural Network: ")

Sequentiual_variable_col, X_variables_col = st.columns(2)
Sequentiual_variable = Sequentiual_variable_col.selectbox('Enter your Sequentiual Data', 
                                                options=df.columns, key='RNN Variable')
X_variables = X_variables_col.selectbox('Enter your Forcasting Column', 
                                          options=df.columns, key='RNN X Variables')


X = df[X_variables]
y = df[Sequentiual_variable]

# Abfangen von Fehlern
# Überprüfung des Datentyps der ausgewählten Variablen
if X.dtype == 'object' or X.dtype == 'string' or X.dtype == 'datetime64[ns]':
    st.warning('Ups, wrong data type for Target variable!')
    st_lottie('wrong_data_type_ML.json', width=700, height=300, quality='low', loop=False)
    st.dataframe(df.dtypes, use_container_width=True)
    st.stop()

if X.dtype == 'object' or X.dtype == 'string' or X.dtype == 'datetime64[ns]':
    st.warning('Ups, wrong data type for Target variable!')
    st_lottie('wrong_data_type_ML.json', width=700, height=300, quality='low', loop=False)
    st.dataframe(df.dtypes, use_container_width=True)
    st.stop()


# Default parameters
total_size = 100
train_size = 60
# test_size = 40
validation_size = 20

# Layout columns
train_size_col, validation_size_col = st.columns(2)

# Train Size slider
with train_size_col:
    train_size = st.slider('Train Size', min_value=0, max_value=total_size, 
                           value=train_size, key='train_size')
    # Adjust test_size and validation_size to ensure total_size is maintained

# Test Size slider
with validation_size_col:
    validation_size = st.slider('Validation Size', min_value=0, max_value=total_size, 
                          value=validation_size, key='validation_size')
    # Adjust train_size and validation_size to ensure total_size is maintained

# X = df[X_variables]
# y = df[Target_variable]


X_train, y_train = X[:int(len(df)*train_size/100)], y[:int(len(df)*train_size/100)] # 60% of the data -> 

X_val, y_val = X[:int(len(df)*validation_size/100)], y[:int(len(df)*validation_size/100)]

# 1. determination of the data length.
# 2. We multiply the values from the slider by the length of the df and divide it by 100. and convert it into an int instead of a float


# Check conditions
if train_size <= 0:
    st.warning('Train size should be greater than zero.')
    st.stop()

# elif test_size <= 0:
#     st.warning('Test size should be greater than zero.')
#     st.stop()

# elif train_size + test_size > total_size:
#     st.warning('Train size and Test size exceed the total size.')
#     st.stop()

elif validation_size > train_size:
    st.warning('Validation size should not exceed Train size.')
    st.stop()

#Assuming df is your dataset
elif train_size >= len(df):  # Uncomment if you have a dataset to check against
    st.warning('Train size cannot be greater than or equal to the number of samples in the dataset')
    st.stop()
    
st.write(X_train.shape)
# initializing the RNN
regressor = Sequential()
# defining the input shape
regressor.add(Input(shape=(X_train.shape)))
# adding first RNN layer and dropout regularization
regressor.add(SimpleRNN(units=50, activation="tanh", return_sequences=True))
regressor.add(Dropout(0.2))

# adding second RNN layer and dropout regularization
regressor.add(SimpleRNN(units=50, activation="tanh", return_sequences=True))
regressor.add(Dropout(0.2))

# adding third RNN layer and dropout regularization
regressor.add(SimpleRNN(units=50, activation="tanh", return_sequences=True))
regressor.add(Dropout(0.2))

# adding fourth RNN layer and dropout regularization
regressor.add(SimpleRNN(units=50))
regressor.add(Dropout(0.2))

# adding the output layer
regressor.add(Dense(units=1))

# compiling RNN
regressor.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])

# fitting the RNN
history = regressor.fit(X_train, y_train, epochs=5, batch_size=32)
st.write('RNN Model has been trained successfully')




####################################################################################################
############# R e c c u r e n t _ N e u r a l _ N e t w o r k ######################################
###################################################################################################
