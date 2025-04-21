


# 🔍 GitHub PageRank Comparison Tool

A Flask web application that compares the influence of two GitHub users using a **custom PageRank algorithm**. It visualizes the follower and repository network of each user, calculates their PageRank scores, and determines who has a more impactful GitHub presence.

## 🚀 Features

- 🔎 Fetches real-time data from GitHub's REST API.
- 📈 Constructs a directed graph for each user with followers and repositories.
- 🧠 Calculates influence using a manually implemented **PageRank algorithm**.
- 📊 Visualizes the network using `NetworkX` and `Matplotlib`.
- 🏆 Compares two GitHub users and declares the winner based on influence.


## 📸 Sample Output
![Screenshot 2025-04-21 172645](https://github.com/user-attachments/assets/7cb18b54-f79d-4eb6-9d2b-9155a31bcfca)


## 🛠️ Installation

### 1. Install libraries

```bash
pip install flask matplotlib networkx requests
```

### 2. Run the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.


## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Visualization:** NetworkX, Matplotlib
- **Frontend:** HTML, CSS (customizable)
- **API:** GitHub REST API



## 📂 Project Structure
```
📦 github-pagerank-compare/
│
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # Frontend UI
├── static/
│   └── *.png              # Generated network graph images
└── README.md              # Project documentation
```




## 👨‍💻 Author
**Arushi Nirala**  
