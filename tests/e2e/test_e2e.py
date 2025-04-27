import message
import inbox_client_protocol
import ai_client

import pytest
import csv
import os


import inbox_client_impl
import message_impl
import ai_client_impl

@pytest.mark.integration
def test_e2e() -> None:
    client = inbox_client_protocol.get_client()
    gemini_client = ai_client.get_client()
    session_id = gemini_client.start_new_session("test_user")
    result = {}
    msgs = client.get_messages()
    msg = msgs.next()
    message = (f"Analyze this email and give me the percent probability it is spam: Subject: {msg.subject}, Body: {msg.body}, From: {msg.from_} ")
    response = ai_client.send_message(session_id, message)
    assert isinstance(response, dict), "response is not a dict!"
    result[msg.id] = response["content"]
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Email ID", "Percentage Probability of SPAM"])
        for key,value in result.items():
            writer.writerow([key,value])
    assert os.path.exists('output.csv'), "CSV file was not created!"