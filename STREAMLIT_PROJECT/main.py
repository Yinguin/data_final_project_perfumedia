import pandas as pd
import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

df = pd.read_csv('perfume_final.csv')

# Add title to the website
st.write('<h1 style="text-align: center;">Perfumedia</h1>', unsafe_allow_html=True)

# Use CSS flexbox to arrange the elements
st.markdown("""
<div style="display: flex; align-items: center;">
    <div style="flex: 1;">
        <img src="https://assets.wikiparfum.com/_resized/ezKtZjzkM3NrsWAExwCCVlcWhP2rqbaw0A6V1Ey3-w2000-q75.webp" width="470">
    </div>
    <div style="flex: 1; font-size: 24px; text-align: center;">
        Welcome to Perfumedia, the APP for perfume lovers.
    </div>
</div>
""", unsafe_allow_html=True)

# Add a horizontal line as a separator
st.markdown("<hr>", unsafe_allow_html=True)


def search_perfume_info():
    st.write("* Find your perfume by brand or name")
    user_input = st.text_input('Enter the brand or name of the perfume:')
    # Convert the user input to lowercase
    input_str = user_input.lower()

    # Combine 'brand' and 'name' columns into a new 'brand_name' column and convert to lowercase
    df['brand_name'] = df['brand'].str.lower() + ' ' + df['name'].str.lower()

    mask = df['brand_name'].apply(lambda x: all(word in x for word in input_str.split()))

    # Filter the DataFrame based on the mask
    results = df[mask]

    # Drop the 'brand_name' column to keep the original DataFrame unchanged
    df.drop(columns=['brand_name'], inplace=True)

    if user_input:  # Check if user has provided input
        if results.empty:
            st.write('No perfumes found matching the input.')
        else:
            # Sort the results by customer_rating and review_count
            results.sort_values(by=['customer_rating', 'review_count'], ascending=[False, False], inplace=True)

            # Show the table with only id, brand, name, category, gender, and customer rating
            columns_to_show = ['brand', 'name', 'category', 'gender', 'customer_rating']
            st.table(results[columns_to_show])

            # Check if any id is clicked
            selected_row = st.selectbox('Select an ID to view the details:', results.index)
            selected_perfume = results.loc[selected_row]

            # Display the details of the selected perfume
            col1, col2 = st.columns(2)  # Split the layout into two columns
            with col1:
                st.header('Perfume Details')
                st.write('Brand:', selected_perfume['brand'])
                st.write('Name:', selected_perfume['name'])
                st.write('Category:', selected_perfume['category'])
                st.write('Gender:', selected_perfume['gender'])
                st.write('Fragrance:', selected_perfume['fragrance'])
                st.write('Price per 100ml:', f"{round(selected_perfume['base_price'] / 10, 2)} €")
                st.write('Customer Rating:', selected_perfume['customer_rating'])
                st.write('Review Count:', selected_perfume['review_count'])

            with col2:
                # Show the image of the selected perfume
                st.image(selected_perfume['image'], width=200)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write('Top Note')
                top_note_words = selected_perfume['top_note'].lower().split(', ') if isinstance(selected_perfume['top_note'], str) else None
                if top_note_words:
                    for note_word in top_note_words:
                        image_path = f"pics/{note_word}.webp"
                        if os.path.exists(image_path):
                            st.image(image_path, caption=note_word, width=120)
                        else:
                            st.write(f" {note_word}")

            with col2:
                st.write('Heart Note')
                heart_note_words = selected_perfume['heart_note'].lower().split(', ') if isinstance(selected_perfume['heart_note'], str) else None
                if heart_note_words:
                    for note_word in heart_note_words:
                        image_path = f"pics/{note_word}.webp"
                        if os.path.exists(image_path):
                            st.image(image_path, caption=note_word, width=120)
                        else:
                            st.write(f"{note_word}")

            with col3:
                st.write('Base Note')
                base_note_words = selected_perfume['base_note'].lower().split(', ') if isinstance(selected_perfume['base_note'], str) else None
                if base_note_words:
                    for note_word in base_note_words:
                        image_path = f"pics/{note_word}.webp"
                        if os.path.exists(image_path):
                            st.image(image_path, caption=note_word, width=120)
                        else:
                            st.write(f"{note_word}")

    return

