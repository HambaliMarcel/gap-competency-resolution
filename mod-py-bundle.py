import pandas as pd
import openai
from google.colab import files

api_key = ""
openai.api_key = api_key

proficiency_levels = {1: 'Entry', 2: 'Basic', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}

lna_master = pd.read_csv('lna_master.csv')
lna_score = pd.read_csv('lna_score.csv')

merged_data = pd.merge(lna_master, lna_score, on='competency_id', how='inner')

def generate_learning_solutions(row):
    if row['status']:
        required_level_description = proficiency_levels.get(row['required_level'])
        current_level_description = proficiency_levels.get(row['current_level'])
        if row['kelas_jabatan'] > 15:
            prompt = f"{row['employee_id']} requires enhancement in the competency {row['competency_id']}, with an actual level of {current_level_description} compared to the required mastery level of {required_level_description}. I need brief recommendations (only 2 sentences) for a targeted learning solution approach tailored to {row['competency_name']} at a {required_level_description} proficiency level. Consider that {row['rumpun_jabatan']} as a job family. The solution should prioritize non-technical and efficient learning methods and consider difficulty of the solution to fit for {required_level_description} proficiency level."
        else:
            prompt = f"{row['employee_id']} requires enhancement in the competency {row['competency_id']}, with an actual level of {current_level_description} compared to the required mastery level of {required_level_description}. I need brief recommendations (only 2 sentences) recommendations for a targeted learning solution approach tailored to {row['competency_name']} at a {required_level_description} proficiency level. Consider that {row['rumpun_jabatan']} as a job family. Consider difficulty of the solution to fit for {required_level_description} proficiency level."
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
        required_level_description = proficiency_levels.get(row['required_level'])
        prompt = f"What are the relevant key outlines or latest essential knowledge or paradigm that I will acquire for the competency {row['competency_name']} at the {required_level_description} proficiency level? List in 1 Title learning and 5 point of brief outline. Make the outline simple (just one line)"
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

def analyze_competency_gap(file_path):
    data = pd.read_excel(file_path)
    average_aggregate_req = data['required_level'].mean()
    rounded_average_aggregate_req = min(max(round(average_aggregate_req), 1), 5)
    proficiency_level_req = proficiency_levels[rounded_average_aggregate_req]

    average_aggregate_curr = data['current_level'].mean()
    rounded_average_aggregate_curr = min(max(round(average_aggregate_curr), 1), 5)
    proficiency_level_curr = proficiency_levels[rounded_average_aggregate_curr]

    prompt = f"Based on the analysis of competency gaps in the organization, the average required level across all competencies is {proficiency_level_req} level but average current level across all is {proficiency_level_curr} Level. Please provide a summary in single paragraph of the current condition (is Low Risk, Moderate Risk, Elevated Risk, High Risk, or Sever Risk) and impact of this competency gap on the organization as an Indonesia Port Maritime Corporation. Please show in Uppercase the status in the first paragraph."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200
    )

    return response.choices[0].text.strip()

file_path = 'learning_recommendations.xlsx'
summary = analyze_competency_gap(file_path)
summary_df = pd.DataFrame({'Summary': [summary]})

summary_file_path = 'LNA_Summary.xlsx'
summary_df.to_excel(summary_file_path, index=False)

files.download(summary_file_path)
