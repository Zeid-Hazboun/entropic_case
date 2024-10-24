# Interview Case for Entropic

The purpose of this repository is to contain the interview assignment as well as proposed solutions for the AI research intern position at Entropic. This solution focuses on helping Entropic achieve its mission of decarbonizing industrial heat by creating an automated system to classify and summarize relevant case studies. The approach balances both accuracy and interpretability while ensuring efficiency. Below, you will first find the case itself. Afterwards, you can find the solution, different files, as well as the reasons for choosing specific methods.

## Case

### Introduction

At Entropic, our mission is clear: decarbonize industrial heat, responsible for 20% of worldwide CO2 emissions. We’ve built a project development platform that reduces the cost and complexity of decarbonization projects. Using digital twins and an innovative marketplace, we streamline energy optimization for factories worldwide, making sustainable solutions fast and accessible. Our vision is to create a global ecosystem that empowers industries to decarbonize efficiently, from chemicals to pharmaceuticals.

### **Problem Statement:**

You are tasked with creating a small system to **scrape case studies** related to "decarbonization of industrial heat" from a publicly available website. After scraping, the system should:

1. **Classify the case studies based on relevance** (using keywords or technologies you define).
2. **Generate a brief summary** of the most important insights from the relevant case studies.

If you have any questions you can send a message to the email address provided below.

### **Steps**:

