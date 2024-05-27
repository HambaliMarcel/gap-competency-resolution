# Gap-Competency-Resolution

This repository demonstrates a proof of concept (PoC) for resolving competency gaps using AI-driven recommendations. By analyzing Learning Needs Analysis (LNA) scores, the system prioritizes competencies and provides tailored learning solutions to address them effectively.

### Overview

The script provided in this repository performs the following tasks:
1. Merges LNA master data with LNA scores.
2. Uses GPT-3.5-turbo-instruct to generate learning recommendations and relevant learning topics for each competency.
3. Outputs the results to an Excel file for further analysis and implementation.

### Prerequisites

- Python 3.x
- Pandas library
- OpenAI library
- Google Colab for file downloads (optional)
- LNA master and LNA score data in CSV format

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gap-competency-resolution.git
   cd gap-competency-resolution
   ```

2. **Install the required libraries:**
   ```bash
   pip install pandas openai
   ```

3. **Prepare your LNA data:**
   - Ensure you have `lna_master.csv` and `lna_score.csv` files in the repository directory.

4. **Set up your OpenAI API key:**
   - Replace the placeholder API key in the script with your actual OpenAI API key:
     ```python
     api_key = "your_openai_api_key_here"
     ```

### Usage

1. **Run the script:**
2. **Download the output file:**
   - After the script runs, download the generated `learning_recommendations.xlsx` file which contains the recommended learning solutions and topics.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### Acknowledgements

- OpenAI for providing the GPT-3.5-turbo-instruct model.
- Pandas library for data manipulation.
- Google Colab for file handling.

---

Feel free to customize this README file as per your project's specific requirements and structure.
