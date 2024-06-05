import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Function to retrieve user data from the database
def get_data(username, password):
    conn = sqlite3.connect('tubes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_all():
    conn = sqlite3.connect('tubes.db')
    restaurants = pd.read_sql_query('SELECT * FROM restaurants', conn)
    menus = pd.read_sql_query('SELECT * FROM menus', conn)
    conn.close()
    return restaurants,menus

# Function to handle login page
def login():
    st.title("Login Page")
    st.write("Please enter your username and password")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_data(username, password)
        if user[2]=='user':
            st.write(f"Welcome, {user[1]}!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.target_page = 'home'
            st.experimental_rerun()
        elif user[2]=='admin':
            st.write(f"Welcome, {user[1]}!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.target_page = 'home'
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Function to handle home page
def home():
    st.title("Home Page")
    st.write(f"Welcome {st.session_state.username}!")
    st.sidebar.title("Panel")
    choice = st.sidebar.selectbox("Menu", ["Menu Utama", "Riwayat Pesanan"])
    # Inject Bootstrap CSS
    
    st.markdown(
        """
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js" integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/" crossorigin="anonymous"></script>
        """,
        unsafe_allow_html=True
    )

    # Create the Bootstrap card
    st.markdown(
        """
            <div class="container text-center mb-2">
                <div class="row">
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://png.pngtree.com/png-clipart/20220818/ourmid/pngtree-blue-washing-machine-for-laundry-logo-png-image_6114594.png" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://logowik.com/content/uploads/images/free-food-delivery6258.logowik.com.webp" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://marketplace.canva.com/EAF4y3V4yF0/1/0/1600w/canva-blue-and-white-cleaning-services-logo-sEqBBz8aTSU.jpg" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Create Streamlit buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Laundry"):
            st.session_state.target_page = 'laundry'
            st.experimental_rerun()
    with col2:
        if st.button("Food Delivery"):
            st.session_state.target_page = 'food_deliv'
            st.experimental_rerun()
    with col3:
        if st.button("Cleaning Service"):
            st.session_state.target_page = 'cleaning'
            st.experimental_rerun()

    # Handle navigation
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.target_page = 'login'
        st.experimental_rerun()

def laundry():
    st.title("Laundry")
    st.write("This is the laundry page.")
    name = st.text_input("Nama",st.session_state.username)
    alamat = st.text_input("Alamat")
    jenis = st.selectbox("Jenis",["Pakaian","Selimut"])
    berat=st.number_input("Berat")
    service=st.selectbox("Paket Laundry",["Reguler (2 Hari)","Express (1 Hari)"])

    if st.button("Home"):
        st.session_state.target_page = 'home'
        st.experimental_rerun()

def food_deliv():
    st.title("Food Delivery")
    st.write(f"This is the food delivery page.")
    restaurants,menus=get_all()
    restaurant_names = restaurants['name'].tolist()
    selected_name = st.selectbox("Nama Restoran", restaurant_names)
    
    selected_restaurant = restaurants[restaurants['name'] == selected_name].iloc[0]
    st.subheader("MenuL")
    foods = menus[(menus['restaurant_id'] == selected_restaurant['id'])]
    
    menu_inputs = {}
    total_price = 0

    for idx, row in foods.iterrows():
        menu_inputs[idx] = st.number_input(f"{row['name']}", step=1)
        total_price += row['harga'] * menu_inputs[idx]

    st.write(f"Total Price: {total_price}")
    if st.button("Home"):
        st.session_state.target_page = 'home'
        st.experimental_rerun()

def cleaning():
    st.title("Cleaning services")
    st.write("This is the cleaning services page.")
    name = st.text_input("Nama", st.session_state.username)
    alamat = st.text_input("Alamat")
    berat=st.date_input("Tanggal",min_value=date.today())
    
    if st.button("Home"):
        st.session_state.target_page = 'home'
        st.experimental_rerun()

# Main function to handle navigation based on login status and target page
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.target_page = 'login'
    
    if st.session_state.logged_in:
        if st.session_state.target_page == 'home':
            home()
        elif st.session_state.target_page == 'cleaning':
            cleaning()
        elif st.session_state.target_page == 'food_deliv':
            food_deliv()
        elif st.session_state.target_page == 'laundry':
            laundry()
        else:
            login()
    else:
        login()
# Run the main function
if __name__ == "__main__":
    main()
