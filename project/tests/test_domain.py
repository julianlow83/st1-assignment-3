"""
Domain Unit Tests for SmartCare Application (Stage 7).
"""

from datetime import datetime
import pytest

from smartcare.domain import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
)

# Patient Domain Tests (TEST-FR01-01, TEST-FR01-02 / Revision 2 Validation)

def test_patient_construction_and_validation():
    """
    TEST-FR01-01: Valid patient construction
    """
    patient = Patient("P101", "Alice Smith")
    assert patient.patient_id == "P101"
    assert patient.name == "Alice Smith"


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_blank_patient_id_rejected(invalid_id):
    """
    TEST-FR01-02: Blank/invalid patient ID validation contract check
    """
    with pytest.raises(ValueError):
        Patient(invalid_id, "Alice Smith")


@pytest.mark.parametrize("invalid_name", ["", "   ", None])
def test_blank_patient_name_rejected(invalid_name):
    """
    Revision 2 Validation Contract: Required name validation.
    """
    with pytest.raises(ValueError):
        Patient("P101", invalid_name)



# Practitioner Domain Tests (FR-03 / Revision 2 Validation)

def test_practitioner_construction_and_validation():
    """
    Verifies that a Practitioner object correctly stores and exposes attributes.
    """
    practitioner = Practitioner("D201", "Dr. John Doe", "Cardiology")
    assert practitioner.practitioner_id == "D201"
    assert practitioner.name == "Dr. John Doe"
    assert practitioner.specialty == "Cardiology"


@pytest.mark.parametrize("invalid_id", ["", "   ", None])
def test_blank_practitioner_id_rejected(invalid_id):
    """
    Revision 2 Validation Contract: Practitioner ID validation.
    Verifies that blank practitioner IDs raise ValueError.
    """
    with pytest.raises(ValueError):
        Practitioner(invalid_id, "Dr. John Doe", "Cardiology")



# Appointment Domain Tests (TEST-FR02-01, TEST-FR05-01, TEST-FR06-01, TEST-FR07-07)

def test_appointment_initial_status():
    """
    TEST-FR02-01 / Reference Intention:
    Verifies that an Appointment initializes with SCHEDULED status.
    """
    patient = Patient("P101", "Alice Smith")
    practitioner = Practitioner("D201", "Dr. John Doe", "GP")
    booking_time = datetime(2026, 11, 1, 10, 0)

    appointment = Appointment("A301", patient, practitioner, booking_time)

    assert appointment.appointment_id == "A301"
    assert appointment.patient == patient
    assert appointment.practitioner == practitioner
    assert appointment.date_time == booking_time
    assert appointment.status == AppointmentStatus.SCHEDULED


def test_appointment_cancellation_guards():
    """
    TEST-FR06-01: Guarded cancellation & status mutation.
    """
    patient = Patient("P101", "Alice Smith")
    practitioner = Practitioner("D201", "Dr. John Doe", "GP")
    appointment = Appointment("A301", patient, practitioner, datetime(2026, 11, 1, 10, 0))

    assert appointment.status == AppointmentStatus.SCHEDULED

    appointment.cancel()
    assert appointment.status == AppointmentStatus.CANCELLED


def test_repeated_cancellation_rejected():
    """
    TEST-FR06-01 (Negative): Repeated cancellation rejection guard.
    """
    patient = Patient("P101", "Alice Smith")
    practitioner = Practitioner("D201", "Dr. John Doe", "GP")
    appointment = Appointment("A301", patient, practitioner, datetime(2026, 11, 1, 10, 0))

    appointment.cancel()
    assert appointment.status == AppointmentStatus.CANCELLED

    # Repeated cancellation attempt must be rejected without mutating state
    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED


def test_completed_appointment_cancellation_rejected():
    """
    TEST-FR07-07 / Status Guard Boundary:
    """
    patient = Patient("P101", "Alice Smith")
    practitioner = Practitioner("D201", "Dr. John Doe", "GP")
    appointment = Appointment(
        "A301", patient, practitioner, datetime(2026, 11, 1, 10, 0), status=AppointmentStatus.COMPLETED
    )
    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status == AppointmentStatus.COMPLETED