1. **Web Scraping**:
    - Scrape case study content from the following website: [ISPT - Decarbonization of Heat Case Studies](https://ispt.eu/projects/?theme-tag=heat).
    - Use any web scraping tools or libraries you find appropriate
2. **Data Processing**:
    - Clean and organize the scraped content to ensure it is structured and usable.
3. **Classification**:
    - Create a simple system to classify the case studies as relevant or irrelevant based on specific criteria. You are free to define these criteria (e.g., keywords related to technologies, temperature ranges, industry types, etc.).
4. **Summarization**:
    - Use a language model or an NLP technique (e.g., pre-trained models like GPT or summarization algorithms) to generate brief summaries of the relevant case studies.

### **Requirements**:

- **Add explanations**. Inline comments explaining key decisions are encouraged.
- **Documentation**: Provide clear documentation that explains how to run the code and outlines the reasoning behind your approach.
- **Creativity**: Show creativity in selecting and using tools or techniques to solve the problem efficiently.

### **Submission Instructions**

- Please submit your code by either:
    1. Sharing a GitHub repository link.
    2. Sending a zip file containing your project.
- Send your submission to: **mwkrijgsman@geothermelectric.com**
- We will review your submission and inform you of the next steps shortly.

Good luck and have fun! 😁

---

## Solution

Other than the requirements in the pyproject.toml file, there are no requirements to run the solutions. **You only need to change the file paths, since it is using the full path instead of the relative path. Places where this should be done with have the comment "#change file path to local one" for ease**

I have also left the data in the repository (`data/`) instead of adding it to the `.gitignore file`, so you would not have to rerun the program/if you wanted to see specific talking points mentioned in this file. 

### Scrapper

Starting with the the scraper (`scraper.py`), we use Beautifulsoup to parse the html content. After examining the code of the website,We saw that all the projects are under the 'article' tag, so we used this to identify each project. The title and hyperlink for each project was collected. The link was then used to further scrape each individual project.

I started by initializing the values present in almost every project (**code, status. start date, description**). We then extract the information using the corresponding keys in the 'entry-mete' div. Afterwards, we extract the description from the 'entry-content' div. This information is then placed in a csv sheet which will then include the **project_title, link, code, status, start_date,** and **description**.

### Data Preprocessing

For data-preprocessing and cleaning (`data_preprocessing.ipynb`), several libraries/methods were chosen such as regex, nltk, scikit-learn and gensim.

First step was removing the end section of each description. The web pages have a section of other items that a user might be interested in. This always starts as "You might also be interested in...", and so that was the cutoff phrase. Once that was done, more typical data cleaning was done using regex and nltk (removing punctuation, stopwords, lowercase only, excessive whitespaces, and special characters). The new processed description was then tokenized. As an extra precaution, I extracted the bigrams since they could be useful in the future for topic classification or modeling. 

#### TF-IDF

My solution to filter the topics was based on using keywords in combination with tf-idf, and then scoring the topics based on the combined tf-idf values present in the matrix pf these topics. I believe this to be a more time efficient solution that requires less understanding of the core concepts of decarbonization of industrial heat. The following are the list of keywords used after some researching of the topic: **['decarbonization', 'carbon', 'emissions', 'industrial heat', 'renewable', 'capture', 'electrification', 'reduction', 'emission', 'industrial', 'sustainability', 'co2', 'waste', 'heat recovery', 'waste heat', 'thermal efficiency', 'heat pump','zero-emission']**. 

Once the scores were computed, we can see that there seems to me a natural threshold point around 0.5, so that was chosen as the threshold. If we wanted to be more lenient, the threshold could be lowered easily. A new CSV file was created that only includes the projects above the threshold.

Other ideas to tackle the filtering problem included using BERT topic modelling and LDA. The reason for not doing them is that I believe topic modelling using BERT might require more of a core understanding of the topic to recognize the correct topics, as well as topics might be grouped together based on different characteristics (the language of completed topics vs ongoing and so on). 

LDA would require more post-processing to determine the concrete relevance of each topic, adding complexity without necessarily improving the quality of the classifications. A keyword-based or TF-IDF-based approach provides a faster, more straightforward way to score the relevance of each project. This approach gives more interpretable and actionable insights by ranking projects based on specific terms related to the field of decarbonization, allowing for a clearer understanding of the relevance of each project.

## Summarizing using an LLM
For the last part of the case, I had to use an LLM to generate a brief summary of the filtered cases. There were many to choose from, but I chose to use [Pegasus](https://huggingface.co/docs/transformers/en/model_doc/pegasus). There were multiple reasons for doing so, but the main reason I chose Pegasus for summarization is due to its state-of-the-art performance on abstractive summarization tasks, particularly for formal text such as case studies. It consistently outperforms other models like GPT-2 and T5 in terms of generating coherent, human-readable summaries, especially when dealing with lengthy technical documents. Here is an example of the performance I previously computed according to [ROGUE](https://en.wikipedia.org/wiki/ROUGE_(metric)) with the `"ccdv/cnn_dailymail", version="3.0.0"` dataset. 

| Model    | rouge1  | rouge2  | rougeL  | rougeLsum |
|----------|---------|---------|---------|-----------|
| baseline | 0.303571| 0.090909| 0.214286| 0.232143   |
| gpt2     | 0.222222| 0.045455| 0.111111| 0.200000   |
| t5       | 0.524590| 0.237288| 0.426230| 0.491803   |
| bart     | 0.487179| 0.157895| 0.307692| 0.435897   |
| pegasus  | 0.866667| 0.655172| 0.800000| 0.833333   |

The descriptions in the filtered csv file were used to generate the summaries. The original descriptions were used, instead of the pre-processed descriptions. This is because the lack of stopwards and punctuation caused the consequent summary to not be coherent. Here is an example of the same summary, one made according the cleaned description and the other by the orignal description in one of the trials.

* **Cleaned**: 'Two virtual public simulation case simulationas enable partner share promote expertise without disclose confidential information.\nGoal is to develop innovative process design solving efficient flexible electrification challenge .'


* **Original**: 'Electrification of heat-driven processes is needed for a substantial reduction of CO 2 emissions.\nThe challenge is to efficiently move to full electrification while coping with the high variability of the availability and price of electricity.\nThis project will develop potential routes based on available technologies through two virtual public simulation cases .'

We can see that the second summary is much more coherent and readable than the first, and therefore we used the original description for the rest of the summaries. Examining the length of the summary, we can see that it had a length of 480 words, while the original description had 3860 words.

After generating the summaries, I decided to also compute the ROGUE metric for the summaries.

| Index | rouge1  | rouge2  | rougeL  |
|-------|---------|---------|---------|
| 0     | 0.218935| 0.207715| 0.218935|
| 1     | 0.153846| 0.145560| 0.153846|
| 2     | 0.395062| 0.362500| 0.395062|
| 3     | 0.169492| 0.160742| 0.169492|

* ROUGE-1: Measures the overlap of unigrams (single words) between the generated summary and the reference. Higher values indicate better coverage of the key words.

     * In this table, the ROUGE-1 scores range from 0.153846 to 0.395062, meaning that around 15% to 39% of the unigrams from the reference texts are captured in the generated summaries.
*   ROUGE-2: Measures the overlap of bigrams (two consecutive words) between the generated summary and the reference. This is a stricter metric than ROUGE-1, as it accounts for word sequence.

    * ROUGE-2 scores here range from 0.145560 to 0.362500, which indicates that 14% to 36% of the two-word sequences from the reference texts appear in the generated summaries.
* ROUGE-L: Measures the longest common subsequence between the generated summary and the reference text. This captures the structural similarity of the sentences, focusing on recall and precision at a higher level.

    * ROUGE-L scores range from 0.153846 to 0.395062, meaning that the generated summaries retain about 15% to 39% of the structure found in the original text.

The summaries are capturing some key points, but the overall performance could be improved, especially in terms of capturing bigrams and sentence structure (as seen in ROUGE-2 and ROUGE-L)

Now that the summaries were generated and examined, I also generated the summaries for the rest of the topics, just incase you were curious as to the performance in the rest of the summaries.


## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Poetry** (if you don’t have it already):
   Poetry is used to manage dependencies and virtual environments. You can install it from [Poetry's official site](https://python-poetry.org/docs/), or use this command:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   Run the following command to install the project’s dependencies:
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:
   After installing dependencies, activate the Poetry-managed virtual environment:
   ```bash
   poetry shell
   ```

5. **Run the scraper**:
   Run the scraper to collect project data:
   ```bash
   python scraper.py
   ```

6. **Run the data preprocessing**:
   Open and run the preprocessing notebook:
   ```bash
   jupyter notebook data_preprocessing.ipynb
   ```

7. **Run the summarizer**:
   Summarize the filtered case studies by running the summarizer notebook:
   ```bash
   jupyter notebook summarizer.ipynb
   ```

8. **Deactivate the virtual environment**:
   Once done, you can exit the Poetry shell:
   ```bash
   exit
   ```

## Conclusion

This project successfully implements a system to scrape, classify, and summarize case studies related to the decarbonization of industrial heat. By leveraging modern NLP techniques, such as TF-IDF for classification and Pegasus for summarization, the solution provides efficient and explainable results. Future improvements could involve fine-tuning the summarization model for domain-specific text and exploring more advanced classification techniques (possibly training a model of its own to classify this if enough data is available).
