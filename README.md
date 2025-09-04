# Prepanet Academic Automation  

This project was developed during my internship at Prepanet (ITESM) to optimize academic processes by integrating the Google Sheets API and the Canvas API.  

## Overview  
Prepanet administrators previously performed a manual daily process that took ~3 hours to complete. The task involved trespassing the grades of each student from Canvas into a Google Sheets file.  

This was necessary because certain organizational roles did not have direct access to Canvas, but still needed visibility of student academic performance. By making this information available through Google Sheets, administrators, coordinators, and staff could collaborate more effectively without requiring full Canvas access.  

This project automated the workflow, reducing the process to ~20 minutes, improving accessibility, and ensuring data accuracy.  

## Features  
- Canvas API integration to fetch student grades and enrollment data.  
- Google Sheets API integration to update spreadsheets automatically.  
- Data transformation pipeline to match Canvas data with Prepanet’s reporting format.  
- Error handling and for failed API requests or missing records.  