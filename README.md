<h1 align="center">
  <img src="https://user-images.githubusercontent.com/2679513/131189167-18ea5fe1-c578-47f6-9785-3748178e4312.png" width="150px"/><br/>
  Speckle | AEC Tech Masterclass
</h1>
<h3 align="center">
    A Speckle app to compare different commits and visualize the results
</h3>
<p align="center"><b>Speckle</b> is data infrastructure for the AEC industry.</p><br/>

<p align="center"><a href="https://twitter.com/SpeckleSystems"><img src="https://img.shields.io/twitter/follow/SpeckleSystems?style=social" alt="Twitter Follow"></a> <a href="https://speckle.community"><img src="https://img.shields.io/discourse/users?server=https%3A%2F%2Fspeckle.community&amp;style=flat-square&amp;logo=discourse&amp;logoColor=white" alt="Community forum users"></a> <a href="https://speckle.systems"><img src="https://img.shields.io/badge/https://-speckle.systems-royalblue?style=flat-square" alt="website"></a> <a href="https://speckle.guide/dev/"><img src="https://img.shields.io/badge/docs-speckle.guide-orange?style=flat-square&amp;logo=read-the-docs&amp;logoColor=white" alt="docs"></a></p>

# About Speckle

What is Speckle? Check our ![YouTube Video Views](https://img.shields.io/youtube/views/B9humiSpHzM?label=Speckle%20in%201%20minute%20video&style=social)

### Features

- **Object-based:** say goodbye to files! Speckle is the first object based platform for the AEC industry
- **Version control:** Speckle is the Git & Hub for geometry and BIM data
- **Collaboration:** share your designs collaborate with others
- **3D Viewer:** see your CAD and BIM models online, share and embed them anywhere
- **Interoperability:** get your CAD and BIM models into other software without exporting or importing
- **Real time:** get real time updates and notifications and changes
- **GraphQL API:** get what you need anywhere you want it
- **Webhooks:** the base for a automation and next-gen pipelines
- **Built for developers:** we are building Speckle with developers in mind and got tools for every stack
- **Built for the AEC industry:** Speckle connectors are plugins for the most common software used in the industry such as Revit, Rhino, Grasshopper, AutoCAD, Civil 3D, Excel, Unreal Engine, Unity, QGIS, Blender and more!

### Try Speckle now!

Give Speckle a try in no time by:

- [![speckle XYZ](https://img.shields.io/badge/https://-speckle.xyz-0069ff?style=flat-square&logo=hackthebox&logoColor=white)](https://speckle.xyz) ⇒ creating an account!


### Resources

- [![Community forum users](https://img.shields.io/badge/community-forum-green?style=for-the-badge&logo=discourse&logoColor=white)](https://speckle.community) for help, feature requests or just to hang with other speckle enthusiasts, check out our community forum!
- [![website](https://img.shields.io/badge/tutorials-speckle.systems-royalblue?style=for-the-badge&logo=youtube)](https://speckle.systems) our tutorials portal is full of resources to get you started using Speckle
- [![docs](https://img.shields.io/badge/docs-speckle.guide-orange?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://speckle.guide/dev/) reference on almost any end-user and developer functionality

# AECTech Masterclass Repo

For the AECTech Masterclass, we're building a web application that **compares two 3D models and visualizes changes in geometry**. This repo is divided into a **web app** developed with Vue.js and a **server** built with python.

![diagram](https://user-images.githubusercontent.com/16748799/140319019-4ff437c6-21b6-4d13-a50f-c6b0f8eaa982.png)

## Frontend

The `frontend/` folder contains all code related to the app any user will be able to access.

The app was built using `Vue.js`, and communicates with Speckle through our `GraphQL API`. It also communicates with the app's `server` using `REST` calls.

## Backend

The `server/` folder contains all code related to the app's backend.

We're using a [FastAPI](https://link) API framework with a Uvicorn server implementation, written in Python, as well as our Python SDK to communicate with the [public Speckle server](https://speckle.xyz). The server contains two basic routes:

- **`diff-check/STREAM_ID/CURRENT_COMMIT_ID/PREV_COMMIT_ID`**
  
  Checks for an existing commit in a predefined `diff` branch and returns the _diff commit_ if it does exist.

- **`diff/STREAM_ID/CURRENT_COMMIT_ID/PREV_COMMIT_ID`**
  
  Performs a diff operation against two commits from the same stream. The result of the `diff` operation will be commited to the stream on a predefined diff branch, and returns the diff commit if the operation was successful.

# Workshop pre-requisites

Our workshop includes a **code walkthrough**, where we'll bring you line-by-line through a few key Speckle-specific front end and back end sections of our repo, as well as **live app testing**, where we'll use Speckle connectors in conjunction with our new web app to analyze some model geometry.

Prepare for both portions of our workshop by going through the following sections to brush up on essential knowledge and make sure your development and testing environments are set up!

## General requirements

- An IDE. We're using [VSCode](https://code.visualstudio.com/download) with the [Vetur extension](https://marketplace.visualstudio.com/items?itemName=octref.vetur)
- A Speckle account. Create one on our public server at [Speckle.xyz](https://speckle.xyz)
- A GitHub account: don't forget to clone this repo!

## Backend walkthrough requirements

Some basic familiarity with python, POST requests, and API routing is recommended.

- `python` (version `3.6`, recommended `3.9`) installed on your computer. [Download it here](https://www.python.org/downloads/)
- Install `FastAPI`:
  ```shell
  pip install fastapi
  # and then
  pip install "uvicorn[standard]"
  ```
- Install `specklepy`
  ```shell
  pip install specklepy
  ```
  *If you're experiencing pip install issues, check that you are running these commands as an administrator!*
  
 To deploy the server, open a command window in VSCode and navigate to your server folder. Run:
 
 ```shell
 uvicorn main:app --reload
 ```
  
## Frontend walkthrough requirements

Some basic familiarity with JS and the Vue framework is recommended.

- Install `node` [Download it here](https://nodejs.org/en/download/)
- Install `vue CLI` - [Instructions here](https://cli.vuejs.org/guide/installation.html)
- Install `vue dev tools` for Chrome [here](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)

 To deploy the server, open a command window in VSCode and navigate to your frontend folder. Run:
 
 ```shell
 npm install
 npm run serve
 ```

## App testing requirements

We're using [Rhino 7](https://www.rhino3d.com/download/), Grasshopper for Rhino, and Revit 2021 for our 3D model comparisons. You can 

- Install [Speckle Manager](https://speckle.guide/user/manager.html)
- Read our [Speckle Rhino guide](https://speckle.guide/user/rhino.html) for a quick intro to using Speckle for Rhino 😎
- Install the Rhino `Speckle Connector` from Speckle Manager. If you'd like to play around with Grasshopper and Revit, you can install those too!
