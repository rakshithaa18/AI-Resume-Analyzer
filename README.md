#  AI Resume Analyzer

An intelligent resume screening platform that helps job seekers optimize their resumes and assists recruiters in identifying the best-fit candidates through automated skill matching and resume analysis.

## Problem Statement

Recruiters receive hundreds of resumes for a single job opening, making manual screening time-consuming and inefficient. Candidates often struggle to understand why their resumes are rejected by ATS systems.

## Solution

AI Resume Analyzer automatically compares a candidate's resume with a target job role, identifies missing skills, calculates a match score, and provides actionable suggestions to improve employability.

## Key Features

✅ Resume Upload (PDF/DOCX)

✅ Automated Resume Text Extraction

✅ Job Role-Based Skill Matching

✅ Resume Match Score Calculation

✅ Missing Skills Detection

✅ Personalized Improvement Suggestions

✅ Downloadable Analysis Report

✅ Fast and User-Friendly Interface

## Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI

### Programming Language
- Python

### Libraries Used
- pdfplumber
- docx2txt
- requests
- fpdf
- pydantic

## Architecture

Resume Upload
      │
      ▼
Text Extraction
      │
      ▼
Skill Analysis Engine
      │
      ▼
Role Matching Algorithm
      │
      ▼
Score Generation
      │
      ▼
Suggestions & PDF Report


## Innovation

- Provides instant resume evaluation.
- Detects skill gaps based on target job roles.
- Helps candidates align resumes with industry expectations.
- Reduces recruiter screening effort through automated analysis.

## Impact

- Saves recruiter screening time.
- Improves candidate resume quality.
- Enhances job-role alignment.
- Supports faster hiring decisions.

## Future Scope

- ATS Compatibility Scoring
- AI-Powered Resume Rewriting
- Job Description Upload Support
- LLM-Based Feedback System
- Candidate Ranking Dashboard
- Recruiter Analytics Portal

## Installation

pip install -r requirements.txt

### Run Backend

uvicorn Backend:app --reload

### Run Frontend

streamlit run app.py

## Team

### Team Name
CodeSquad

### Members
- Rakshitha S
- Akshaya HR
- Ayisha Nisma
- Mahima

## Hackathon Submission

**Project Name:** AI Resume Analyzer

**Theme:** AI for Career Development & Recruitment

**Built With:** Python, FastAPI, Streamlit

---
 Transforming Resume Screening with AI
