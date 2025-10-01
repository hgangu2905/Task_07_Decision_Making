# Raw LLM Outputs (Task 7)

This file contains the raw prompts and outputs from Claude used during Task 7.  
They are included for transparency. Key claims were validated against descriptive statistics, bootstrap uncertainty intervals, and fairness metrics.

---

## Initial Conversation

**User Prompt:**  
"I'm working on a research task where I analyze student performance data. I’ll ask you some questions based on the data. Here's the dataset: Attached the dataset."

**Claude Response (excerpt):**  
"I can see you've provided a student performance dataset with information about gender, race/ethnicity, parental education level, lunch type, test preparation course completion, and scores in math, reading, and writing… The dataset contains 1,000 student records… What aspects of the student performance data are you most interested in analyzing?"

---

## Question Set 1

**User Prompts:**  
1. How many students are there in the dataset?  
2. What is the average math score?  
3. What is the average reading score?  
4. What is the average writing score?  
5. Which subject had the highest average score among students?  
6. How many students completed the test preparation course?  
7. What are the average total scores of male and female students?  
8. How many students scored a total below 150?  
9. What are the three performance categories used to classify students?  
10. How many students fall into each performance category?  

**Claude Response (excerpt):**  
- Dataset size: **1,000 students**  
- Math mean: **66.1**  
- Reading mean: **69.2**  
- Writing mean: **68.1**  
- Highest subject: **Reading (69.2)**  
- Test prep completion: **358 students (35.8%)**  
- Avg total: Male = **201.4**, Female = **204.9**  
- Below 150 total: **102 students**  
- Performance categories: High ≥240, Average 180–239, Low <180  
- Distribution: High = **273**, Average = **525**, Low = **202**  

---

## Question Set 2

**User Prompts:**  
1. Which parental education group has the highest average total score?  
2. Who benefits more from test preparation — males or females?  
3. Which subject shows the most variation in student performance?  
4. Which group (by race/ethnicity) has the highest average writing score?  
5. If I want to increase the number of “Excellent” students, which performance category should I focus on and why?  

**Claude Response (excerpt):**  
- Highest parental education: **Master’s degree (219.3 avg total)**  
- Test prep benefit: **Females (+15.4) > Males (+14.2)**  
- Most variation: **Math (std dev 15.2)**  
- Highest writing score: **Group E (71.4)**  
- Strategic focus: **High Performance students (240–269)** since they need fewer points to reach Excellent.  

---

## Notes  

- These raw outputs guided the Stakeholder Report but were **not used directly without validation**.  
- All statistics cited from Claude were cross-checked against Python scripts in `scripts/` and results in `outputs/`.  
- Any differences in thresholds (e.g., Claude’s High/Average/Low vs. our Failing/Average/Excellent) were noted and harmonized for consistency.  
