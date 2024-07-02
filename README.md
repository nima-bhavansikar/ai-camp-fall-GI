# mo-chen
A repository for Mo's Data Dashboard. AI Camp Guided Internship 2023. 

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#product-spec">Product Spec</a></li>
  </ol>
</details>

## Setup

### 1. Download the projects zip file and save it to your desired location.
### 2. Navigate to the project file in the terminal
```sh
$ cd link/to/file/path/
```
### 3. Setup Virtual Environement
```sh
$ python3 -m venv .venv
```
To activate the Virtual Environement:
```sh
$ source .venv/bin/activate
```
To deactivate the Virtual Environement:
```sh
(.venv) $ deactivate
```
### 4. Install django:

```sh
(.venv) $ python3 -m pip install django~=4.2.0
```
### 5. Migrate and Run the Server:
```sh
(.venv) $ cd backend
(.venv) $ python3 manage.py makemigrations
(.venv) $ python3 manage.py migrate
(.venv) $ python3 manage.py runserver
```
## Product Spec

### Problem/Opportunity

Data analysis is a skill of growing importance. It can help drive innovation and optimization in technology. Data analysis also plays a crucial role in the training and improvement of AI algorithms. The aim of EDA, or Exploratory Data Analysis, is to investigate and understand the underlying patterns, trends, and characteristics of a dataset. It involves analyzing and visualizing the data to gain insights, identify anomalies, and formulate hypotheses before formal modeling or statistical testing. Not many people know how to use EDA, so we have an opportunity to create a platform that can teach beginners the fundamentals. EDA is an important step of data analysis, as it helps researchers and machine learning engineers to identify critical information in a dataset that can be used to train a Machine Learning model.

### Our Solution

A feature-rich website that allows the audience to delve deeper into exploratory data analysis (EDA), create interactive visualizations, and share their work with an online community, without having to download anything. The site's contents will include a guided tutorial covering the fundamentals of EDA and visualization techniques using Python code with coding blocks mixed in to allow users to practice what they learn as they learn it, instead of treating it like a textbook. There will also be an embedded programming environment where users can input, manipulate, and analyze datasets, and create visualizations so that students don’t have to download any other software to complete the work.  There should be a variety of different real-life datasets to choose from. Topics for possible datasets include credit card approval data, risk assessment, stock information, jobs, etc. There should be three different and unique datasets. 

### Our Target Audience

People ages 18-44 or beginners of EDA with an interest in data analysis

### Success Metrics

- XX% of people who start the course finish it (shows the course is engaging)
- The course takes XX hours on average to complete (is accessible to busy people)
- The tutorial must be comprehensive but easy to understand

### MVP (Minimum Viable Product)

- Having a website
    - Allow users to login
    - Store users’ progress in their course
    - Have a course with information on EDA as well as a sandbox area/code blocks to be interactive
    - Have 1 dataset that people can use for the course, each with a course to guide users through them (we’ll have three in total by this team that will be WIP)
- Make the Website look good aesthetically
    - Make sure that themes are consistent across the website
    - Light/Dark Mode theme