def find_similar_perfumes(top_n=6):
    st.write("* Find similar perfumes")
    # Ask the user to input the perfume ID
    input_perfume_id = st.number_input('Enter the perfume ID:', min_value=1, max_value=len(df), step=1)

    # Find the notes of the input perfume using the given ID
    input_perfume_notes = df.loc[input_perfume_id, 'notes']
    
    # Vectorize the notes using TF-IDF
    vectorizer = TfidfVectorizer()
    notes_vectors = vectorizer.fit_transform(df['notes'])
    
    # Vectorize the notes of the input perfume
    input_vector = vectorizer.transform([input_perfume_notes])
    
    # Calculate cosine similarity between the input perfume and all other perfumes
    cosine_similarities = cosine_similarity(input_vector, notes_vectors).flatten()
    
    # Add cosine similarity as a new column to the DataFrame
    df['cosine_similarity'] = cosine_similarities
    
    # Sort the DataFrame based on cosine similarity in descending order
    similar_perfumes = df.sort_values(by='cosine_similarity', ascending=False)
    
    # Define the columns to show in the output table
    columns_to_show = ['brand', 'name', 'category', 'gender', 'cosine_similarity']
    st.table(similar_perfumes.head(top_n)[columns_to_show])

    # Check if any id is clicked
    selected_row = st.selectbox('Select an ID to view the details:', similar_perfumes.index)
    selected_perfume = similar_perfumes.loc[selected_row]

    # Display the details of the selected perfume
    col1, col2 = st.columns(2)  # Split the layout into two columns
    with col1:
        st.header('Perfume Details')
        st.write('Brand:', selected_perfume['brand'])
        st.write('Name:', selected_perfume['name'])
        st.write('Category:', selected_perfume['category'])
        st.write('Gender:', selected_perfume['gender'])
        st.write('Fragrance:', selected_perfume['fragrance'])
        st.write('Price per 100ml:', f"{round(selected_perfume['base_price'] / 10, 2)} €")
        st.write('Customer Rating:', selected_perfume['customer_rating'])
        st.write('Review Count:', selected_perfume['review_count'])

    with col2:
        # Show the image of the selected perfume
        st.image(selected_perfume['image'], width=200)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Top Note')
        top_note_words = selected_perfume['top_note'].lower().split(', ') if isinstance(selected_perfume['top_note'], str) else None
        if top_note_words:
            for note_word in top_note_words:
                image_path = f"pics/{note_word}.webp"
                if os.path.exists(image_path):
                    st.image(image_path, caption=note_word, width=120)
                else:
                    st.write(f" {note_word}")

    with col2:
        st.write('Heart Note')
        heart_note_words = selected_perfume['heart_note'].lower().split(', ') if isinstance(selected_perfume['heart_note'], str) else None
        if heart_note_words:
            for note_word in heart_note_words:
                image_path = f"pics/{note_word}.webp"
                if os.path.exists(image_path):
                    st.image(image_path, caption=note_word, width=120)
                else:
                    st.write(f"{note_word}")

    with col3:
        st.write('Base Note')
        base_note_words = selected_perfume['base_note'].lower().split(', ') if isinstance(selected_perfume['base_note'], str) else None
        if base_note_words:
            for note_word in base_note_words:
                image_path = f"pics/{note_word}.webp"
                if os.path.exists(image_path):
                    st.image(image_path, caption=note_word, width=120)
                else:
                    st.write(f"{note_word}")

    return

