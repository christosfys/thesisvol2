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


🔹 Part I – Role-Based Views
Experiment Page (Example: 2D Unet Prostate WG Segmentation)

Title and experiment info (fetched from MLflow).

Left panel includes three divs:

Task type (e.g., classification, segmentation).

Role selector: AI Developer, Patient, Clinical.

QR code linking to GitLab with metadata collection code.

Available Buttons

Download JSON → Export metadata as .json.

Show More Info → Reveal additional metadata beyond user role.

Save → Store selected info in sessionStorage.

See Data → Navigate to aggregated view of saved metadata.

Role Selection

Dropdown with roles: AI Developer, Patient, Clinical.

Users can select info from their role or combine from multiple roles.

Data Saving

Multiple selections supported.

Success alert confirms storage.

Errors handled (e.g., no role selected, no checkbox selected).

Viewing Stored Data

After saving, See Data is enabled.

Aggregated info displayed, organized per role.

🔹 Part II – General Metadata View

Consolidates metadata into tables, accessible to all users.

Left panel includes task type, QR code, and three buttons:

Download → Download .zip file with code & artifacts.

Share Model → Share the experiment page.

Download JSON → Export all metadata as .json.

Central page displays tables by category.

A pipeline section illustrates experiment workflows.

📊 Example Outputs

JSON files are generated per task when Download JSON is used.

Different experiments provide varied cases and parameters.

📝 Conclusion

The two implemented applications enable the collection and visualization of metadata:

Part I: Role-based filtering ensures each user (AI Developer, Patient, Clinical) sees relevant information and can select useful metadata.

Part II: A general overview provides consolidated metadata for the broader public.

These tools improve accessibility and usability of AI model metadata within ProCAncer-I.

🙏 Acknowledgements

Special thanks to:

Χαρίδημος Κονδυλάκης

Βάλια Καλοκύρη

Χαράλαμπος Καλαντζόπουλος

for their valuable support during the project.
