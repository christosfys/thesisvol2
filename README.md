# Visual Design Based on the Roles of Metadata Concerning Machine-Learning Models  

Diploma Thesis – **University of Crete, Department of Computer Science**  
Author: **Χρήστος Φυσάρακης (ΑΜ: 4068)**  
Supervisor: **Χαρίδημος Κονδυλάκης**  

---

## 📖 Introduction  

The **ProCAncer-I** project aims to build the first European medical imaging platform focusing on prostate cancer (PCa), fully compliant with GDPR and ethical standards. The platform integrates large-scale data and AI algorithms under strict quality control measures.  

The main objective of ProCAncer-I is to collect and organize a significant volume of multimodal data, including **mpMRI imaging** and **clinical data**, along with their metadata, to enable efficient and clinically oriented training of advanced AI models for prostate cancer management.  

One of its applications, the **AI Passport**, is responsible for presenting all the necessary details to make an AI model fully usable. Metadata is collected and managed via **MLflow**.  

As part of this thesis, two different **web applications** were implemented to visualize and manage metadata.  

---

## ⚙️ Implementation  

The **AI Model Passport UI** is a **Django-based application**.  
It provides a web interface to publish, explain, and share metadata with the public.  

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Django  
- **Dependencies:** `django`, `mlflow`, `qrcode`, `boto3`  
- **Execution:**  
  ```bash
  python manage.py runserver




🙏 Acknowledgements

Special thanks to:

Χαρίδημος Κονδυλάκης

Βάλια Καλοκύρη

Χαράλαμπος Καλαντζόπουλος

for their valuable support during the project.
