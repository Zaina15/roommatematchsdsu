import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Paths to JSON files
USERS_JSON = 'database/Users.json'
USERINTERESTS_JSON = 'database/UserInterests.json'
INTERESTS_JSON = 'database/Interests.json'
LIVINGPREFERENCES_JSON = 'database/LivingPreferences.json'
ACADEMICINFO_JSON = 'database/AcademicInfo.json'
ADDITIONALPREFERENCES_JSON = 'database/AdditionalPreferences.json'
PETSINFO_JSON = 'database/PetsInfo.json'

# Read JSON data from files
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Compatibility calculation function
def calculate_compatibility(user1, user2, user_interests, living_preferences, academic_info, pets_info, additional_preferences):
    score = 0
    
    # Gender compatibility
    if user1['gender'] == user2['gender']:
        score += 10
    
    # Age compatibility (same logic as before)
    age_diff = abs(user1['age'] - user2['age'])
    if age_diff <= 2:
        score += 20

    # Compare living preferences
    user1_living_pref = next((pref for pref in living_preferences if pref['user_id'] == user1['user_id']), None)
    user2_living_pref = next((pref for pref in living_preferences if pref['user_id'] == user2['user_id']), None)
    
    if user1_living_pref and user2_living_pref:
        if user1_living_pref['cleanliness'] == user2_living_pref['cleanliness']:
            score += 5
        if user1_living_pref['noise_level'] == user2_living_pref['noise_level']:
            score += 5
        if user1_living_pref['sleep_schedule'] == user2_living_pref['sleep_schedule']:
            score += 5
        if user1_living_pref['smoking'] == user2_living_pref['smoking']:
            score += 5
        if user1_living_pref['guest_frequency'] == user2_living_pref['guest_frequency']:
            score += 5

    # Compare academic info
    user1_academic_info = next((info for info in academic_info if info['user_id'] == user1['user_id']), None)
    user2_academic_info = next((info for info in academic_info if info['user_id'] == user2['user_id']), None)
    
    if user1_academic_info and user2_academic_info:
        if user1_academic_info['major'] == user2_academic_info['major']:
            score += 10
        if user1_academic_info['study_habits'] == user2_academic_info['study_habits']:
            score += 10

    # Compare additional preferences
    user1_additional_pref = next((pref for pref in additional_preferences if pref['user_id'] == user1['user_id']), None)
    user2_additional_pref = next((pref for pref in additional_preferences if pref['user_id'] == user2['user_id']), None)
    
    if user1_additional_pref and user2_additional_pref:
        if user1_additional_pref['additional_info'] == user2_additional_pref['additional_info']:
            score += 5

    # Compare pets info
    user1_pets_info = next((info for info in pets_info if info['user_id'] == user1['user_id']), None)
    user2_pets_info = next((info for info in pets_info if info['user_id'] == user2['user_id']), None)
    
    if user1_pets_info and user2_pets_info:
        if user1_pets_info['has_pets'] == user2_pets_info['has_pets']:
            score += 10

    # Compare interests
    user1_interests = [ui['interest_id'] for ui in user_interests if ui['user_id'] == user1['user_id']]
    user2_interests = [ui['interest_id'] for ui in user_interests if ui['user_id'] == user2['user_id']]
    
    common_interests = set(user1_interests).intersection(user2_interests)
    score += len(common_interests) * 3  # Each common interest adds 3 points

    return score

# Route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        
        # Read data from JSON files
        users = read_json_file(USERS_JSON)
        user_interests = read_json_file(USERINTERESTS_JSON)
        interests = read_json_file(INTERESTS_JSON)
        living_preferences = read_json_file(LIVINGPREFERENCES_JSON)
        academic_info = read_json_file(ACADEMICINFO_JSON)
        additional_preferences = read_json_file(ADDITIONALPREFERENCES_JSON)
        pets_info = read_json_file(PETSINFO_JSON)
        
        current_user = next((user for user in users if user['user_id'] == user_id), None)
        if current_user is None:
            return "User not found"
        
        # Find compatibility scores
        compatibility_scores = []
        for user in users:
            if user['user_id'] != current_user['user_id']:
                score = calculate_compatibility(current_user, user, user_interests, living_preferences, academic_info, pets_info, additional_preferences)
                compatibility_scores.append((user, score))

        # Sort users by score
        compatibility_scores.sort(key=lambda x: x[1], reverse=True)

        # Get top 5 matches
        top_5_matches = [{'username': user['username'], 'full_name': user['full_name'], 'score': score} for user, score in compatibility_scores[:5]]

        return render_template('algorithm.html', matches=top_5_matches)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
