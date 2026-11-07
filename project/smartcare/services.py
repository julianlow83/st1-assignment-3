from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from .data_store import SmartCareDataStore
from .domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from .queries import select_appointments


class PatientService:
    """Coordinate patient registration and lookup through the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate patient operations."""
        self.data_store = data_store

    def register_patient(self, patient_id: str, name: str) -> Patient:
        """Validate and register a patient, returning the stored object.

        Raise ValueError for invalid fields or an existing patient ID.
        """
        patient = Patient(patient_id, name)
        self.data_store.add_patient(patient)
        return patient

    def find_patient(self, patient_id: str) -> Patient:
        """Return the stored patient for a valid patient ID.

        Completion raises LookupError for absence and ValueError for
        a blank/invalid ID. It does not create a replacement patient.
        """
        if not isinstance(patient_id, str) or not patient_id.strip():
            raise ValueError("Patient ID must be a non-blank string.")

        trimmed_id = patient_id.strip()
        patient = self.data_store.find_patient(trimmed_id)
        if patient is None:
            raise LookupError(f"Patient with ID '{trimmed_id}' not found.")

        return patient


class PractitionerService:
    """Coordinate practitioner registration and lookup through the shared
    store.
    """

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate practitioner operations."""
        self.data_store = data_store

    def register_practitioner(
        self,
        practitioner_id: str,
        name: str,
        specialty: str,
    ) -> Practitioner:
        """Validate and register a practitioner, returning the stored
        object.

        Raise ValueError for invalid fields or an existing practitioner
        ID.
        """
        practitioner = Practitioner(practitioner_id, name, specialty)
        self.data_store.add_practitioner(practitioner)
        return practitioner

    def find_practitioner(self, practitioner_id: str) -> Practitioner:
        """Return the stored practitioner for a valid ID.

        Completion raises LookupError for absence and ValueError for
        a blank/invalid ID. It does not create a replacement
        practitioner.
        """
        if not isinstance(practitioner_id, str) or not practitioner_id.strip():
            raise ValueError("Practitioner ID must be a non-blank string.")

        trimmed_id = practitioner_id.strip()
        practitioner = self.data_store.find_practitioner(trimmed_id)
        if practitioner is None:
            raise LookupError(f"Practitioner with ID '{trimmed_id}' not found.")

        return practitioner


class AppointmentService:
    """Coordinate booking, lookup and cancellation using the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate appointment operations."""
        self.data_store = data_store

    def book_appointment(
        self,
        appointment_id: str,
        patient_id: str,
        practitioner_id: str,
        date_time: datetime,
    ) -> Appointment:
        """Book registered participant IDs and return the stored
        appointment.

        Raise LookupError for absent participants. Raise ValueError for
        invalid values, duplicate appointment IDs or a practitioner
        conflict.
        """
        patient = self.data_store.find_patient(patient_id)
        practitioner = self.data_store.find_practitioner(practitioner_id)
        if patient is None:
            raise LookupError('Patient not found')
        if practitioner is None:
            raise LookupError('Practitioner not found')
        appointment = Appointment(
            appointment_id,
            patient,
            practitioner,
            date_time,
        )
        if self.data_store.find_appointment(
            appointment.appointment_id,
        ) is not None:
            raise ValueError('Appointment ID already exists')
        if self.data_store.has_practitioner_conflict(
            practitioner.practitioner_id,
            date_time,
        ):
            raise ValueError(
                'Practitioner already has a SCHEDULED appointment at this time',
            )
        self.data_store.add_appointment(appointment)
        return appointment

    def find_appointment(self, appointment_id: str) -> Appointment:
        """Return the stored appointment; raise LookupError when absent.

        Reject a blank or invalid ID with ValueError; do not create
        records.
        """
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID must be a non-blank string.")

        trimmed_id = appointment_id.strip()
        appointment = self.data_store.find_appointment(trimmed_id)
        if appointment is None:
            raise LookupError(f"Appointment with ID '{trimmed_id}' not found.")

        return appointment

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        """Cancel an appointment through the domain method and retain the
        appointment.

        Return the cancelled object. Unknown IDs raise LookupError;
        invalid transitions or blank/invalid IDs raise ValueError and leave
        state unchanged.
        """
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID must be a non-blank string.")

        trimmed_id = appointment_id.strip()
        appointment = self.data_store.find_appointment(trimmed_id)

        if appointment is None:
            raise LookupError(f"Appointment with ID '{trimmed_id}' not found.")

        # Execute the domain state transition on the stored instance
        appointment.cancel()
        return appointment

    def reschedule_appointment(
            self, appointment_id: str, new_date_time: datetime
    ) -> Appointment:
        """Reschedule a known SCHEDULED appointment to a new date_time.

        Raise LookupError if unknown ID; raise ValueError for blank/invalid IDs,
        invalid datetimes, terminal statuses, or practitioner conflicts.
        """
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID must be a non-blank string.")

        trimmed_id = appointment_id.strip()
        appointment = self.data_store.find_appointment(trimmed_id)
        if appointment is None:
            raise LookupError(f"Appointment with ID '{trimmed_id}' not found.")

        # Check practitioner conflict using the existing data store helper with target exclusion
        if self.data_store.has_practitioner_conflict(
                appointment.practitioner.practitioner_id,
                new_date_time,
                exclude_appointment_id=appointment.appointment_id,
        ):
            raise ValueError(
                "Practitioner already has a SCHEDULED appointment at the requested time"
            )

        # Delegate state update to the domain entity
        appointment.reschedule(new_date_time)
        return appointment

    def list_practitioner_appointments(
            self,
            practitioner_id: str,
            status: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        if not practitioner_id or not practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be blank.")

        cleaned_pid = practitioner_id.strip()

        # Explicitly verify the practitioner exists in the store
        practitioner = self.data_store.find_practitioner(cleaned_pid)
        if practitioner is None:
            raise LookupError(f"Practitioner with ID '{cleaned_pid}' not found.")

        if status is not None and not isinstance(status, AppointmentStatus):
            raise ValueError("Invalid status filter supplied.")

        all_appointments = self.data_store.list_appointments()
        return select_appointments(all_appointments, cleaned_pid, status)