# Command_Control_Appointment_Scheduler_Using_Alexa
Doctor_Appointment_Schedule_Using_Alexa is an intelligent appointment scheduling system designed to streamline and simplify the process of booking doctor appointments. This bot utilizes AWS services and integrates with Google Calendar API to provide a seamless user experience for scheduling medical consultations.
# Problem statement
command-controlled appointment scheduler using Alexa would be to create a hands-free and convenient way for users to schedule appointments and manage their schedule. Many people have busy schedules and struggle to keep track of their appointments, which can lead to missed appointments and wasted time. By integrating Alexa into the scheduling process, users can easily manage their schedule and free up time for more important tasks. The solution should be user-friendly, efficient, and accurately interpret user commands to ensure that appointments are scheduled correctly.
# Solution Overview
The Doctor Appointment Scheduler skill is developed using the Alexa Skills Kit (ASK) and utilizes AWS Lambda for serverless processing. It makes use of AWS DynamoDB for storing patient and doctor details, integrates with the Google Calendar API to check doctor availability, and employs Amazon Simple Email Service (SES) for sending email notifications
The following outlines the primary components of the solution:
**1.New User Registration:** New patients can create an account by providing essential information such as their name, age, gender, and email address. The skill ensures email verification to confirm the user's identity securely.
**2.Existing User Login:** Existing patients can log in using their patient ID. In case they forget their patient ID, they have the option to verify their identity by entering forgot ID.
**3.Doctor Availability Check:** The skill integrates with the Google Calendar API to access doctors' schedules and availability. Patients can inquire about available doctors based on their specialization, date, and time preferences.
**4.Appointment Booking:** Patients can effortlessly schedule appointments with their chosen doctors, taking into account the availability retrieved from the Google Calendar API. Once an appointment is booked, the skill reserves the slot in the doctor's calendar to avoid overlapping appointments.
**5.Appointment Confirmation:** After successfully booking an appointment, the skill sends a confirmation email to the patient, containing details such as the appointment date, time and doctor's name.
**6.Voice-Based Doctor Recommendations:** For added convenience, the skill can offer voice-based doctor recommendations. Patients can inquire about suitable doctors based on their specific symptoms or medical conditions. The skill responds with a list of doctors specialized in relevant fields.
**7.Voice Authentication (Optional):** To enhance security, the skill can implement voice authentication technology. This ensures that only authorized users can access sensitive account information and book appointments.
**8.Email Notifications:** Amazon Simple Email Service (SES) is utilized to send verification and confirmation emails securely. These emails play a crucial role in verifying user identities and keeping patients informed about their scheduled appointments.

# Tech Stack
The Hospital Appointment Scheduler skill is powered by a sophisticated tech stack that includes:
**1.Alexa Skills Kit (ASK):** A cutting-edge set of APIs and tools that enable seamless voice-driven interactions.
**2.AWS Lambda:** A robust serverless compute service that efficiently handles code execution in response to Alexa requests.
**3.AWS DynamoDB:** A high-performing NoSQL database service utilized for secure and scalable storage of patient and doctor data.
**4.Google Calendar API:** An advanced interface that facilitates smooth management of doctor schedules and availability.
**5.Amazon Simple Email Service (SES):** A reliable solution for sending well-timed and informative emails to users, ensuring effective communication.

