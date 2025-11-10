# YemekYAP
Image processing suggestion AI tool to find an appropriate meal for your fridge.
@authors
Ege Rasim, Ali Şahin, Efe Görkem Akkanat, Kaan Arslan.

# 🍲 AI Recipe Generator from Image (YOLO & OpenAI Integration)

This application is an intelligent tool that automates the process of generating custom meal recipes. It achieves this by combining **state-of-the-art computer vision (YOLO)** and **advanced large language models (OpenAI API)** to analyze user-uploaded ingredient images.

The core value proposition is transforming a simple photo of ingredients into a step-by-step cooking guide.

## 🚀 Key Features and Workflow Breakdown

The application follows a precise, multi-stage AI pipeline to ensure accurate ingredient detection and creative recipe generation:

1.  **Input Acquisition:** The user uploads an image (strictly **PNG format**) containing various food items, such as fruits, vegetables, meat, and other kitchen staples.
2.  **Ingredient Detection (YOLO):** The uploaded image is processed by an integrated **YOLO (You Only Look Once)** model. This powerful object detection framework accurately identifies and localizes all relevant food ingredients present in the picture.
3.  **Prompt Engineering:** The list of detected ingredients is systematically extracted and formatted into a highly specific and optimized **prompt** tailored for the OpenAI API's recipe generation capabilities.
4.  **Recipe Generation via OpenAI API:** The customized prompt is sent to the **OpenAI API (GPT Models)**, requesting a unique, feasible recipe utilizing all or most of the detected items.
5.  **Output Display:** The structured recipe received from the API is presented to the user through a clean, readable graphical user interface (GUI).

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Object Detection** | YOLO (You Only Look Once) | Identifies and localizes ingredients in the image. |
| **Recipe Generation** | OpenAI API (GPT Models) | Generates the cooking instructions and recipe structure. |
| **Frontend/GUI** | Python (Specific framework, e.g., Tkinter/PyQt, if applicable) | Provides the graphical interface for user interaction and output display. |
| **Input Format** | PNG Image | Required input format for ingredient images. |

## ⚙️ Setup and Launch Instructions

To get the application running on your local machine, follow these simple steps:

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR-REPO-URL]
    cd [YOUR-REPO-NAME]
    ```
2.  **Install Dependencies:**
    *Ensure you have Python installed and install the necessary libraries (e.g., `opencv`, `yolo_package`, `openai`, GUI library):*
    ```bash
    pip install -r requirements.txt 
    # (Assuming you have a requirements.txt file)
    ```
3.  **Set Environment Variables:**
    *You must set your OpenAI API key as an environment variable (`OPENAI_API_KEY`).*
4.  **Launch the Application:**
    Navigate to the frontend directory and run the main GUI file:
    ```bash
    cd frontend/
    python GUI.py
    ```

The application window will open, allowing you to start uploading ingredient images.
