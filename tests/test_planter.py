import os
import base64
import pytest
from mock import MagicMock
from mock import patch
import json
from typing import Sequence, Tuple, List
import aglabler


def detection(s3: str, pairs: Sequence[Tuple[str, float]]):
    return {
        's3': s3,
        'detection': {
           "LabelModelVersion": "string",
           "Labels": [
              {
                 "Confidence": pair[1],
                 "Instances": [],
                 "Name": pair[0],
                 "Parents": []
              } for pair in pairs
           ],
           "OrientationCorrection": ""
        }
    }


def kinesis(records):
    return {
        'Records': [{'data': base64.b64encode(json.dumps(r).encode())} for r in records]
    }


@pytest.mark.parametrize('event,calls', [
    [kinesis([detection('aaa', [('a', 0.7), ('b', 0.8)])]), ['aaa']],
    [kinesis([detection('aaa', [('a', 0.7), ('b', 0.8)]), detection('bbb', [('a', 0.7), ('c', 0.8)])]), ['aaa', 'bbb']],
    [kinesis([detection('aaa', [('c', 0.7), ('d', 0.8)])]), []]
])
def test_handler(event, calls: [List[str]]):
    env = {
        'DETECTION_LABELS': 'a,b,c',
        'SMTP_HOST': 'test_host',
        'EMAIL_TO': 'a@a.test',
        'EMAIL_FROM': 'b@b.test',
        'EMAIL_SUBJECT': 'test subject'
    }
    with patch.dict(os.environ, env):
        mock_send = MagicMock()
        mock_smtp = MagicMock()
        with patch('aglabler.planter.smtplib.SMTP', return_value=mock_smtp):
            with patch('aglabler.planter.send_email', new=mock_send):
                aglabler.planter.handler(event, {})
                if calls:
                    assert mock_send.call_count == len(calls)
                    for i, call in enumerate(calls):
                        assert mock_send.mock_calls[i].args == (mock_smtp, call)
            mock_smtp.quit.assert_called_once()
