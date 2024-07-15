# Diabetes Management Platform

![HealthPath Presentation (1)](https://github.com/user-attachments/assets/3d4b3e6b-c6a3-442a-9b91-9936990d5332)

## Overview
Our platform integrates with Continuous Glucose Monitors (CGM) to help diabetics manage their health through real-time glucose tracking, personalized insulin dosage, and AI chatbot support.

## Features
- **Real-time Glucose Tracking**: Integrates with CGMs to provide continuous monitoring.
- **Personalized Insulin Dosage**: Recommends insulin doses based on real-time data.
- **AI Chatbot Support**: Offers 24/7 assistance and guidance.
- **Calorie Measurement**: Helps users manage their meal plans effectively.

## Technologies Used
- **Streamlit**: For building the web interface.
- **Langflow**: For architecture and component integration.
- **AI/ML APIs**:
  - GPT-4: For text generation and understanding image content.
  - ADA-002: For embedding and image input.

## Langflow Architecture
Langflow provides predefined components, but we created custom components due to the absence of specific AI/ML APIs in the models section. Using the custom component element from Langflow's helpers section, we developed:
- **Image Input**: For processing image data.
- **AI/ML API Embeddings (ADA-002)**: For embedding functionality.
- **AI/ML API Chatbot (GPT-4)**: For chatbot capabilities.

## Business Model
Our business model involves strategic partnerships across various sectors:
- **Healthcare**: Collaborations with hospitals and clinics.
- **Medical Devices Providers**: Partnerships with companies like Dexcom and Abbott.
- **Food & Beverage**: Associations with Glovo and Monoprix for dietary management.
- **R&D**: Working with organizations like WHO and the International Diabetes Federation.
- **Fitness Centers**: Partnerships with gyms like Anytime Fitness.

## How it Works
1. **Glucose Monitoring**: Continuous monitoring through CGM.
2. **Live Data Integration**: Real-time data streaming to HealthPath.
3. **Services**: Personalized insights, dosage recommendations, and chatbot support.

## Installation
To install and run the project locally, follow these steps:
1. Clone the repository:
    ```sh
    git clone https://github.com/yahyasamet/healthpath/
    ```
2. Navigate to the project directory:
    ```sh
    cd diabetes-management-platform
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the application:
    ```sh
    streamlit run app.py
    ```
