# Interview Case for Entropic

The purpose of this repository is to contain the interview assignment as well as proposed solutions for the AI research intern position at Entropic. Below, you will first find the case itself. Afterwards, you can find the solution, different files, as well as the reasons for choosing specific methods.

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

Starting with the the scraper, we use Beautifulsoup to parse the html content. After examining the code of the website, we saw that all the projects are under the "article" tag, therefore we used that to find each projects. The title and hyperlink for each project was collected. The link was then used to further scrape each individual project.

I started by initializing the values present in almost every project (**code, status. start date, description**). We then extract theys using the corresponding keys in the entry-meta div.