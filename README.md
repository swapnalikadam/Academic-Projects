I implemented a Data Visualization project using three datasets (landscaping.csv, employees.csv, and calendar.csv) to identify opportunities for improving our landscaping company. Before starting visualizations, I set two sub-goals:

##Goal 1: Understand which job types contribute to higher customer satisfaction.

##Goal 2: Explore the number of days employees worked to enhance productivity and customer satisfaction.

The four visualizations are as follows:

Explanatory Visualization:
Explores job types that yield high and low customer satisfaction.
Assumption: Customer satisfaction < 5 is poor, > 5 is good.

Interactive Visualization:
Investigate if the time gap between job request and start date affects customer satisfaction for specific jobs (Retaining Wall and Water Feature).
Features a dropdown for users to select job types for comparison.

Visualization with Derived Data:
Introduces "Employee Productivity" as derived data.
Utilizes a Scatter plot to analyze the correlation between the number of days worked, employee wages, and productivity.

Exploratory Visualization:
Presents a Tree Map illustrating the number of jobs completed by each employee.
Two inquiries viewers can make:

1. Evaluate whether high job volume correlates with poor customer satisfaction, indicating potential employee overload.
2. Compare customer satisfaction between employees with the most and least jobs to identify factors influencing satisfaction levels.

These visualizations aim to provide actionable insights for company improvement, focusing on customer satisfaction and employee productivity. 

The technologies I utilized include Pandas and NumPy for efficient data handling and numerical operations in analyzing landscaping company data. Matplotlib and Seaborn were employed to create insightful plots, uncover data patterns, optimize performance, and evaluate customer satisfaction. I incorporated Squarify for hierarchical data representation through tree maps. IPyWidgets facilitated interactive dropdowns for customized visualizations. Additionally, Plotly proved valuable for crafting dynamic and interactive plots and dashboards, offering versatility in data exploration.

