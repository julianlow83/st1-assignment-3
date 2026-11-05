"""Three in-memory collections, valid only for the current session."""

from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
    required_text,
)


class SmartCareDataStore:
    """Own three in-memory collections for one SmartCare session."""

    def __init__(self) -> None:
        """Create an empty store for the current session."""
        self._patients: dict[str, Patient] = {}
        self._practitioners: dict[str, Practitioner] = {}
        self._appointments: dict[str, Appointment] = {}

    def add_patient(self, patient: Patient) -> None:
        """Store a Patient; reject a wrong type or duplicate ID with
        ValueError.
        """
        if not isinstance(patient, Patient):
            raise ValueError('Expected a Patient object')
        if patient.patient_id in self._patients:
            raise ValueError('Patient ID already exists')
        self._patients[patient.patient_id] = patient

    def find_patient(self, patient_id: str) -> Patient | None:
        """Return the stored patient or None; reject blank IDs with
        ValueError.
        """
        return self._patients.get(required_text(patient_id, 'Patient ID'))

    def list_patients(self) -> list[Patient]:
        """Return a new list containing the stored patient objects."""
        return list(self._patients.values())

    def add_practitioner(self, practitioner: Practitioner) -> None:
        """Store a Practitioner; reject wrong types or duplicate IDs with
        ValueError.
        """
        if not isinstance(practitioner, Practitioner):
            raise ValueError('Expected a Practitioner object')
        if practitioner.practitioner_id in self._practitioners:
            raise ValueError('Practitioner ID already exists')
        self._practitioners[practitioner.practitioner_id] = practitioner

    def find_practitioner(self, practitioner_id: str) -> Practitioner | None:
        """Return the stored practitioner or None; reject blank IDs with
        ValueError.
        """
        return self._practitioners.get(
            required_text(practitioner_id, 'Practitioner ID'),
        )

    def list_practitioners(self) -> list[Practitioner]:
        """Return a new list containing the stored practitioner objects."""
        return list(self._practitioners.values())

    def add_appointment(self, appointment: Appointment) -> None:
        """Store an appointment with the actual registered participant
        objects.

        Raise ValueError for wrong types, duplicate IDs or unregistered
        objects. Do not change stored records when insertion fails.
        """
        if not isinstance(appointment, Appointment):
            raise ValueError('Expected an Appointment object')
        if appointment.appointment_id in self._appointments:
            raise ValueError('Appointment ID already exists')
        if self.find_patient(
            appointment.patient.patient_id,
        ) is not appointment.patient:
            raise ValueError('Patient must be registered in this data store')
        if self.find_practitioner(
            appointment.practitioner.practitioner_id,
        ) is not appointment.practitioner:
            raise ValueError(
                'Practitioner must be registered in this data store',
            )
        self._appointments[appointment.appointment_id] = appointment

    def find_appointment(self, appointment_id: str) -> Appointment | None:
        """Return the stored appointment by ID or None if absent.

        Fault F8-02 injected: Cancelled appointments are incorrectly filtered out.
        """
        appointment = self._appointments.get(
            required_text(appointment_id, 'Appointment ID'),
        )
        # BUG (F8-02): Returns None if status is CANCELLED, violating FR-07 / AC-05.2
        if appointment is not None and appointment.status == AppointmentStatus.CANCELLED:
            return None
        return appointment

    def list_appointments(self) -> list[Appointment]:
        """Return a new list containing all stored appointment objects."""
        return list(self._appointments.values())

    def has_practitioner_conflict(self, practitioner_id: str, date_time: datetime) -> bool:
        """Return True if practitioner_id already has a SCHEDULED appointment at date_time.

        Fault F8-01 injected: Checks only date_time across ALL practitioners instead of practitioner_id.
        """
        for appt in self._appointments.values():
            # BUG (F8-01): Missing check for appt.practitioner.practitioner_id == practitioner_id
            if appt.date_time == date_time and appt.status == AppointmentStatus.SCHEDULED:
                return True  # Incorrectly blocks DIFFERENT practitioners at the same time
        return False