# Work Flow
![workflow](https://github.com/jahnaviy26/Command_Control_Appointment_Scheduler_Using_Alexa/assets/97887220/ba3054ff-4982-4b4b-a394-87b15c7552bb)

# Skill Features
**User Registration and Verification**
-New patients can register by providing their full name, age, gender, DOB, father's name, and email.
-The skill sends a verification email to the provided email address for identity confirmation.
-After confirmation, The details of patient are stored in the DynamoDB in the form of table.
-Returning patients can log in using their patient ID or if they forgot their patiend ID they can verify their identity using their father's name.
**Doctor Availability Checking**
-Patients can search for available doctors based on a specified specialization, date, and time.
-The details of the doctors are retrieved from the DynamoDB table of doctors_details.
-The skill uses the Google Calendar API to check the availability of doctors for the specified time slot.
**Appointment Booking**
-Patients can schedule appointments with their chosen doctor based on availability.
-The skill reserves the appointment slot in the doctor's Google Calendar.
**Voice-Based Doctor Recommendations**
-Alexa can provide doctor recommendations based on the patient's symptoms or medical conditions.
-Users can ask Alexa for suggCode Link:estions, and the skill will offer a list of doctors specializing in relevant fields.
**Email Notifications**
-The skill sends verification emails to new patients for identity confirmation.
-Confirmation emails for scheduled appointments are sent to patients' registered email addresses.
# Lambda Function Code
The Lambda function for the Hospital Appointment Scheduler skill is responsible for handling user requests and interacting with the backend services. It is written in Python and integrated with the ASK SDK for Alexa interactions. The code is structured into several intent handlers to handle different user intents, such as registration, login, appointment booking, doctor recommendations, and more.
**Code Link:**

# Skill Invocation and User Flow
**1.Skill Launch:** Users can invoke the skill by saying "Alexa, open Hospital Appointment Scheduler."
**2.New Patient:** New patients can provide their information during the registration process and store them in DynamoDB. The skill will send a verification email to the provided email address.
**3.Verification:** New patients need to verify their email by following the instructions in the verification email.
**4.Returning Patient:** Returning patients can log in using their patient ID. If they forget their ID, they can verify their identity by providing their father's name.
**5.Doctor Availability Checking:** Patients can check the availability of doctors based on specialization, date, and time.
**6.Appointment Booking:** Patients can book appointments with available doctors.
**7.Voice-Based Doctor Recommendations:** Patients can ask Alexa for doctor recommendations based on their symptoms or medical conditions.
**8.Email Notifications:** Verification emails are sent to new patients, and confirmation emails are sent for scheduled appointments.

# Working with New Patients
New patients can efficiently register and schedule appointments through the Hospital Appointment Scheduler skill. Below is a step-by-step guide on how new patients can utilize the skill:
**Skill Invocation:** New patients can initiate the skill by saying "Alexa, open Hospital Appointment Scheduler."
**Registration:** Alexa will guide the new patient through the registration process. The patient needs to provide the following information:
    -Full Name
    -Age
    -Gender
    -Date of Birth (DOB)
    -Father's Name
    -Email Address
**Email Verification:** After registration, the skill will send a verification email to the provided email address. The patient must check their email and follow the instructions to complete the verification process.
**Account Creation:** Once the email is verified, the skill will create a unique patient ID for the new patient. The patient can use this ID for future logins.
**Storing the Information:** The details of the patient are successfully stored in the DynamoDB in the form of table.
**Doctor Availability Checking:** New patients can inquire about doctor availability based on their preferred specialization, date, and time.
**Appointment Booking:** After selecting a suitable doctor and appointment slot, the patient can proceed to book the appointment. Alexa will confirm the booking and send a confirmation email to the patient.

# Working with Returning Patients
Returning patients can conveniently access their accounts and manage appointments through the Hospital Appointment Scheduler skill. Here's a step-by-step guide on how returning patients can use the skill:
   **Skill Invocation:** Returning patients can launch the skill by saying "Alexa, open Hospital Appointment Scheduler."
   **Returning Patient Login:** Alexa will prompt the returning patient to provide their unique patient ID for authentication. The patient can say, "My patient 
     ID is [patient ID]," to log in directly.
   **Appointment Management:** Once logged in, returning patients can manage their appointments with ease. They can schedule appointments, check available 
     doctors by giving date, time and your required specialization.
   **Doctor Recommendations:** Returning patients can also ask for doctor recommendations based on their medical condition or symptoms. Alexa will provide a list 
     of doctors specializing in relevant fields to help them make informed decisions.
   **Appointment Booking:** After selecting a suitable doctor and appointment slot, the patient can proceed to book the appointment. Alexa will confirm the booking 
     and send a confirmation email to the patient.

# DynamoDB
In our project we use two DynamoDB tables:

   **1.Patient Registration Table:**
     -Purpose: This table is used to store the registration details of new patients who use the Alexa skill for the first time.Attributes: 
      patient_id,full_name,age, gender,date_of_birth,Father_name, email(The email address of the patient used for verification and 
      communication).
     -Usage: When a new patient uses the skill, their registration information is collected and stored in this table. It is also used to retrieve the patient's 
      details when they return to the skill.
     -Patient_Registration csv file: 
   **2.Doctor calendar Table:**
     -Purpose: This table is used to store the availability details of doctors for scheduling appointments.
     -Attributes: - doctor_name: The name of the doctor. - specialization: The medical specialization of the doctor. - calendar_id: The unique identifier for the 
      doctor's Google Calendar. -Usage: The skill checks this table to find available doctors based on user-requested medical specialization and schedules 
      appointments by updating the doctors' calendars with the appointment details.
     -Doctor calendar table csv file: 

# Emails you get while working with the skill
  Using the unverified email in [AWS SES](https://aws.amazon.com/ses/)to verify the email as the first step.
  **Verification Email**
  ![verifying email](https://github.com/jahnaviy26/Command_Control_Appointment_Scheduler_Using_Alexa/assets/97887220/f5e4c5e0-c2df-4acd-a9a5-58323ec06edc)
  **UserDetails Email**
  ![UserDetails](https://github.com/jahnaviy26/Command_Control_Appointment_Scheduler_Using_Alexa/assets/97887220/116e8fe6-6e21-439e-b284-f0460dfdf052)
  **Appointment Scheduled Email**
  ![Appointment Scheduled](https://github.com/jahnaviy26/Command_Control_Appointment_Scheduler_Using_Alexa/assets/97887220/3f6db7db-cd25-4cf5-8609-c65bea310391)

# Applications
  **Voice-Based Doctor Recommendations:** It Implements a feature that allows Alexa to recommend doctors based on the patient's medical conditions. 
    Users can ask Alexa for suggestions, and the skill can provide a list of doctors specializing in relevant fields.
  **Appointment Reminders:** Enabled the skill to send appointment reminders to patients a day or a few hours before their scheduled appointment. This can help 
    reduce no-shows and improve overall patient attendance.
  **Multilingual Support:** Can Extend the skill's capabilities to support multiple languages. Patients from diverse linguistic backgrounds can then interact 
    with the skill in their preferred language.

**In conclusion,command-controlled appointment scheduler using Alexa represents a significant leap forward in appointment management technology. By seamlessly integrating voice technology into the scheduling process,this has revolutionized the way users manage their busy lives.This user-friendly system simplifies the scheduling experience, enabling users to effortlessly and accurately schedule appointments through natural voice commands.
                      Through the power of Alexa's voice services,this solution offers a hands-free and convenient alternative to traditional manual methods. Users can now bid farewell to the tedious and error-prone processes of manual appointment management. With our command-controlled scheduler, they can reclaim valuable time, enhance productivity, and prioritize what truly matters.**

# Author
The Command Control Appointment Scheduler Using Alexa was developed by :
    -@jahnaviy26
    -Repository :

  
