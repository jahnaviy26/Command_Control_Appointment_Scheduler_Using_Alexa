import logging
import ask_sdk_core.utils as ask_utils
import boto3
import uuid
import re
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

scope = ["https://www.googleapis.com/auth/calendar"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
API_NAME = 'calendar'
API_VERSION = 'v3'

service = build(API_NAME, API_VERSION, credentials=creds)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    def handle(self, handler_input):
        speak_output = "Hello! Welcome to our hospital.Are you already a user with us? If yes, Say 'Returning patient' to schedule a doctor appointment. If you are a new user, Say 'new patient' to create a new user ID."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class NewPatientIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewPatientIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Thank you for choosing this Hospital. Please provide your information. What is your full name?"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response    
        
def convert_email(email):
    converted_email = email.replace(" dot ", ".").replace(" at ", "@").replace(" ", "").lower()
    return converted_email

class GatherUserInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GatherUserInfoIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots

        name = slots['FullName'].value
        age = slots['Age'].value
        gender= slots['Gender'].value
        email = slots['Email'].value
        
        
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['name'] = name
        session_attributes['age'] = age
        session_attributes['gender'] = gender
        session_attributes['email'] = email
        
        Email=convert_email(email)
        print(Email)
        
        ses_client = boto3.client('ses', region_name="eu-north-1")
        response = ses_client.list_identities(IdentityType='EmailAddress')
        verified_emails = response['Identities']

        if Email not in verified_emails:
            verify_email_identity(Email)

            session_attributes = handler_input.attributes_manager.session_attributes
            session_attributes['Email'] = Email  # Store the email in session attributes for future reference

            speak_output = f"Thank you for providing your information. A verification email has been sent to your email address. Please check your inbox and follow the instructions to verify your email. Once you have verified your email, say 'Verified'."
        else:
            
            user_id = str(random.randint(10000000, 99999999))
            print(user_id)
            
            store_user_info(user_id,age,Email, gender, name , petName)
            print(f"info stored")
            send_email(Email, name, user_id)

            speak_output = f"Thank you for providing your information. Your Patient ID is {user_id}. The details have been sent to the email.If you want to schedule an appointment say 'schedule an appointment'!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )      

def verify_email_identity(Email):
    ses_client = boto3.client('ses', region_name="eu-north-1")
    response = ses_client.verify_email_identity(EmailAddress=Email)
    
    return response
    
class VerifyEmailIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("VerifyEmailIntent")(handler_input)

    def handle(self, handler_input):
        
        session_attributes = handler_input.attributes_manager.session_attributes
        Email = session_attributes.get('Email')
        name=session_attributes.get('name')
        age=session_attributes.get('age')
        gender=session_attributes.get('gender')

        if Email:
            user_id = str(random.randint(10000000, 99999999))
            store_user_info(user_id,age,Email, gender, name)
            
            subject = "User ID is successfully created "
            body = f"Dear {name},your information has been stored. Your ID is {user_id}."
            send_email(Email,subject,body)

            speak_output = f"Thank you for verifying your email. Your ID is {user_id}.The details have been sent to your email.Say 'Schedule an appointment' if you want to schedule an appointment."
        else:
            # No email provided in session attributes
            speak_output = "Sorry, I couldn't find any pending email verification. Please provide your information again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

client = boto3.client('dynamodb')

def store_user_info(user_id,age,Email, gender, name):
    # Put item (store user information) in the table
    response = client.put_item(
        TableName='infoTable',
        Item={
            'user_id': {'S': user_id},
            'u_age': {'S': age},
            'u_email': {'S': Email},
            'u_gender': {'S': gender},
            'u_name': {'S': name}
        }
    )

def send_email(Email, subject, body):
    ses_client = boto3.client('ses',region_name="eu-north-1")
    sender_email = "jahnaviyerram2605@gmail.com" 
   
    response = ses_client.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [Email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response        

class ReturningPatientIntentHandler(AbstractRequestHandler):
    # uttarance: returning patient
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReturningPatientIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        user_id= slots["user_id"].value
        Email=get_email_byUserId(user_id)
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['Email'] = Email
        speak_output=f"Your Id is {user_id}"
        try:
            dynamodb = boto3.resource('dynamodb')
            table_name = "infoTable"
            table = dynamodb.Table(table_name)

            response = table.get_item(Key={'user_id': user_id})
            if 'Item' in response:
                speak_output = "Welcome back! How may I assist you today? Say 'Schedule an appointment' if you want to schedule a new appointment!"
                handler_input.attributes_manager.session_attributes['user_id'] =user_id
            else:
                speak_output = "The provided patient ID does not exist. Please check your patient ID or register as a new patient."
        except ValueError:
            speak_output = "The user ID should be a valid integer. Please try again."
       
        return (handler_input.response_builder.speak(speak_output).response)  

def get_email_byUserId(user_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(
        TableName='infoTable',
        FilterExpression='user_id = :name',
        ExpressionAttributeValues={
            ':name': {'S': user_id}
        }
    )
    if response['Count'] > 0:
        item = response['Items'][0]
        email = item['u_email']['S']
        return email
    
    return None

class forgotIdIntentHandler(AbstractRequestHandler):
    # uttarance: forgot,forgot id
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("forgotIdIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        Email = slots["emailId"].value
        print(Email)
        Email = Email.lower()
        Email = Email.replace(" at ", "@").replace(" dot ", ".").replace(" ","")
        user_ids = retrieve_userid(Email)

        if user_ids:
            speak_output = f"Welcome back! Your user id's are {', '.join(user_ids)}.Say 'Schedule an appointment' if you want to to schedule a new appointment."
        else:
            speak_output = f"The provided EmailAddress does not exist. Please provide us the valid EmailAddress or register as a new patient."

        return(handler_input.response_builder.speak(speak_output).response)

def retrieve_userid(Email):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(
        TableName='infoTable',
        FilterExpression='u_email = :Email',
        ExpressionAttributeValues={
            ':Email': {'S': Email}
        }
    )
    if response['Count'] > 0:
        user_ids = [item['user_id']['S'] for item in response['Items']]
        return user_ids
    return None
      
     
class ScheduleIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScheduleIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        date = str(slots["date"].value)
        time = str(slots["time"].value)
        field=str(slots["specialization"].value)
        print(field)
        doctors = get_doctors_by_specialization(field)
        
        handler_input.attributes_manager.session_attributes["date"] = date
        handler_input.attributes_manager.session_attributes["time"] = time
        handler_input.attributes_manager.session_attributes["field"] = field
        
        doctors_string = ", ".join(doctors)
        print(doctors_string) 
        speak_output=f"The available doctors in the {field} specialization are {doctors_string}. Please select a doctor for scheduling."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
class DoctorSchedulingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DoctorSchedulingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        DoctorName = slots["doctor_name"].value
        DoctorName=DoctorName.lower()
        print("doctor name is",DoctorName)
        
        calendar_id = get_calendar_id_by_doctor_name(DoctorName)
        print("Calendar ID:", calendar_id) 
        
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['calendar_id'] =calendar_id
        
        date   = session_attributes.get("date")
        time   = session_attributes.get("time")
        Email  = session_attributes.get('Email')
        user_id= session_attributes.get('user_id')
        field  = session_attributes.get('field')
        
        
        dateSlot = datetime.strptime(date, "%Y-%m-%d")
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        time_min = datetime(dateSlot.year, dateSlot.month, dateSlot.day, hour, mins)
        print(time_min)
        session_attributes['time_min'] =time_min
        time_max = time_min + timedelta(hours=1)
        
        handler_input.attributes_manager.session_attributes["time_min"] = str(time_min)
        if check_free_busy(time_min, time_max,calendar_id):
            print(f"checked free busy")
            reserve_appointment(time_min, time_max,calendar_id)
            print(f"appointment reserved")
            subject = "Your appointment is Scheduled"
            body = f"Dear user your appointment is successfully scheduled with {DoctorName} for {field} at {time} on {date}."
            print(body)
            send_email(Email, subject, body)
            
            speak_output = f"Your appointment on {date} at {time} with doctor {DoctorName} is successfully scheduled."
        else :
            speak_output = f"Sorry, the selected time is not available. Would you like to schedule in the next available slot?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
class ConfirmationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ConfirmationIntent")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        confirmation_slot = slots["confirmation"]
        
        calendar_id=session_attributes.get('calendar_id')
        time_min=session_attributes.get('time_min')
        
        if confirmation_slot and confirmation_slot.resolutions and confirmation_slot.resolutions.resolutions_per_authority:
            confirmation_value = confirmation_slot.resolutions.resolutions_per_authority[0].values[0].value.name
            
            if confirmation_value == "yes":
                next_slot = find_next_available_slot(time_min)
                
                if next_slot is not None:
                    reserve_appointment(next_slot['start'], next_slot['end'],calendar_id)
                    speak_output = f"Your appointment on {next_slot['date']} at {next_slot['time']} is successfully scheduled."
                else:
                    speak_output = "Sorry, there are no available slots at the moment. Please try again later."
            else:
                speak_output = "Alright, let me know when you want to schedule an appointment.say 'schedule an appointment' to resume your journey!"
        else:
            speak_output = "Sorry, I didn't understand your confirmation. Please try again."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("How can I assist you further?")
                .response
        )
        
    
from datetime import datetime
import pytz
import boto3

dynamodb = boto3.client('dynamodb')

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)
    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))
    def handle(self, handler_input):
        speak_output = "Goodbye!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response)

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response)


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NewPatientIntentHandler())
sb.add_request_handler(GatherUserInfoIntentHandler())
sb.add_request_handler(ReturningPatientIntentHandler())
sb.add_request_handler(forgotIdIntentHandler())
sb.add_request_handler(VerifyEmailIntentHandler())
sb.add_request_handler(ScheduleIntentHandler())
sb.add_request_handler(DoctorSchedulingIntentHandler())
sb.add_request_handler(ConfirmationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) 

sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()

import pytz
from datetime import datetime, timedelta
import json
import boto3
client = boto3.client('dynamodb')


def get_doctors_by_specialization(field):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DocInfo')
    response = table.scan(
        FilterExpression='#field = :se', 
        ExpressionAttributeNames={'#field': 'field'},  
        ExpressionAttributeValues={
            ':se': field
        }
    )
    doctors = [item['DocName'] for item in response['Items']]
    return doctors


def get_calendar_id_by_doctor_name(DoctorName):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(
        TableName='DocInfo',
        FilterExpression='DocName = :name',
        ExpressionAttributeValues={
            ':name': {'S': DoctorName}
        }
    )
    
    if response['Count'] > 0:
        item = response['Items'][0]
        calendar_id = item['calendar_id']['S']
        return calendar_id
    return None
    
def reserve_appointment(time_min, time_max,calendar_id):
    timezone = pytz.timezone('Asia/Kolkata')
    
    #user_id=handler_input.attributes_manager.session_attributes.get("user_id")
    
    time_min_ist = time_min.astimezone(timezone)
    time_max_ist = time_max.astimezone(timezone)
    
    event = {
        'summary': 'appointment',
        'description': f' Patient id: \n Patient Name:',
        'start': {
            'dateTime': time_min_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': time_max_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    response = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(response)
   
   
import pytz
from datetime import datetime

def check_free_busy(time_min, time_max,calendar_id):
    try:
        ist_timezone = pytz.timezone('Asia/Kolkata')
        time_min_ist = time_min.astimezone(ist_timezone)
        time_max_ist = time_max.astimezone(ist_timezone)
        print(f"chehcking free busy")
        
        free_busy_query = {
            'timeMin': time_min_ist.isoformat(),
            'timeMax': time_max_ist.isoformat(),
            'timeZone': 'Asia/Kolkata',
            'items': [{'id': calendar_id}]
        }
        response = service.freebusy().query(body=free_busy_query).execute()
        calendars = response.get('calendars', {})
        calendar = calendars.get(calendar_id, {})
        busy_slots = calendar.get('busy', [])
        return len(busy_slots) == 0
    except Exception as e:
        logging.error(f"Error querying free/busy: {str(e)}")
        return False


def schedule_appointment():
    next_slot = find_next_available_slot()
    if next_slot is not None:
        reserve_appointment(next_slot['start'], next_slot['end'])
        return True, f"Your appointment on {next_slot['date']} at {next_slot['time']} is successfully scheduled."
    else:
        return False, "Sorry, there are no available slots at the moment. Please try again later."



def find_next_available_slot(handler_input,time_min):
    time_min = datetime.strptime(time_min, "%Y-%m-%d %H:%M:%S")
    current_time =time_min
    calendar_id=handler_input.attributes_manager.session_attributes.get("calendar_id")
    
    time_min = current_time
    print(time_min)
    time_max = time_min+ timedelta(days=1)

    interval = timedelta(minutes=60)

    while time_min <= time_max:
        if check_free_busy(time_min, time_min + interval,calendar_id):
            return {
                'start': time_min,
                'end': time_min + interval,
                'date': time_min.date().strftime("%Y-%m-%d"),
                'time': time_min.time().strftime("%H:%M")
            }

        time_min += interval
        
    return None

  
