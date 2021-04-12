def greetings(payload: dict) -> dict:
    """Utility function just for demo purpose."""
    msg = payload.get('name', '')
    return {'result': f'Hello {msg}...!'}


def dummy_data() -> None:
    """
    Function to create dummy data for API testing using Postman.

    :return:
    :rtype:
    """
    import json

    data = []
    for i in range(1, 10001):
        data.append({
            "service_name": f"greeting {round(int(10000 % i))}",
            "name": f"Dummy Client {i}",
            'redirect_location': {
                'url': 'http://127.0.0.1:8001/jobs-result',
                'method': 'POST'
            }
        })
    with open('tests.json', 'w') as fp:
        fp.writelines(json.dumps(data))
