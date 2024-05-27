import pandas as pd
import openai
from google.colab import files
import datetime

api_key = " "
openai.api_key = api_key

lna_master = pd.read_csv('lna_master.csv')
lna_score = pd.read_csv('lna_score.csv')

merged_data = pd.merge(lna_master, lna_score, on='competency_id', how='inner')

def generate_learning_solutions(row):
    if row['status']:
        required_level_map = {1: 'Entry', 2: 'Basic', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}
        required_level_description = required_level_map.get(row['required_level'])
        current_level_map = {1: 'Entry', 2: 'Basic', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}
        current_level_description = required_level_map.get(row['current_level'])
        prompt = (f"{row['employee_id']} requires enhancement in the competency {row['competency_id']}, "
                  f"with an actual level of {current_level_description} compared to the required mastery level of {required_level_description}. "
                  f"I need brief recommendations (only 2 sentences) for a targeted learning solution approach tailored to {row['competency_name']} "
                  f"at a {required_level_description} proficiency level, considering {row['rumpun_jabatan']} as a job family. "
                  f"The solution should prioritize non-technical and efficient learning methods and consider the difficulty of the solution to fit for {required_level_description} proficiency level.")
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    else:
        return ''

def generate_learning_topics(row):
    if row['status']:
        required_level_map = {1: 'Entry', 2: 'Basic', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}
        required_level_description = required_level_map.get(row['required_level'])
        prompt = (f"What are the relevant key outlines or latest essential knowledge or paradigm that I will acquire for the competency {row['competency_name']} "
                  f"at the {required_level_description} proficiency level? List in 1 Title learning and 5 point of brief outline. Make the outline simple (just one line)")
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )
        topics = [topic['text'].strip() for topic in response.choices[:2]]
        return '; '.join(topics)
    else:
        return ''

merged_data['recommendation'] = merged_data.apply(generate_learning_solutions, axis=1)
merged_data['topic_1'] = merged_data.apply(generate_learning_topics, axis=1)
merged_data = merged_data[merged_data['recommendation'] != '']

output_file = 'learning_recommendations.xlsx'
selected_columns = ['lna_master_id', 'employee_id', 'group_id', 'position_id', 'competency_id', 'name', 'kelas_jabatan', 'rumpun_jabatan', 'vitality_score', 'priority_comp', 'current_level', 'required_level', 'status', 'aggregate_competency', 'lna_batch_id_x', 'createdAt_x', 'updatedAt_x', 'lna_score_id', 'competency_name', 'recommendation', 'topic_1']

merged_data[selected_columns].to_excel(output_file, index=False)

files.download(output_file)

def collect_feedback_and_progress(employee_id):
    feedback = input(f"Enter feedback for employee {employee_id} on the learning solution: ")
    progress = input(f"Enter progress for employee {employee_id} on the learning solution (0-100%): ")
    return feedback, int(progress)

def update_recommendations():
    updated_data = []
    for index, row in merged_data.iterrows():
        feedback, progress = collect_feedback_and_progress(row['employee_id'])
        prompt = (f"Based on the feedback '{feedback}' and progress {progress}%, "
                  f"please provide updated recommendations for improving competency {row['competency_id']} "
                  f"({row['competency_name']}) for employee {row['employee_id']}.")
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150
        )
        updated_recommendation = response.choices[0].text.strip()
        updated_data.append((row['employee_id'], row['competency_id'], updated_recommendation, feedback, progress))
    
    updated_df = pd.DataFrame(updated_data, columns=['employee_id', 'competency_id', 'updated_recommendation', 'feedback', 'progress'])
    return updated_df

updated_recommendations_df = update_recommendations()
updated_recommendations_file = 'updated_learning_recommendations.xlsx'
updated_recommendations_df.to_excel(updated_recommendations_file, index=False)

files.download(updated_recommendations_file)
