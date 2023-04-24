# ThreatAI: A Cutting-Edge Cybersecurity Solution

## Introduction
ThreatAI is a state-of-the-art cybersecurity solution that leverages the power of artificial intelligence and machine learning to accurately classify incoming network traffic based on the tactics employed by potential attackers. Our system has been expertly trained using data gathered from a Cowrie honeypot deployed in the cloud, ensuring a comprehensive understanding of the latest cyber threat landscape.
Our user-friendly dashboard provides essential information on network traffic, enabling security professionals to gain valuable insights and make informed decisions. By integrating with the AbuseIPDB API, ThreatAI enriches the collected data with additional information such as IP reputation, country, and ISP, offering a more holistic view of potential threats.
Stay one step ahead of cybercriminals with ThreatAI, the intelligent solution for detecting and understanding network threats in real-time. Protect your organization's critical assets and ensure its digital security with our advanced AI-driven technology.

## System Requirements
ThreatAI is a lightweight and flexible application, designed to work on a variety of systems. The product was tested on a local PC with an AMD Ryzen 5 5625U, 8GB RAM, Windows 11, and a 512GB SSD. However, due to its lightweight nature, ThreatAI can also be tested on machines with lower specifications.

## Installation
1. Clone repository.
2. Install node modules: `npm install`
3. Replace the API key for Abuse IPDB in the appropriate configuration file.
4. Run server: `node index.js`
5. Open Website: `localhost:3000`

## How to Use

1. Visit the ThreatAI website and navigate to the main dashboard. You will see a three-step process outlined: Conversion, Preprocessing, and Running ML Model.
2. Click on the "Run" button for Step-1: Conversion. This step will execute a Python script to convert the .gz file to a .csv file, streamlining the preprocessing of the dataset.
3. Once the conversion is complete, click on the "Run" button for Step-2: Preprocessing. This step will run multiple scripts in sequence to prepare the data for the application of the ML model.
4. After preprocessing is complete, click on the "Run" button for Step-3: Running ML Model. The LSTM model will be applied to the data for threat classification.
5. Upon successful completion of the ML model, a table dashboard will appear, displaying the latest threats along with key information such as Source IP, Commands, Tactic, and an Action button.
6. To gain more insight into a specific threat, click the "More Info" button in the Action column. This will use the AbuseIPDB API to generate additional information about the selected threat, such as IP reputation, country, ISP, and recommended mitigation techniques.

*Please note: Wait for the error or success message to show up after each script before running the next one. The last script, "Running ML model," may take some time to complete.*

## Troubleshooting & Customization
- The conversion script assumes you have a `cowrie.json.x.gz` file, where x is a number. You can remove or add functions to suit your file format.
- Data manipulation is done using the following attributes from the Cowrie honeypot: `['session', 'eventid', 'src_ip', 'destfile', 'username', 'password', 'timestamp', 'input']`. Ensure your file contains these attributes.

## Updates and Maintenance
Stay updated with the latest updates and bug fixes by following the ThreatAI repository: [https://github.com/tahaarshad/ThreatAI](https://github.com/tahaarshad/ThreatAI)

## Contact and Support
For any questions, assistance, or feedback, please visit the creator's LinkedIn profile: [https://www.linkedin.com/in/taha-arshad10/](https://www.linkedin.com/in/taha-arshad10/)

By following these steps and guidelines, you can effectively utilize ThreatAI to analyze network traffic, classify potential threats, and access valuable information to protect your organization's digital assets.
