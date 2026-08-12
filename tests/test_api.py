def test_get_parking_spaces(client):
    """
    Test if the API successfully returns the list of parking spaces.
    """
    response = client.get("/api/v1/parking-spaces")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["code"] == "TEST-101"


def test_create_reservation_success(client):
    """
    Test the successful creation of a new reservation (Happy Path).
    """
    payload = {
        "parking_space_id": 1,
        "applicant_name": "Test User",
        "start_time": "2026-08-15T10:00:00Z",
        "end_time": "2026-08-15T12:00:00Z"
    }
    response = client.post("/api/v1/reservations", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["applicant_name"] == "Test User"
    assert data["status"] == "CONFIRMED"


def test_create_reservation_conflict(client):
    """
    Test the overlap prevention logic. A second reservation overlapping 
    the first one should be rejected with a 409 Conflict.
    """
    # Create the initial reservation
    payload1 = {
        "parking_space_id": 1,
        "applicant_name": "User One",
        "start_time": "2026-08-15T10:00:00Z",
        "end_time": "2026-08-15T12:00:00Z"
    }
    client.post("/api/v1/reservations", json=payload1)

    # Attempt to create an overlapping reservation
    payload2 = {
        "parking_space_id": 1,
        "applicant_name": "User Two",
        "start_time": "2026-08-15T11:00:00Z",
        "end_time": "2026-08-15T13:00:00Z"
    }
    response = client.post("/api/v1/reservations", json=payload2)
    
    # Assert conflict is handled
    assert response.status_code == 409


def test_cancel_reservation(client):
    """
    Test the cancellation logic of an existing reservation.
    """
    # First, create a reservation
    payload = {
        "parking_space_id": 1,
        "applicant_name": "To Be Cancelled",
        "start_time": "2026-08-16T10:00:00Z",
        "end_time": "2026-08-16T12:00:00Z"
    }
    create_response = client.post("/api/v1/reservations", json=payload)
    reservation_id = create_response.json()["id"]

    # Cancel the reservation via the dedicated cancel endpoint
    cancel_response = client.post(f"/api/v1/reservations/{reservation_id}/cancel")
    assert cancel_response.status_code == 200

    # Verify the reservation is marked cancelled and the space can be rebooked
    cancelled_data = cancel_response.json()
    assert cancelled_data["status"] == "CANCELLED"

    rebook_response = client.post("/api/v1/reservations", json=payload)
    assert rebook_response.status_code == 201