# Function to get the desired brand from the user
def get_brand():
    # Get user input for brand and convert to lowercase
    brand_input = st.text_input("Enter a brand:")
    brand = brand_input.lower()

    # Get unique brands from the DataFrame and convert them to lowercase for comparison
    all_brands = df['brand'].str.lower().unique()

    if brand_input:  # Check if there is a user input
        # Check if the lowercase brand input exists in the lowercase brands list
        if brand in all_brands:
            st.write(f"Selected brand: {brand}")
            return [brand]  # Return the brand as a list
        else:
            st.write("Sorry, we don't have the brand you want. Please enter another brand or skip.")
            return get_brand()  # Ask the user to input again
    else:
        st.write("No brand chosen. Getting all brands.")
        return all_brands.tolist()  # Return all the unique brands in the DataFrame as a list
    return

# Function to get the desired categories from the user
def get_categories():
    all_categories = df['category'].unique()
    selected_categories = st.multiselect("Choose category(s):", all_categories)

    if not selected_categories:
        st.write("No category chosen. Getting all categories.")
        return all_categories.tolist()

    st.write(f"Selected category(s): {', '.join(selected_categories)}")
    return selected_categories

# Function to get the desired gender from the user
def get_gender():
    all_genders = df['gender'].unique()
    selected_gender = st.multiselect("Choose gender(s):", all_genders)

    if not selected_gender:
        st.write("No gender chosen. Getting all genders.")
        return all_genders.tolist()

    st.write(f"Selected gender(s): {', '.join(selected_gender)}")
    return selected_gender

# Function to get the desired fragrance from the user
def get_fragrance():
    all_fragrances = df['fragrance'].unique()
    selected_fragrance = st.multiselect("Choose fragrance(s):", all_fragrances)

    if not selected_fragrance:
        st.write("No fragrance chosen. Getting all fragrances.")
        return all_fragrances.tolist()

    st.write(f"Selected fragrance(s): {', '.join(selected_fragrance)}")
    return selected_fragrance

def get_notes():
    notes = []
    max_choices = 5

    st.write("Enter notes:")

    # Use st.columns to create 5 equal-width columns
    cols = st.columns(5)

    for i, col in enumerate(cols):
        choice = col.text_input(f"Enter note {i+1}:")

        if choice:  # Check if the input is not empty
            notes.append(choice)
            col.write(f"{choice} added to the chosen notes.")

    if len(notes) == 0:
        st.write("No notes entered.")
    else:
        st.write(f"Selected notes: {', '.join(notes)}")

    return notes

# Function to get the desired price range from the user
def get_price_range():
    # Get the lowest and highest prices from the DataFrame's "base_price" column (in 1000ml)
    lowest_price_1000ml = df["base_price"].min()
    highest_price_1000ml = df["base_price"].max()

    # Adjust the lowest and highest prices for 100ml comparison
    lowest_price = lowest_price_1000ml / 10
    highest_price = highest_price_1000ml / 10

    # Get user input for the price range using sliders
    price_from, price_to = st.slider('Select price range for 100ml:', min_value=float(lowest_price), max_value=float(highest_price), value=(float(lowest_price), float(highest_price)), step=0.01)

    # Check if the price upper limit is lower than the price lower limit
    if price_to < price_from:
        st.write("Invalid price range. The price upper limit cannot be lower than the price lower limit.")
        return get_price_range()  # Ask the user to input again

    st.write(f"Price range selected: {price_from} to {price_to} EUR per 100ml")
    return price_from, price_to

