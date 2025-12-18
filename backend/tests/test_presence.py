import pytest
from httpx import AsyncClient
from app.utils.mongodb import MongoDB


@pytest.mark.asyncio
async def test_presence_reporting_and_get(client_test: AsyncClient):
    # Create a session
    resp = await client_test.post('/session', json={'instructor_id': 'inst-test', 'class_name': 'Test Class'})
    assert resp.status_code == 200
    body = resp.json()
    session_id = body['session_id']
    # Report presence
    p_resp = await client_test.post(f'/session/{session_id}/presence', json={
        'student_id': 'student_test',
        'rssi': -55,
        'device_model': 'TestModel',
        'device_os': 'TestOS',
    })
    assert p_resp.status_code == 200
    p_json = p_resp.json()
    assert p_json.get('success') is True
    # Fetch logs
    logs_resp = await client_test.get(f'/session/{session_id}/presence')
    assert logs_resp.status_code == 200
    logs = logs_resp.json()
    assert isinstance(logs, list)
    assert any(l['student_id'] == 'student_test' and l['rssi'] == -55 for l in logs)
