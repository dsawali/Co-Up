## Project: CO_OP_US
This application aims to bring together students seeking help with pursuing co-op opportunities and students willing to share their co-op experiences.

Students, who have done co-op previously, can list positions held for other students to see.

Students seeking help with co-op can browse through recently added position or search for a
specific company/position they are interested in. Once found, they can contact people for more information about their co-op experiences.


## Project Folder Structure:
Project repository for COUP

High level files (e.g., requirements.txt, README.md, .gitignore, etc) are included at final_project/

Django configuration files (e.g., urls.py, settings.py, wsgi.py, etc) are found in final_project/config/settings/

Django non-configuration files (e.g., apps, templates) are found in final_project/coup/
    - actions
    - api
    - common
    - conversations
    - core
    - dashboard
    - fixtures
    - media
    - positions
    - search
    - static
    - templates
    - user_auth
    - users

------------------------------------

## Getting Started
1. vagrant up
2. Open a browser and go to http://localhost:8080
3. You will be redirected to http://localhost:8080/user_auth/login/
3. Create an account or login with a test account () to navigate the application

---------------------------------

## Accessing the application
 - Option one: Create a New Account
    1. Click on the Signup link from the Login page or go to http://localhost:8080/user_auth/signup/
    2. Once account is created, you will be prompted to Login.

 - Option two: Login with Existing Account
    1. From the Login page, enter your information
    2. If correct, you will be logged in and redirected to Dashboard
    3. If incorrect, you will be prompted to try again.

_Note: admin page can be accessed with **username: admin** , **password: adminadmin**_

-----------------------------------------------------------------------------------------------------

## Dashboard
  - This is a landing page once logged in
  - Navigation Bar across the top of the page displays different links for easy site navigation

-----------------------------------------------------------------------------------------------------

## Profile
Every user is encouraged to update their profile with relevant information:
- Full Name
- Faculty/Program they are studying
- Profile Picture  
- Previous co-op experience can be added by following "Update" link next to Your Positions
  - This will take the user to the Positions tab (see below)

Other users' profiles:
  - Shows other user's information along with previous co-op positions held
  - From here users can be Followed or a Conversation can be started

-----------------------------------------------------------------------------------------------------

## Messages
Allows users to create "chatrooms" for desired groups of people
Each Group can have many Conversations

Messages tab is separated into three subsections: Overview, Conversations, and Groups
Overview section is all-in-one view of all groups and conversations.
- Create a group
  1. Clicking on "New Group"
  2. Fill out group's information and add ALL desired users (including yourself)

- Edit a group
  1. Click on "Edit Groups" and choose a group to edit
  2. Change information and Submit

- Start Group Conversation(s)
  1. Click on "New Conversation"
  2. Choose a group for which to create a conversations
  3. Write a Subject for the conversation and Submit

- Access existing Conversations and Post Messages
 1. Select a group from the list
 2. All available conversations for that group will appear
 3. Select the desired one
 4. Earlier posts (if available) will be displayed
 5. Compose a new message in the area provided and press Send
 6. Messages will be accessible by all group members

Conversations and Groups sections allow to zoom in on specific functionalities for quicker access.
-----------------------------------------------------------------------------------------------------

## Positions
Information under this tab is divided into two sections:
- You Positions
  1. Lists all positions added for user's profile
  2. New positions can be added via "Add New Position" link
  3. "Find Position" link will take the user to the Search by Position section (see below)

- Recently Added positions (added by all users)
  1. Displays a list of recently added positions application-wide
  2. Users' profiles can be accessed by pressing on a Username in each posting
  3. From there, users can be Followed or a Conversation can be started

-----------------------------------------------------------------------------------------------------

## People
This tab is separated into two sections:
1. Following You:
  - Displays a list of all people following you at the moment

2. Followed by You:
  - Displays a list of all people you decided to follow
  - This essentially works like bookmarking people you found useful for future reference

-----------------------------------------------------------------------------------------------------

## Search
1. Search for a specific Position
  - Returns a list of co-op position taken by students that satisfy the criteria
  - Google Maps is integrated for easier search

2. Search for User
  - Returns all users satisfying the search criteria
  - Each user's profile can be accessed by pressing on their username/link

------------------------------------------------------------------------------------------------------

## Logout
1. Click on the user dropdown menu in the right top corner.
2. Number of options will be displayed
3. Click on Logout

------------------------------------------------------------------------------------------------------
