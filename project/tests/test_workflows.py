import pytest
from datetime import datetime
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService, PractitionerService, AppointmentService
from smartcare.domain import AppointmentStatus

def test_service_list_practitioner_appointments_cases():
    store = SmartCareDataStore()
    p_svc = PatientService(store)
    d_svc = PractitionerService(store)
    a_svc = AppointmentService(store)

    p_svc.register_patient("P1", "Alice")
    d_svc.register_practitioner("D1", "Dr. House", "GP")

    dt = datetime(2026, 11, 1, 10, 0)
    a_svc.book_appointment("A1", "P1", "D1", dt)

    # 1. Known practitioner with matching appointment
    appts = a_svc.list_practitioner_appointments("D1")
    assert len(appts) == 1

    # 2. Known practitioner with no matching status
    cancelled_list = a_svc.list_practitioner_appointments("D1", status=AppointmentStatus.CANCELLED)
    assert cancelled_list == []

    # 3. Valid unknown practitioner ID raises LookupError
    with pytest.raises(LookupError):
        a_svc.list_practitioner_appointments("D999")

    # 4. Blank or invalid ID raises ValueError
    with pytest.raises(ValueError):
        a_svc.list_practitioner_appointments("")

    # 5. Non-enum status string raises ValueError
    with pytest.raises(ValueError):
        a_svc.list_practitioner_appointments("D1", status="scheduled") # type: ignore