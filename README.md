## SECTION 1 : PROJECT TITLE
## Dog Breed Detective

<img src="SystemCode/dogDetectiveProject/static/images/preview pic.jpg"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
COVID-19 pandemic has created massive disruptions to businesses around the world and businesses are forced to take an aggressive stance toward reducing operation overheads and increasing their profitability  in order to survive. However, the pandemic has not only brought about lower profitability, but it has also increased the outflow of skilled professionals. The pet industry is no different from the rest of the business and has met with similar fate with the rest of the industry.  As we emerge from the crisis, the pet industry is now seeking innovative solutions to enhance productivity and rebuild their operations for sustained growth and promote resiliency into their business.


Pet owners on the other end of the equation face the same issues of getting reliable information and products in the midst of the pandemic as pet business faces the shortage of manpower and logistics constraints. This brought about an increase in cases of pets’ abandonment and disownment as pet owners feel the hassle of keeping their pets. It turns the enjoyment of owning a pet into a nightmare when pets’ owners struggle to provide daily care for their pets.

The project team understands these pain points and is promoting a web application to reduce the dependency on the skilled and experienced staff of the pet industry to provide sound advice to the pet owners while pet owners could readily find reliable information they require despite the shortage of staff within the pet industry. 


The first step of the solution to create a Minimum Viable Product (MVP) for the recognition of dog breed as the first iteration. This will enable the application to provide details of the dog which the owner requires. Once the recognition of the dog breed is complete, the solution will provide first a brief description of the dog so that the owner would understand more about the dog. Secondly, the solution will provide insights from an established source on the different aspects of the dog breed such as the activeness, health, maintenance cost etc. 

This will provide prospective dog owners with information so that they know about the essential upkeep that comes along with the dog. This is to manage their expectation so that they could be well prepared if they would proceed to get the dog breed they have selected. The team hopes that in this case, this will reduce the number of disownments of pets as the owners are well-informed of their pet’s upkeep. 

For seasoned dog owners, the team hopes to provide new insights based on the insights provided by the application as some of this information might be unknown to these seasoned dog owners. Moving forward, the project team also hopes to add in more functionalities for these seasoned dog owners such as pet product recommendation, illness symptoms identification to provide an all rounded experience for these dog owners. 

The team will be using the techniques and knowledge acquired from the Graduate Certificate in Intelligent Reasoning System to build the MVP. The team will be employing the techniques in designing the system using a Frame Based system approach. The team will then be implementing the CRISP-DM approach in building the image recognition and recommender model for this MVP. The approach will consist of the evaluation of the best model for the MVP. The team has concluded from the evaluation that the optimum algorithm is using the Convolutional Neural Network (CNN). This enables high accuracy to be attained by the system and meet the success factor identified by the project team. 

The team will also be deploying a recommender system to recommend similar dog breeds to prospective dog owners. This recommender will be built by using the euclidean similarity algorithm to match the dog breed which was uploaded by the prospective dog owner against a list of dog breeds with similar aspects on the daily upkeep. 

The project team is confident that with this MVP, it will be able to provide the dog owners with the essential information they require and reduce the reliance on the experienced pet shop staff while the pet store owners will be able to achieve higher customer satisfaction and retention despite in the reduction of manpower due to the outflow of experience staff.  This will create a win-win situation for users at both sides of the equation.
 

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Item Contribution | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Tan Chee Wei | A0230818H | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A1234567A@nus.edu.sg |
| Aloysius Ong Jun Long | S****702J | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A1234567B@gmail.com |
| Goh Zhi Hui | A0269364R | 1. Image pre-processing<br/>2. Object Detection in Image<br/>3. CNN modelling<br/>4. API integration<br/>5. Frontend development E1112235@u.nus.edu |
| Chen Yihan Johaness | A0214926A | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A1234567D@yahoo.com |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[![Sudoku AI Solver](http://img.youtube.com/vi/-AiYLUjP6o8/0.jpg)](https://youtu.be/-AiYLUjP6o8 "Sudoku AI Solver")

Note: It is not mandatory for every project member to appear in video presentation; Presentation by one project member is acceptable. 
More reference video presentations [here](https://telescopeuser.wordpress.com/2018/03/31/master-of-technology-solution-know-how-video-index-2/ "video presentations")

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

### [ 1 ] To run the system using iss-vm

> download pre-built virtual machine from http://bit.ly/iss-vm

> start iss-vm

> open terminal in iss-vm

> $ git clone https://github.com/telescopeuser/Workshop-Project-Submission-Template.git

> $ source activate iss-env-py2

> (iss-env-py2) $ cd Workshop-Project-Submission-Template/SystemCode/clips

> (iss-env-py2) $ python app.py

> **Go to URL using web browser** http://0.0.0.0:5000 or http://127.0.0.1:5000

### [ 2 ] To run the system in other/local machine:
### Install additional necessary libraries. This application works in python 2 only.

> $ sudo apt-get install python-clips clips build-essential libssl-dev libffi-dev python-dev python-pip

> $ pip install pyclips flask flask-socketio eventlet simplejson pandas

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

**Recommended Sections for Project Report / Paper:**
- Executive Summary / Paper Abstract
- Sponsor Company Introduction (if applicable)
- Business Problem Background
- Market Research
- Project Objectives & Success Measurements
- Project Solution (To detail domain modelling & system design.)
- Project Implementation (To detail system development & testing approach.)
- Project Performance & Validation (To prove project objectives are met.)
- Project Conclusions: Findings & Recommendation
- Appendix of report: Project Proposal
- Appendix of report: Mapped System Functionalities against knowledge, techniques and skills of modular courses: MR, RS, CGS
- Appendix of report: Installation and User Guide
- Appendix of report: 1-2 pages individual project report per project member, including: Individual reflection of project journey: (1) personal contribution to group project (2) what learnt is most useful for you (3) how you can apply the knowledge and skills in other situations or your workplaces
- Appendix of report: List of Abbreviations (if applicable)
- Appendix of report: References (if applicable)

---
## SECTION 7 : MISCELLANEOUS

`Refer to Github Folder: Miscellaneous`

### HDB_BTO_SURVEY.xlsx
* Results of survey
* Insights derived, which were subsequently used in our system

---

### <<<<<<<<<<<<<<<<<<<< End of Template >>>>>>>>>>>>>>>>>>>>

---

**This [Machine Reasoning (MR)](https://www.iss.nus.edu.sg/executive-education/course/detail/machine-reasoning "Machine Reasoning") course is part of the Analytics and Intelligent Systems and Graduate Certificate in [Intelligent Reasoning Systems (IRS)](https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "Intelligent Reasoning Systems") series offered by [NUS-ISS](https://www.iss.nus.edu.sg "Institute of Systems Science, National University of Singapore").**

**Lecturer: [GU Zhan (Sam)](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan "GU Zhan (Sam)")**

[![alt text](https://www.iss.nus.edu.sg/images/default-source/About-Us/7.6.1-teaching-staff/sam-website.tmb-.png "Let's check Sam' profile page")](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan)

**zhan.gu@nus.edu.sg**
