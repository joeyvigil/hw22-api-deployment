# hw22-api-deployment
In this lesson you will be creating your own CI/CD Pipeline as we did in class (Feel free to follow along in the recording). 

## You will
-   Host a database to Render
-   Create your production config
-   Install gunicorn psycopg2 python-dotenv (freeze to your requirements.txt and manually remove python-dotenv)
-   Store sensitive information as an environmental variable in your .env file (database uri and secret key)
-   add .env to your .gitignore
-   Use the os package to retrieve those environmental variable
-   Rename app.py to flask_app.py
-   Pass your ProductionConfig into your create_app function inside flask_app.py
-   Remove app.run() from flask_app.py
-   Push to your github repository
-   Deploy a Web Service on Render using the link to your github repository (make sure to add your environment variables during the deploy process).
-   After successful deployment adjust your swagger documentation host from 127.0.0.1:5000 to the base url of your live API (base url should not include https://)
-   Change your swagger schemes from http to https

## CI/CD Pipline:
-   Create .github folder with a workflows folder inside
-   Create a main.yaml file inside the workflows folder.
-   In the main.yaml file create a workflow including:
-   ---- name: name of workflow
-   ---- on: trigger for workflow
-   ---- jobs: Create the build and test jobs 
-   Store the Render SERVICE_ID and RENDER_API_KEY as secrets in your github repository
-   Set up the deploy job in your .github/workflows/main.yaml and make it dependant on the test job needs: test

## Submission:
After deploying submit the link to your deployed service as well as the the link to your github repository.