def perfume_recommender():
    st.write("* Perfume Recommer")
    
    # Get user inputs for brand, categories, gender, fragrance, and price range
    brand = get_brand()
    categories = get_categories()
    genders = get_gender()
    fragrances = get_fragrance()
    notes = get_notes()
    price_from, price_to = get_price_range()

    # Apply the filters to the DataFrame
    mask_brand = df['brand'].str.lower().isin(brand) if brand and len(brand) > 0 else True
    mask_categories = df['category'].isin(categories) if categories and len(categories) > 0 else True
    mask_genders = df['gender'].isin(genders) if genders and len(genders) > 0 else True
    mask_fragrances = df['fragrance'].isin(fragrances) if fragrances and len(fragrances) > 0 else True
    mask_price = (df['base_price']/10 >= price_from) & (df['base_price']/10 <= price_to)

    # Apply the notes filter to the DataFrame if notes are provided
    if notes and len(notes) > 0:
        note_masks = [df['notes'].str.contains(note, case=False) for note in notes]
        mask_notes = pd.DataFrame(note_masks).T.any(axis=1)
    else:
        mask_notes = True

    # Combine all the masks using the logical AND operator (&)
    combined_mask = mask_brand & mask_categories & mask_genders & mask_fragrances & mask_price & mask_notes

    # Filter the DataFrame based on the combined mask
    recommended_perfumes = df[combined_mask]

    if recommended_perfumes.empty:
        print('No perfumes found matching the selected criteria.')
    else:
        # Sort the results by the number of matched notes, customer_rating, and review_count
        recommended_perfumes['num_matched_notes'] = recommended_perfumes['notes'].apply(lambda x: sum(note in x for note in notes))
        recommended_perfumes.sort_values(by=['num_matched_notes', 'customer_rating', 'review_count'], ascending=[False, False, False], inplace=True)
        recommended_perfumes.drop(columns=['num_matched_notes'], inplace=True)

        # Show the initial table with only id, brand, name, category, gender, and customer rating
        columns_to_show = ['brand', 'name', 'category', 'gender', 'customer_rating']
        st.table(recommended_perfumes[columns_to_show])

        # Check if any id is clicked
        selected_row = st.selectbox('Select an ID to view the details:', recommended_perfumes.index)
        selected_perfume = recommended_perfumes.loc[selected_row]

        # Display the details of the selected perfume
        col1, col2 = st.columns(2)  # Split the layout into two columns
        with col1:
            st.header('Perfume Details')
            st.write('Brand:', selected_perfume['brand'])
            st.write('Name:', selected_perfume['name'])
            st.write('Category:', selected_perfume['category'])
            st.write('Gender:', selected_perfume['gender'])
            st.write('Fragrance:', selected_perfume['fragrance'])
            st.write('Price per 100ml:', f"{round(selected_perfume['base_price'] / 10, 2)} €")
            st.write('Customer Rating:', selected_perfume['customer_rating'])
            st.write('Review Count:', selected_perfume['review_count'])

        with col2:
            # Show the image of the selected perfume
            st.image(selected_perfume['image'], width=200)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Top Note')
            top_note_words = selected_perfume['top_note'].lower().split(', ') if isinstance(selected_perfume['top_note'], str) else None
            if top_note_words:
                for note_word in top_note_words:
                    image_path = f"pics/{note_word}.webp"
                    if os.path.exists(image_path):
                        st.image(image_path, caption=note_word, width=120)
                    else:
                        st.write(f" {note_word}")

        with col2:
            st.write('Heart Note')
            heart_note_words = selected_perfume['heart_note'].lower().split(', ') if isinstance(selected_perfume['heart_note'], str) else None
            if heart_note_words:
                for note_word in heart_note_words:
                    image_path = f"pics/{note_word}.webp"
                    if os.path.exists(image_path):
                        st.image(image_path, caption=note_word, width=120)
                    else:
                        st.write(f"{note_word}")

        with col3:
            st.write('Base Note')
            base_note_words = selected_perfume['base_note'].lower().split(', ') if isinstance(selected_perfume['base_note'], str) else None
            if base_note_words:
                for note_word in base_note_words:
                    image_path = f"pics/{note_word}.webp"
                    if os.path.exists(image_path):
                        st.image(image_path, caption=note_word, width=120)
                    else:
                        st.write(f"{note_word}")

    return


# Create a dictionary to map the subsection names to their corresponding functions
apps = {
    "Search Perfumes": search_perfume_info,
    "Find Similar Perfumes": find_similar_perfumes,
    "Perfume Recommender": perfume_recommender
}

# Add a sidebar for navigation between subsections
st.sidebar.title("Navigation")
selected_app = st.sidebar.radio("APPs:", list(apps.keys()))

# Call the selected function based on the user's choice
apps[selected_app]()