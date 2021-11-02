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

- [![speckle XYZ](https://img.shields.io/badge/https://-speckle.xyz-0069ff?style=flat-square&logo=hackthebox&logoColor=white)](https://speckle.xyz) ⇒ creating an account at
- [![create a droplet](https://img.shields.io/badge/Create%20a%20Droplet-0069ff?style=flat-square&logo=digitalocean&logoColor=white)](https://marketplace.digitalocean.com/apps/speckle-server?refcode=947a2b5d7dc1) ⇒ deploying an instance in 1 click

### Resources

- [![Community forum users](https://img.shields.io/badge/community-forum-green?style=for-the-badge&logo=discourse&logoColor=white)](https://speckle.community) for help, feature requests or just to hang with other speckle enthusiasts, check out our community forum!
- [![website](https://img.shields.io/badge/tutorials-speckle.systems-royalblue?style=for-the-badge&logo=youtube)](https://speckle.systems) our tutorials portal is full of resources to get you started using Speckle
- [![docs](https://img.shields.io/badge/docs-speckle.guide-orange?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://speckle.guide/dev/) reference on almost any end-user and developer functionality

![Untitled](https://user-images.githubusercontent.com/2679513/132021739-15140299-624d-4410-98dc-b6ae6d9027ab.png)

# Repo structure

This repo is divided into two distinct parts, a **frontend** and a **server**

## Frontend

The `frontend/` folder contains all code related to the app any user will be able to access.

The app was built using `Vue.js`, and communicates with Speckle through our `GraphQL API`. It also communicates with the app's `server` using `REST` calls.

## Backend

The `server/` folder contains all code related to the app's backend.

It's a [FastAPI](https://link) server, written in Python and uses our Python SDK to communicate with our [public server](https://speckle.xyz)

> `FastAPI` generates automatic documentation on the `/docs` route of the server.

It is a very basic server composed of two routes:

## `diff-check/STREAM_ID/CURRENT_COMMIT_ID/PREV_COMMIT_ID`

Checks for an existing commit in a predefined `diff` branch and returns the _diff commit_ if it does exist.

## `diff/STREAM_ID/CURRENT_COMMIT_ID/PREV_COMMIT_ID`

Performs a diff operation against two commits from the same stream.

Result of the `diff` operation will be commited to the stream on a predefined branch.

Returns the diff commit if the operation was successfull.

# Workshop pre-requisites

For the **server**, you must have:

- `python` installed in your computer (at least version `3.6`, `3.9` recommended) [Download it here](https://www.python.org/downloads/)
- Install `FastAPI`:
  ```shell
  pip install fastapi
  # and then
  pip install "uvicorn[standard]"
  ```
-

For the **Vue app**:

- Install `node` [Download it here](https://nodejs.org/en/download/)
- Install `vue CLI` - [Instructions here](https://cli.vuejs.org/guide/installation.html)
- Install `vetur` VSCode extension
- Install `vue dev tools` for Chrome