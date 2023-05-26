# student_recipes_DjangoApp

## Project Description
"Recipes for Students" is a web application developed in Django by a 5-member team following the Agile methodology and SCRUM framework. The project aims to provide a user-friendly platform for students to discover, share, and contribute to a collection of affordable and easy-to-make recipes.

The application allows students to browse through a wide variety of recipes specifically curated for their needs, considering factors such as budget constraints, limited time, and minimal cooking equipment. Users can create an account, save their favorite recipes, and even submit their own recipes to share with the community.

Key Features:

- User registration and authentication system
- Recipe browsing and searching functionality
- Recipe submission and sharing capabilities
- Ability to save favorite recipes for future reference
- Categorization of recipes based on dietary preferences or cuisine types
- Interactive user interface with a clean and intuitive design

The team follows the Agile methodology to ensure regular collaboration, feedback, and iterative development. SCRUM is employed for effective project management, including sprint planning, daily stand-ups, sprint reviews, and retrospectives.

By leveraging the power of Django, the team has built a robust and scalable web application that caters specifically to the culinary needs of students, making cooking an enjoyable and hassle-free experience.

## Team Members
* Gabriel Sawicki - Scrum Master / Backend Developer
* Qiuyu Huang - Product Owner
* Ada Bilska - Frontend Developer
* Nicholas Lambert - Backend Developer
* Shane Waters - Database Designer and Tester

## System Requirements
Before getting started with the "Recipes for Students" application, make sure you have the following software installed:

- Python 3.10
- Django 4.0.2
- Other dependencies listed in the requirements.txt file

## Installation
1. Clone this repository to your local machine:

`git clone https://github.com/your-username/recipes-for-students.git`

2. Navigate to the project directory:

`cd recipes-for-students`

3. It is recommended to create a Python virtual environment. You can do this using the virtualenv tool:

`python3 -m venv env`

4. Activate the virtual environment:

- For Windows:

`env\Scripts\activate`

- For Unix/Linux:

`source env/bin/activate`

5. Install the required Python libraries:

`pip install -r requirements.txt`

6. Apply the database migrations:

`python manage.py migrate`

7. Start the Django development server:

`python manage.py runserver`

8. The application should now be accessible at http://localhost:8000 in your browser.

## Configuration
To configure the application according to your needs, you can modify certain settings. Open the recipes/settings.py file and modify the relevant variables.

## Contributing
If you would like to contribute to the project, you can follow these steps:

1. Fork this repository and clone your copy to your local machine.
2. Create a new branch for your changes:

`git checkout -b my-changes`

3. Make your changes and commit them:

`git commit -m "Description of changes"`

4. Push your changes to your GitHub repository:

`git push origin my-changes`

5. Create a pull request in the original repository.
