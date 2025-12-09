import json
import torch

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    number_str = params.get("number", "2")

    try:
        number = float(number_str)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid number parameter"})
        }

    tensor = torch.tensor([number])
    doubled = tensor * 2

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "PyTorch API is working",
            "original": tensor.tolist(),
            "doubled": doubled.tolist()
        })
    }