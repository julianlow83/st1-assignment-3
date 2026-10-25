"""Unit tests for Stage 6 SmartCare service operations."""

from datetime import datetime
import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


@pytest.fixture
def store_and_services():
    """Fixture providing a fresh data store and wired service instances."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)
    return store, patient_svc, practitioner_svc, appointment_svc



# Patient Lookup Tests

def test_find_patient_success(store_and_services):
    """Assert valid lookup returns the exact stored Patient object."""
    _, patient_svc, _, _ = store_and_services
    registered = patient_svc.register_patient("P101", "Alice Smith")

    retrieved = patient_svc.find_patient("P101")
    assert retrieved is registered
    assert retrieved.patient_id == "P101"
    assert retrieved.name == "Alice Smith"


def test_find_patient_trimmed_and_case_sensitive(store_and_services):
    """Assert whitespace is trimmed and lookups are strictly case-sensitive."""
    _, patient_svc, _, _ = store_and_services
    registered = patient_svc.register_patient("P101", "Alice Smith")

    # Trimmed whitespace lookup succeeds
    retrieved = patient_svc.find_patient("  P101  ")
    assert retrieved is registered

    # Case mismatch raises LookupError
    with pytest.raises(LookupError):
        patient_svc.find_patient("p101")


def test_find_patient_unknown_raises_lookup_error(store_and_services):
    """Assert valid but absent ID raises LookupError."""
    _, patient_svc, _, _ = store_and_services

    with pytest.raises(LookupError):
        patient_svc.find_patient("P999")


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_find_patient_invalid_id_raises_value_error(store_and_services, invalid_id):
    """Assert blank, whitespace-only, or non-string IDs raise ValueError."""
    _, patient_svc, _, _ = store_and_services

    with pytest.raises(ValueError):
        patient_svc.find_patient(invalid_id)


# Practitioner Lookup Tests


def test_find_practitioner_success(store_and_services):
    """Assert valid lookup returns the exact stored Practitioner object."""
    _, _, practitioner_svc, _ = store_and_services
    registered = practitioner_svc.register_practitioner("D201", "Dr. John Doe", "Cardiology")

    retrieved = practitioner_svc.find_practitioner("D201")
    assert retrieved is registered
    assert retrieved.practitioner_id == "D201"


def test_find_practitioner_trimmed_and_case_sensitive(store_and_services):
    """Assert whitespace is trimmed and practitioner lookup is case-sensitive."""
    _, _, practitioner_svc, _ = store_and_services
    registered = practitioner_svc.register_practitioner("D201", "Dr. John Doe", "Cardiology")

    # Trimmed whitespace succeeds
    retrieved = practitioner_svc.find_practitioner("  D201\t")
    assert retrieved is registered

    # Case mismatch raises LookupError
    with pytest.raises(LookupError):
        practitioner_svc.find_practitioner("d201")


def test_find_practitioner_unknown_raises_lookup_error(store_and_services):
    """Assert valid but absent practitioner ID raises LookupError."""
    _, _, practitioner_svc, _ = store_and_services

    with pytest.raises(LookupError):
        practitioner_svc.find_practitioner("D999")


@pytest.mark.parametrize("invalid_id", ["", "   ", None])
def test_find_practitioner_invalid_id_raises_value_error(store_and_services, invalid_id):
    """Assert blank or invalid practitioner IDs raise ValueError."""
    _, _, practitioner_svc, _ = store_and_services

    with pytest.raises(ValueError):
        practitioner_svc.find_practitioner(invalid_id)



# Appointment Cancellation Tests for FR-06 & FR-07

def test_cancel_appointment_success_and_retained_history(store_and_services):
    """Assert cancelling SCHEDULED updates status, returns same object, and retains in history."""
    _, patient_svc, practitioner_svc, appointment_svc = store_and_services
    patient_svc.register_patient("P101", "Alice Smith")
    practitioner_svc.register_practitioner("D201", "Dr. John Doe", "GP")
    
    booked = appointment_svc.book_appointment(
        "A301", "P101", "D201", datetime(2026, 11, 1, 10, 0)
    )
    assert booked.status == AppointmentStatus.SCHEDULED

    # Execute Cancellation
    cancelled = appointment_svc.cancel_appointment("A301")

    # Assert same object and status transition
    assert cancelled is booked
    assert cancelled.status == AppointmentStatus.CANCELLED

    # FR-07: Assert object remains retrievable in session store history
    retrieved = appointment_svc.find_appointment("A301")
    assert retrieved is booked
    assert retrieved.status == AppointmentStatus.CANCELLED


def test_cancel_appointment_repeated_cancellation_raises_value_error(store_and_services):
    """Assert repeated cancellation of an already CANCELLED appointment raises ValueError."""
    _, patient_svc, practitioner_svc, appointment_svc = store_and_services
    patient_svc.register_patient("P101", "Alice Smith")
    practitioner_svc.register_practitioner("D201", "Dr. John Doe", "GP")
    
    appointment_svc.book_appointment("A301", "P101", "D201", datetime(2026, 11, 1, 10, 0))
    appointment_svc.cancel_appointment("A301")

    # Second cancellation attempt must raise ValueError
    with pytest.raises(ValueError):
        appointment_svc.cancel_appointment("A301")


def test_cancel_appointment_unknown_and_invalid_ids(store_and_services):
    """Assert unknown appointment ID raises LookupError; blank ID raises ValueError."""
    _, _, _, appointment_svc = store_and_services

    # Unknown ID
    with pytest.raises(LookupError):
        appointment_svc.cancel_appointment("A999")

    # Blank / Invalid IDs
    with pytest.raises(ValueError):
        appointment_svc.cancel_appointment("   ")
    with pytest.raises(ValueError):
        appointment_svc.cancel_appointment("")