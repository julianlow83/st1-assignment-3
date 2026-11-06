"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

from datetime import datetime
from typing import Optional
from .domain import AppointmentStatus
from .data_store import SmartCareDataStore
from .services import PatientService, PractitionerService, AppointmentService
from .domain import parse_date_time, format_appointment


def run_menu(store: SmartCareDataStore) -> None:
    """
    Interactive terminal menu for SmartCare.
    Reuses a single store and service instances throughout the session.
    Handles user prompts, enum parsing, and graceful error recovery.
    """
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)

    while True:
        print("\n=== SmartCare Appointment System ===")
        print("1. Register Patient")
        print("2. Find Patient")
        print("3. Register Practitioner")
        print("4. Find Practitioner")
        print("5. Book Appointment")
        print("6. Cancel Appointment")
        print("7. Find Appointment")
        print("8. List Practitioner Appointments")
        print("0. Exit")

        choice = input("Enter choice (0-8): ").strip()

        if choice == "0":
            print("Exiting session. All session data is discarded.")
            break

        elif choice == "1":
            pid = input("Enter Patient ID: ").strip()
            name = input("Enter Patient Name: ").strip()
            try:
                patient_svc.register_patient(pid, name)
                print(f"Successfully registered patient: {pid}")
            except (ValueError, LookupError) as e:
                print(f"[Error] Failed to register patient: {e}")

        elif choice == "2":
            pid = input("Enter Patient ID to find: ").strip()
            try:
                patient = patient_svc.find_patient(pid)
                print(f"Found Patient -> ID: {patient.patient_id}, Name: {patient.name}")
            except LookupError as e:
                print(f"[Error] {e}")

        elif choice == "3":
            pid = input("Enter Practitioner ID: ").strip()
            name = input("Enter Practitioner Name: ").strip()
            spec = input("Enter Practitioner Specialty: ").strip()
            try:
                practitioner_svc.register_practitioner(pid, name, spec)
                print(f"Successfully registered practitioner: {pid}")
            except (ValueError, LookupError) as e:
                print(f"[Error] Failed to register practitioner: {e}")

        elif choice == "4":
            pid = input("Enter Practitioner ID to find: ").strip()
            try:
                doc = practitioner_svc.find_practitioner(pid)
                print(f"Found Practitioner -> ID: {doc.practitioner_id}, Name: {doc.name}, Specialty: {doc.specialty}")
            except LookupError as e:
                print(f"[Error] {e}")

        elif choice == "5":
            aid = input("Enter Appointment ID: ").strip()
            pid = input("Enter Patient ID: ").strip()
            doc_id = input("Enter Practitioner ID: ").strip()
            date_str = input("Enter Date & Time (YYYY-MM-DD HH:MM): ").strip()
            try:
                dt = parse_date_time(date_str)
                appointment_svc.book_appointment(aid, pid, doc_id, dt)
                print(f"Successfully booked appointment: {aid}")
            except (ValueError, LookupError) as e:
                print(f"[Error] Booking failed: {e}")

        elif choice == "6":
            aid = input("Enter Appointment ID to cancel: ").strip()
            try:
                appointment_svc.cancel_appointment(aid)
                print(f"Successfully cancelled appointment: {aid}")
            except (ValueError, LookupError) as e:
                print(f"[Error] Cancellation failed: {e}")

        elif choice == "7":
            aid = input("Enter Appointment ID to find: ").strip()
            try:
                appt = appointment_svc.find_appointment(aid)
                print(f"Found Appointment -> {format_appointment(appt)}")
            except LookupError as e:
                print(f"[Error] {e}")

        elif choice == "8":
            doc_id = input("Enter Practitioner ID to list appointments: ").strip()
            status_input = input(
                "Enter Status filter (SCHEDULED / CANCELLED / COMPLETED or leave blank for all): ").strip()
            try:
                status_enum = None
                if status_input:
                    status_enum = AppointmentStatus[status_input.upper()]

                appts = appointment_svc.list_practitioner_appointments(doc_id, status_enum)
                if not appts:
                    print("No appointments found matching criteria.")
                else:
                    print(f"\n--- Appointments for Practitioner {doc_id} ---")
                    for appt in appts:
                        print(format_appointment(appt))
            except (ValueError, KeyError, LookupError) as e:
                print(f"[Error] Listing failed: {e}")
        else:
            print("[Error] Unknown menu choice. Please select between 0 and 8.")